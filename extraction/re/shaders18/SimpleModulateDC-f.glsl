//#define LIGHTING
//#define VERTICALFOG
//#define LOD_BIAS -1.0

#ifdef LIGHTING
varying		lowp	vec4	vLight;
#endif

#ifdef TDKR_SPLIT_ALPHA
uniform 	lowp	sampler2D 		DiffuseMap_alpha;
#endif
uniform 	lowp	sampler2D 		DiffuseMap;
varying		lowp	vec4	vColor;
varying		mediump	vec2 	vCoord0;

//FOG
uniform 	lowp	vec4 	FogColor;
varying 	lowp	float 	FogFactor;

#ifdef EDITOR_DIFFUSE_DENSITY
uniform		highp	vec2 DiffuseMap_size;
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

#ifdef SHADOW
uniform		lowp	float	Opacity;
#endif

void main()
{
#ifdef TDKR_SPLIT_ALPHA
	lowp	vec4	DiffuseMapColor	= vec4(texture2D(DiffuseMap, vCoord0, LOD_BIAS).rgb, texture2D(DiffuseMap_alpha, vCoord0, LOD_BIAS).r);
#else
	lowp	vec4	DiffuseMapColor	= texture2D(DiffuseMap, vCoord0, LOD_BIAS);
#endif

#ifdef LIGHTING
	lowp	vec4  Color				= DiffuseMapColor * (1.0 + vLight);
#else
	lowp	vec4  Color				= DiffuseMapColor;
#endif	//LIGHTING
	
	Color 							*= vColor;
	
#ifdef EXTRA_DIFFUSE
	Color.a							*= vColor.a;
#endif
	
#ifdef SHADOW
	Color.a 						*= Opacity;
#endif
	
#ifdef VERTICALFOG
#ifdef TEXTURE_FOG
	lowp	vec4 FogMapColor		= vec4(texture2D(FogTexture, FogUV).rgb, VerticalFogAlpha);
	lowp 	vec4 fogCol2 			= mix(FogMapColor, FogColor, clamp(FogY, 0.0, 1.0));
	Color							= mix(Color, fogCol2, clamp(FogFactor, 0.0, 1.0) * fogCol2.a * Color.a);
#else // TEXTURE_FOG
	Color							= ComputeFogFS(Color, vFogColor, clamp(FogFactor, 0.0, 1.0));
#endif
#else
	Color							= ComputeFogFS(Color, FogColor, clamp(FogFactor, 0.0, 1.0));
#endif	//VERTICALFOG

	Color.a 						= DiffuseMapColor.a;
	
	gl_FragColor					= Color;

#ifdef EDITOR_DIFFUSE_DENSITY
	highp vec2 PixelCoord			= DiffuseMap_size * vCoord0;
	highp float TexSize				= DiffuseMap_size.x;
	highp float Alpha				= DiffuseMapColor.a;
	highp float Step				= 0.015625;
#endif

#if defined(EDITOR_LIGHTMAP_DENSITY)
	highp vec2 PixelCoord			= 0.0;
	highp float TexSize				= 2048.0;
	highp float Alpha				= 0.0;
	highp float Step				= 0.03125;
#endif

#if defined(EDITOR_DIFFUSE_DENSITY) || defined(EDITOR_LIGHTMAP_DENSITY)
  highp float fmodResult = mod(floor(Step * PixelCoord.x) + floor(Step * PixelCoord.y),
                          2.0);

  if (TexSize < 0.0) // no LIGHTMAP -> make it black
  {
		gl_FragColor				= vec4(0.0, 0.0, 0.0, Alpha);
  }
  else
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

#ifdef DEBUG_HEIGHTMAP
	gl_FragColor					= vColor;
#endif

#ifdef DEBUG_LIGHTING
	gl_FragColor 					= vLight;
#endif
}