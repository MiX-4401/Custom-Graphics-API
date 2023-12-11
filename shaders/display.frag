# version 460 core

in vec2 uvs;
out vec4 finalColour;

void main () {

    finalColour = vec4(uvs.xy, 1.0, 1.0);
}