//#define LIGHTING
//#define VERTICALFOG

#ifdef LIGHTING
varying		lowp	vec4	vLight;
#endif

uniform lowp	sampler2D LightMapSampler;
uniform lowp	sampler2D Texture1;
uniform lowp	sampler2D Texture2;
varying lowp    vec4 	vColor;
varying mediump	vec2 	vCoord0;
varying mediump	vec2 	vCoord1;

#ifdef USE_MASK
uniform lowp	sampler2D 			MaskSampler;
uniform mediump float 		MaskContrast;
#endif	//USE_MASK

//FOG
uniform 	lowp	vec4 	FogColor;
varying 	lowp	float 	FogFactor;

#ifdef EDITOR_DIFFUSE_DENSITY
uniform		highp	vec2 Texture1_size;
#endif

#ifdef EDITOR_LIGHTMAP_DENSITY
uniform		highp	vec2 LightMapSampler_size;
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
    lowp vec4 _LightMap	= vec4(1.0, 1.0, 1.0, 1.0);
#else // EDITOR_DIFFUSE
    lowp vec4 _LightMap	= texture2D(LightMapSampler, vCoord1, -1.0) * 2.0;
#endif //EDITOR_DIFFUSE

#ifdef EDITOR_LIGHTMAP
	lowp vec4 _Texture1	= texture2D(Texture1, vCoord0, -1.0);
	_Texture1 = vec4(1.0, 1.0, 1.0, _Texture1.a);
	lowp vec4 _Texture2	= texture2D(Texture2, vCoord0, -1.0);
	_Texture2 = vec4(1.0, 1.0, 1.0, _Texture2.a);
#else // EDITOR_LIGHTMAP
	lowp vec4 _Texture1	= texture2D(Texture1, vCoord0, -1.0);
	lowp vec4 _Texture2	= texture2D(Texture2, vCoord0, -1.0);
#endif //EDITOR_LIGHTMAP
	
	lowp float BlendFactor = vColor.a;
	
#ifdef USE_MASK
	lowp float MaskColor = texture2D(MaskSampler, vCoord0).r;
	BlendFactor	= clamp(BlendFactor + BlendFactor * MaskColor * MaskContrast, 0.0, 1.0);
#endif	//USE_MASK

#ifdef LIGHTING
	lowp vec4 Color 	= (_LightMap + vLight) * mix(_Texture1, _Texture2, BlendFactor) * vec4(vColor.rgb, 1.0);
#else
	lowp vec4 Color 	= _LightMap * mix(_Texture1, _Texture2, BlendFactor) * vec4(vColor.rgb, 1.0);
#endif	//LIGHTING
	
#ifdef VERTICALFOG
#ifdef TEXTURE_FOG
	lowp	vec4 FogMapColor		= vec4(texture2D(FogTexture, FogUV).rgb, VerticalFogAlpha);
	lowp 	vec4 fogCol2 			= mix(FogMapColor, FogColor, clamp(FogY, 0.0, 1.0));
	Color							= mix(Color, fogCol2, clamp(FogFactor, 0.0, 1.0) * fogCol2.a);
#else // TEXTURE_FOG
	Color							= ComputeFogFS(Color, vFogColor, clamp(FogFactor, 0.0, 1.0));
#endif
#else
	Color							= ComputeFogFS(Color, FogColor, clamp(FogFactor, 0.0, 1.0));
#endif	//VERTICALFOG
	

	gl_FragColor					= Color;

#ifdef EDITOR_DIFFUSE_DENSITY
	highp vec2 PixelCoord			= Texture1_size * vCoord0;
	highp float TexSize				= Texture1_size.x;
	highp float Alpha				= _Texture1.a;
	highp float Step				= 0.015625;
#endif
	
#ifdef EDITOR_LIGHTMAP_DENSITY
	highp vec2 PixelCoord			= LightMapSampler_size * vCoord1;
	highp float TexSize				= LightMapSampler_size.x;
	highp float Alpha				= _LightMap.a;
	highp float Step				= 0.03125;
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


#ifdef DEBUG_HEIGHTMAP
	gl_FragColor					= vColor;
#endif

#ifdef DEBUG_LIGHTING
	gl_FragColor 					= vLight;
#endif
}
