//#define LIGHTING
//#define LIGHTING_MALI
//#define VERTICALFOG
//#define TEXTURE_FOG
//#define REFLECTION
//#define GLASS

//#define VERTICAL_FOG_COLOR vec4(0.93, 0.76, 0.47, 0.35)
//#define VERTICAL_FOG_HEIGHT	18.0

#if defined(LIGHTING) && !defined(LPLD)
	#if defined(LIGHTING_MALI)
	varying		mediump	vec3	vNormal;
	varying		mediump	vec3	vPosition;
	#else
uniform		highp	vec3	Light0PositionOS;
uniform		highp	vec3	Light0attenuation;
uniform		highp	vec4	Light0diffuseColor;

#ifndef LIGHTING_LOW
uniform		highp	vec3	Light1PositionOS;
uniform		highp	vec3	Light1attenuation;
uniform		highp	vec4	Light1diffuseColor;

/*
uniform		highp	vec3	Light2PositionOS;
uniform		highp	vec3	Light2attenuation;
uniform		highp	vec4	Light2diffuseColor;
*/
#endif

varying		lowp	vec4	vLight;
	#endif	//LIGHTING_MALI
#endif	//LIGHTING

#ifdef DEBUG_HEIGHTMAP
varying		lowp	vec4	vColor;
#endif

attribute 	highp	vec3 	Normal;
attribute 	highp	vec4 	Position;
attribute	lowp	vec4	Color;
attribute 	highp	vec2 	Coord0;
attribute 	highp	vec2 	Coord1;

uniform 	highp 	vec4 	Coord0_scaleoffset;
uniform 	highp 	vec4 	Coord1_scaleoffset;

uniform 	highp	mat4	WorldViewProjection;
uniform     highp	vec4	LightMapAtlas;

//varying		lowp	vec4	vColor;// ATICA - removed on 26.04 to save memory in batching
varying		highp	vec2 	vCoord0;
varying		highp	vec2 	vCoord1;

#if defined(REFLECTION) && defined(GLASS) && defined(SPHEREMAP)
uniform 	highp	mat4	WorldInverse;
uniform 	highp	mat4	ViewInverse;

varying		lowp	vec2	vSpheremapUV;

lowp vec2 SpheremapUV(lowp vec3 I, lowp vec3 N)
{
	lowp vec3 R = reflect(-I, N);
	lowp float L = length(R + vec3(0.0, 0.0, 1.0));
	return (R.xy / (2.0 * L) + 0.5);
}
#endif	//REFLECTION

//FOG
uniform 	highp	mat4	WorldViewTransposed;
uniform 	highp	vec2 	FogStartEnd;
uniform 	lowp	vec4 	FogColor;

varying 	lowp	float 	FogFactor;

/*
float ComputeFogVS(vec4 pos, mat4 WVT, vec2 fogSE)
{
	highp	float depth			= dot(WVT[2], pos);
	return (-depth - fogSE.x)/(fogSE.y - fogSE.x);
}
*/

#ifdef VERTICALFOG
uniform 	highp	mat4	World;
uniform		mediump float	VerticalFogHeight;

#ifdef TEXTURE_FOG
varying 	highp 	vec2 	FogUV;
varying 	lowp 	float 	FogY;
uniform		highp	vec4	FogMap;
#else
varying		lowp	vec4	vFogColor;
#endif
#endif	//VERTICALFOG

