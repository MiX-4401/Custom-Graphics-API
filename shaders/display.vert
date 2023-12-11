# version 460 core

in vec2 aPosition;
in vec2 aTexCoord;
out vec2 uvs;

void main () {
    uvs = aTexCoord;

    gl_Position = vec4(aPosition, 0.0, 1.0);
}