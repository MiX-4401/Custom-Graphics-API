# version 460 core

uniform sampler2D sourceTexture;

in vec2 uvs;
out vec4 finalColour;

void main () {
    vec4 sourceImage = texture(sourceTexture, uvs).rgba;

    finalColour = vec4(sourceImage.rgb, sourceImage.a);
}