//#define LIGHTING
//#define LIGHTING_MALI
//#define LIGHTING_LOW
//#define VERTICALFOG
//#define TEXTURE_FOG
//#define REFLECTION
//#define GLASS
//#define SPHEREMAP
//#define OPAQUE

//#define VERTICAL_FOG_COLOR (vec4(0.74, 0.66, 0.52, 0.55))
//#define VERTICAL_FOG_HEIGHT	(20.0)
//#define LOD_BIAS -1.0

//GLASS			-	defined in the material
//REFLECTION	-	defined in glsl.config

#if defined(LIGHTING) && !defined(LPLD)
	#if defined(LIGHTING_MALI)
	uniform		mediump	vec3	Light0PositionOS;
	uniform		mediump	vec3	Light0attenuation;
	uniform		mediump	vec4	Light0diffuseColor;
	#ifndef LIGHTING_LOW
	uniform		mediump	vec3	Light1PositionOS;
	uniform		mediump	vec3	Light1attenuation;
	uniform		mediump	vec4	Light1diffuseColor;
	uniform		mediump	vec3	Light2PositionOS;
	uniform		mediump	vec3	Light2attenuation;
	uniform		mediump	vec4	Light2diffuseColor;
	#endif
	varying		mediump	vec3	vNormal;
	varying		mediump	vec3	vPosition;
	#else
varying		lowp	vec4	vLight;
	#endif	//LIGHTING_MALI
#endif	//LIGHTING

#ifdef DEBUG_HEIGHTMAP
varying		lowp	vec4	vColor;
#endif

#if defined(TDKR_SPLIT_ALPHA) && defined(HAS_ALPHA)
uniform 	lowp	sampler2D 		DiffuseMap_alpha;
#endif

uniform 	lowp	sampler2D 		DiffuseMap;
uniform 	lowp	sampler2D 		LightMap;
//varying		lowp	vec4	vColor;// ATICA - removed on 26.04 to save memory in batching
varying		mediump	vec2 	vCoord0;
varying		mediump	vec2 	vCoord1;

#if defined(REFLECTION) && defined(GLASS)
#if defined(SPHEREMAP) || defined(ROOF)
varying		lowp	vec2	vSpheremapUV;
uniform lowp	sampler2D 	ReflectionMapSampler;
#endif

uniform lowp	sampler2D 	DiffuseMaskSampler;
#endif	//REFLECTION, GLASS

//FOG
uniform 	lowp	vec4 	FogColor;
varying 	lowp	float 	FogFactor;

#ifdef EDITOR_DIFFUSE_DENSITY
uniform		highp	vec2 DiffuseMap_size;
#endif

#ifdef EDITOR_LIGHTMAP_DENSITY
uniform		highp	vec2 LightMap_size;
#endif

lowp vec4 ComputeFogFS(lowp vec4 col, lowp vec4 fogCol, lowp float fogF)
{
	lowp 	float 	GrayScale 	= dot(col.xyz, vec3(0.149, 0.293, 0.57));
	lowp 	float 	fFactor		= fogF * (1.0 - GrayScale);
	return vec4(mix(col.rgb, fogCol.rgb, fFactor * fogCol.a), col.a);
}

#ifdef VERTICALFOG
#ifdef TEXTURE_FOG
uniform 	lowp	sampler2D 		FogTexture;
varying 	mediump 	vec2 	FogUV;
varying 	lowp 	float 	FogY;
uniform 	lowp	float 	VerticalFogAlpha;
#else
varying		lowp	vec4	vFogColor;
#endif
#endif	//VERTICALFOG

