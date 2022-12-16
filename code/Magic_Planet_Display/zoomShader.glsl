#version 330

uniform sampler2D texture;

in highp vec4 vertTexCoord;
out highp vec4 fragColor;
uniform int scale;

void main(void) {
  float ang = atan(vertTexCoord.y-.5, vertTexCoord.x-.5);

  float dist = pow(2*distance(vertTexCoord.xy, vec2(0.5, 0.5)), scale);

  float x = cos(ang)*(dist)/2 + .5;
  float y = sin(ang)*(dist)/2 + .5;

  if(dist > 1) {
    fragColor = texture2D(texture, vertTexCoord.xy);
  } else {
    fragColor = texture2D(texture, vec2(x, y));
  }
}

