#version 330 core
layout(location = 0) in vec2 position;
layout(location = 1) in vec3 colour;
uniform mat3 model;
uniform mat3 projection;
out vec3 vertexColour;
void main()
{
    vec3 p = projection * model * vec3(position, 1.0);
    gl_Position = vec4(p.xy, 0.0, 1.0);
    vertexColour = colour;
}