void main()
{
//	vColor						= Color;// ATICA - removed on 26.04 to save memory in batching
	vCoord0 					= Coord0 * Coord0_scaleoffset.xy + Coord0_scaleoffset.zw;
#ifdef MAX_LIGHTMAP
	vCoord1 					= Coord1 * Coord1_scaleoffset.xy + Coord1_scaleoffset.zw;
#else
	vCoord1						= (Coord1 * Coord1_scaleoffset.xy + Coord1_scaleoffset.zw) * LightMapAtlas.xy + LightMapAtlas.zw;
#endif

	gl_Position 				= WorldViewProjection * Position;

#if defined(LIGHTING) && !defined(LPLD)
	#if defined(LIGHTING_MALI)
		vNormal = Normal;
		vPosition = Position.xyz;
	#else
		lowp vec3 fvNormal			= normalize(Normal);
	// Point Lights
	highp	float fNDotL;
	highp 	float fDistance;
	highp 	float fAttenuation;
	highp	vec3  fvLightDirection;
	highp	vec3  fvDirection;
	highp	vec4  fvLightColor;
	
	// Light 0
	fvDirection					= Light0PositionOS - Position.xyz;
	fDistance					= length(fvDirection);
	fAttenuation				= clamp(1.0 - fDistance * Light0attenuation[1], 0.0, 1.0);
	fvLightDirection			= normalize(fvDirection);
	fNDotL						= clamp(dot(fvLightDirection, fvNormal), 0.0, 1.0);
	fvLightColor				= Light0diffuseColor * (fNDotL * fAttenuation);
	
#ifndef LIGHTING_LOW
	
	// Light 1
	fvDirection					= Light1PositionOS - Position.xyz;
	fDistance					= length(fvDirection);
	fAttenuation				= clamp(1.0 - fDistance * Light1attenuation[1], 0.0, 1.0);
	fvLightDirection			= normalize(fvDirection);
	fNDotL						= clamp(dot(fvLightDirection, fvNormal), 0.0, 1.0);
	fvLightColor				+= Light1diffuseColor * (fNDotL * fAttenuation);
	
	// Light 2
/*	fvDirection					= Light2PositionOS - Position.xyz;
	fDistance					= length(fvDirection);
	fvLightDirection			= normalize(fvDirection);
	fAttenuation				= clamp(1.0 - fDistance * Light2attenuation[1], 0.0, 1.0);
	fNDotL						= clamp(dot(fvLightDirection, fvNormal), 0.0, 1.0);
	fvLightColor				+= Light2diffuseColor * (fNDotL * fAttenuation);*/
	//////////////
#endif

	vLight						= fvLightColor;
	#endif	//LIGHTING_MALI
#endif	//LIGHTING
	
#if defined(REFLECTION) && defined(GLASS) && defined(SPHEREMAP)
		#if !defined(LIGHTING) || defined(LPLD) || defined(LIGHTING_MALI)
		lowp vec3 fvNormal			= normalize(Normal);
		#endif
	vSpheremapUV				= SpheremapUV(normalize(WorldInverse * ViewInverse[3] - Position).xyz, fvNormal);
#endif	//REFLECTION
	
	//fog
	FogFactor                       = (-dot(WorldViewTransposed[2], Position) - FogStartEnd.x) * FogStartEnd.y;
	
#ifdef VERTICALFOG
	lowp float fY				= dot(vec4(World[0].z, World[1].z, World[2].z, World[3].z), vec4(Position.xyz, 1.0)) * VerticalFogHeight;
	fY							+= FogFactor * 0.5;
	
#ifdef TEXTURE_FOG
	FogUV.xy = ((World * Position).xy - FogMap.xy) * FogMap.zw;
	FogY = fY;
#else
	vFogColor					= mix(VERTICAL_FOG_COLOR, FogColor, fY);
#endif
#endif	//VERTICALFOG

#ifdef DEBUG_HEIGHTMAP
	if ((World * Position).z > HEIGHT_MAX)
		vColor = vec4(COLOR_MAX, 1.0);
	else if ((World * Position).z > HEIGHT_HIGH)
		vColor = vec4(COLOR_HIGH, 1.0);
	else if ((World * Position).z > HEIGHT_MED)
		vColor = vec4(COLOR_MED, 1.0);
	else if ((World * Position).z > HEIGHT_LOW)
		vColor = vec4(COLOR_LOW, 1.0);
	else // min height
		vColor = vec4(COLOR_WHITE, 1.0);
#endif
}