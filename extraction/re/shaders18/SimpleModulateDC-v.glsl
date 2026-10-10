//#define LIGHTING
//#define VERTICALFOG

#ifdef LIGHTING
attribute 	highp	vec3 	Normal;

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
#endif	//LIGHTING

attribute	highp	vec4	Position;
attribute	highp	vec4	Color;
attribute	highp	vec2	TexCoord0;
uniform 	highp 	vec4 	TexCoord0_scaleoffset;

uniform		highp	mat4	WorldViewProjection;

varying		highp	vec4	vColor;
varying		highp	vec2	vCoord0;

#ifdef OUTLINE
uniform		highp	float	Time;
varying		lowp	float	VarOutlineFactor;
#endif

#ifdef EXTRA_DIFFUSE
uniform		lowp	vec4	ExtraDiffuse;
#endif	//EXTRA_DIFFUSE

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
	vColor						= Color;
	vCoord0 					= TexCoord0 * TexCoord0_scaleoffset.xy + TexCoord0_scaleoffset.zw;
	
	gl_Position					= WorldViewProjection * Position;
	
#ifdef EXTRA_DIFFUSE
	vColor 						*= ExtraDiffuse;
#endif	//EXTRA_DIFFUSE
	
#ifdef LIGHTING
	
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
#endif	//LIGHTING

	//fog
	FogFactor                       = (-dot(WorldViewTransposed[2], Position) - FogStartEnd.x) * FogStartEnd.y;
	
#ifdef VERTICALFOG
	lowp float fY				= dot(vec4(World[0].z, World[1].z, World[2].z, World[3].z), vec4(Position.xyz, 1.0)) * VerticalFogHeight;
	fY							+= FogFactor * FOG_DECAY;
	
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