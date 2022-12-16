#version 330

uniform sampler2D texture;
const highp float PI = 3.1415926535897932384626433832795; 

in highp vec4 vertTexCoord;
out highp vec4 fragColor;
uniform highp mat3 rotation;

void main(void) {

  // A shader asks "for a given point in the destination image, what
  // is the color?"

  // vertTexCoord.xy is the coordinate in our destination image, which
  // will be an azimuthal projection of a sphere. 

  // Because we need to deal with the rotations of the sphere, we need
  // to convert vertTexCoord.xy into spherical coordinates.

  // phi is the polar angle, which is the angle formed by the top of the sphere,
  // the origin (center of the sphere) and vertTexCoord.xy:

  highp float phi = 2.0*PI*distance(vertTexCoord.xy,vec2(0.5,0.5)); // [0,pi]

  // we are dealing with a fisheye lens arrangement, so we have to correct for 
  // that distortion here. This next formula is known from Paul Bourke's
  // experimental measurements of the display system and is not mathematically
  // derived:

  phi = 2.0*acos(phi/PI); // NEED TO FIX THIS

  // theta is the azimuthal angle, which is the angle formed by the the point
  // (1,0,0) on the surface of the sphere, the origin, and vertTexCoord.xy:

  highp float theta = atan(0.5-vertTexCoord.y,0.5-vertTexCoord.x); // [-pi,pi]

  // in 3D Cartesian coordinates, we then have:
  vec3 destinationPoint = vec3(
    sin(phi)*cos(theta),
    sin(phi)*sin(theta),
    cos(phi)
  );

  vec3 inputPoint = rotation*destinationPoint;

  // now we need to know the input point's position in the equirectangular 
  // projection we have as input, so we need to convert originPoint to
  // spherical coordinates

  highp float phi2 = acos(inputPoint.z); // [0,pi]
  highp float theta2 = atan(inputPoint.y,inputPoint.x); // [-pi,pi]


  if (phi<PI) {
    fragColor = texture2D(texture, vec2(theta2/(2*PI)+0.5, phi2/PI));
  } else {
    fragColor = vec4(0,0,0,1);
  }
}