void main()
{
#ifdef EDITOR_DIFFUSE
	lowp	vec4 	LightMapColor	= vec4(1.0, 1.0, 1.0, 1.0);
#else // EDITOR_DIFFUSE
#ifndef LPLD
	lowp	vec4 	LightMapColor	= texture2D(LightMap, vCoord1) * 2.0;
#endif // LPLD
#endif // EDITOR_DIFFUSE

#ifdef EDITOR_LIGHTMAP
	highp	vec4 	DiffuseMapColor	= texture2D(DiffuseMap, vCoord0, LOD_BIAS);
	DiffuseMapColor 				= vec4(1.0, 1.0, 1.0, DiffuseMapColor.a);
#else // EDITOR_LIGHTMAP
#if defined(TDKR_SPLIT_ALPHA) && defined(HAS_ALPHA)
	highp	vec4 	DiffuseMapColor	= vec4(texture2D(DiffuseMap, vCoord0, LOD_BIAS).rgb, texture2D(DiffuseMap_alpha, vCoord0).r);
#else // TDKR_SPLIT_ALPHA & HAS_ALPHA
	highp	vec4 	DiffuseMapColor	= texture2D(DiffuseMap, vCoord0, LOD_BIAS);
#endif // TDKR_SPLIT_ALPHA & HAS_ALPHA
#endif // EDITOR_LIGHTMAP
	
#ifdef EDITOR_DIFFUSE
	lowp	vec4 	Mask			= vec4(1.0, 1.0, 1.0, 1.0);
	lowp	vec4	reflection		= vec4(0.0, 0.0, 0.0, 0.0);
#else // EDITOR_DIFFUSE
#if defined(REFLECTION) && defined(GLASS)
	lowp	vec4 	Mask			= texture2D(DiffuseMaskSampler, vCoord0);
	
#if defined(SPHEREMAP) //|| defined(ROOF)
	lowp	vec2	ReflectionUV	= vSpheremapUV;
	
	#ifdef ROOF
		ReflectionUV -= vec2((Mask.r - 0.5) * 0.02);
	#else
	#ifdef OPAQUE
		ReflectionUV -= vec2(Mask.g) * 0.02 - vec2(0.01);
	#endif // OPAQUE
	#endif
	
	lowp	vec4	reflection		= texture2D(ReflectionMapSampler, ReflectionUV);
#endif
	
#ifndef ROOF
	LightMapColor					= mix(LightMapColor, vec4(Mask.b), Mask.b);
#endif
#endif	//REFLECTION & GLASS
#endif // EDITOR_DIFFUSE
	
#ifdef EDITOR_DIFFUSE
	lowp	float	FogFactorLight  = clamp(FogFactor, 0.0, 1.0);
#else // EDITOR_DIFFUSE
#ifdef VERTICALFOG
	lowp	float	FogFactorLight	= clamp(FogFactor, 0.0, 1.0);
	
#ifdef LPLD
	FogFactorLight					*= (0.4 + DiffuseMapColor.a * 0.6); //(1.0 - DiffuseMapColor.a * 0.60);
#endif // LPLD

#if defined(REFLECTION) && defined(GLASS)
	FogFactorLight					*= (1.0 - Mask.b * 0.60);
#endif // REFLECTION
#endif // VERTICALFOG
#endif // EDITOR_DIFFUSE

#ifdef EDITOR_DIFFUSE
	lowp	vec4  Color				= DiffuseMapColor;
#else // EDITOR_DIFFUSE
#if defined(LIGHTING) && !defined(LPLD)
	#if defined(LIGHTING_MALI)
		// Point Lights
		mediump	float fNDotL;
		mediump float fDistance;
		mediump float fAttenuation;
		mediump	vec3  fvLightDirection;
		mediump	vec3  fvDirection;
		mediump	vec4  fvLightColor;
		mediump vec3 fvNormal = normalize(vNormal);
		// Light 0
		fvDirection				= Light0PositionOS - vPosition;
		fDistance					= length(fvDirection);
		fAttenuation			= clamp(1.0 - fDistance * Light0attenuation.y, 0.0, 1.0);
		fvLightDirection	= fvDirection / fDistance; //normalize(fvDirection);
		fNDotL						= clamp(dot(fvLightDirection, fvNormal), 0.0, 1.0);
		fvLightColor			= Light0diffuseColor * (fNDotL * fAttenuation);
		#ifndef LIGHTING_LOW
		// Light 1
		fvDirection				= Light1PositionOS - vPosition;
		fDistance					= length(fvDirection);
		fAttenuation			= clamp(1.0 - fDistance * Light1attenuation.y, 0.0, 1.0);
		fvLightDirection	= fvDirection / fDistance; //normalize(fvDirection);
		fNDotL						= clamp(dot(fvLightDirection, fvNormal), 0.0, 1.0);
		fvLightColor			+= Light1diffuseColor * (fNDotL * fAttenuation);
		// Light 2
		fvDirection				= Light2PositionOS - vPosition;
		fDistance					= length(fvDirection);
		fAttenuation			= clamp(1.0 - fDistance * Light2attenuation.y, 0.0, 1.0);
		fvLightDirection	= fvDirection / fDistance; //normalize(fvDirection);
		fNDotL						= clamp(dot(fvLightDirection, fvNormal), 0.0, 1.0);
		fvLightColor			+= Light2diffuseColor * (fNDotL * fAttenuation);
		//////////////
		#endif
		lowp	vec4  Color				= DiffuseMapColor * (LightMapColor + fvLightColor);// * vColor;// ATICA - removed on 26.04 to save memory in batching
	#else
	lowp	vec4  Color				= DiffuseMapColor * (LightMapColor + vLight);// * vColor;// ATICA - removed on 26.04 to save memory in batching
	#endif //LIGHTING_MALI
#else // LIGHTING & LPLD
#ifndef LPLD
	lowp	vec4  Color				= DiffuseMapColor * LightMapColor;// * vColor;// ATICA - removed on 26.04 to save memory in batching
#else // LPLD
	lowp	vec4  Color				= DiffuseMapColor;
#endif // LPLD
#endif	//LIGHTING
#endif // EDITOR_DIFFUSE
	
#if defined(REFLECTION) && defined(GLASS) && defined(SPHEREMAP)	
#ifdef ROOF
	reflection						*= LightMapColor;
	Color							+= reflection * (1.0 - Mask.g);
#else
	Color							+= reflection * (1.0 - Mask.r);
#endif
#endif	//REFLECTION
	
#ifdef VERTICALFOG
#ifdef TEXTURE_FOG
	lowp	vec4 FogMapColor		= vec4(texture2D(FogTexture, FogUV).rgb, VerticalFogAlpha);
	lowp 	vec4 fogCol2 			= mix(FogMapColor, FogColor, clamp(FogY, 0.0, 1.0));
	Color							= mix(Color, fogCol2, FogFactorLight * fogCol2.a);
#else
//	Color							= ComputeFogFS(Color, vFogColor, FogFactorLight);
	Color							= vec4(mix(Color.rgb, vFogColor.rgb, FogFactorLight * vFogColor.a), Color.a);
#endif
#else
	Color							= ComputeFogFS(Color, FogColor, clamp(FogFactor, 0.0, 1.0));
#endif	//VERTICALFOG

#if defined(REFLECTION) && defined(GLASS) && !defined(ROOF) && !defined(OPAQUE)
	Color.a							= Mask.g;
#endif	//REFLECTION

#ifdef OPAQUE
	Color.a = 1.0;
#endif
	
#ifdef VERTEX_ALPHA
//	gl_FragColor					= vec4(Color.rgb, vColor.a);// ATICA - removed on 26.04 to save memory in batching
	gl_FragColor					= vec4(Color.rgb, 1.0);
#endif

	gl_FragColor					= Color;



#ifdef EDITOR_DIFFUSE_DENSITY
	highp vec2 PixelCoord			= DiffuseMap_size * vCoord0;
	highp float TexSize				= DiffuseMap_size.x;
	highp float Alpha				= DiffuseMapColor.a;
	highp float Step				= 0.015625;
#endif
	
#ifdef EDITOR_LIGHTMAP_DENSITY
	highp vec2 PixelCoord			= LightMap_size * vCoord1;
	highp float TexSize				= LightMap_size.x;
	highp float Alpha				= LightMapColor.a;
	highp float Step				= 0.0625;
#endif
	

#if defined(EDITOR_DIFFUSE_DENSITY) || defined(EDITOR_LIGHTMAP_DENSITY)
  highp float fmodResult = mod(floor(Step * PixelCoord.x) + floor(Step * PixelCoord.y),
                          2.0);

  if (fmodResult < 1.0) {
  	if (TexSize > 1024.0) // 2048
		gl_FragColor				= vec4(0.2, 0.5, 0.0, Alpha);
	else if (TexSize > 512.0) // 1024
		gl_FragColor				= vec4(1.0, 0.6, 0.0, Alpha);
	else if (TexSize > 256.0) // 512
		gl_FragColor				= vec4(1.0, 0.3, 0.0, Alpha);
	else // 256 or lower
		gl_FragColor				= vec4(1.0, 0.0, 0.0, Alpha);
  } else {
		gl_FragColor				= vec4(1.0, 1.0, 1.0, Alpha);
  }	
#endif //EDITOR_DIFFUSE_DENSITY || EDITOR_LIGHTMAP_DENSITY

#ifdef DEBUG_LIGHTING
	gl_FragColor 					= vLight;
#endif

#ifdef DEBUG_HEIGHTMAP
	gl_FragColor					= vColor;
#endif

#ifdef ALPHA_TEST
	if (DiffuseMapColor.a < 0.5)
		discard;
#endif
}