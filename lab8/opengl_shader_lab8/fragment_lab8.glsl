#version 330 core
in vec3 vertexColour;
out vec4 fragmentColour;
void main()
{
    fragmentColour = vec4(vertexColour, 1.0);
}
