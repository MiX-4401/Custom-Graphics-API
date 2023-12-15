# version 460 core

uniform sampler2D myTexture;
uniform float time;

in vec2 uvs;
out vec4 finalColour;

void main () {
    vec4 fragColour = texture(myTexture, uvs).rgba;

    finalColour = vec4(uvs.x + sin(time * 0.01), uvs.y, 1.0, fragColour.a);
}