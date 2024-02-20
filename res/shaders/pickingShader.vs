#version 330

attribute vec3 position;
attribute vec3 color;
attribute vec3 normal;
attribute vec2 texCoords;


uniform mat4 Proj;
uniform mat4 View;
uniform mat4 Model;

//out vec3 color0;

void main()
{
	//color0 = color;
	gl_Position = Proj *View * Model* vec4(position, 1.0);
}
