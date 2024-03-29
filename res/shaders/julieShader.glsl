#version 330

uniform sampler1D tex;
uniform vec4 data;
uniform int iter;
uniform float p;
uniform float s;

in vec2 texCoords0;

void main() {
	vec2 z, c;

	c.x = (texCoords0.x - 0.5) * 3;
	c.y = (texCoords0.y - 0.5) * 3;

	int i;
	z = c;
	c=vec2( data.x - 0.5 * s - data.z,data.y - 0.5 * s + data.w);
	for(i=0; i<iter; i++) {
        float r = sqrt(z.x * z.x + z.y * z.y), angle = atan(z.y,z.x);     
        float sn = sin(angle*p);
        float cn = cos(angle*p);
		float x = cn*pow(r,p) + c.x;
		float y = sn*pow(r,p) + c.y;
       // float x =  (z.x * z.x - z.y * z.y) + c.x;
		//float y = (z.y * z.x + z.x * z.y) + c.y;
		if((x * x + y * y) > 4.0) break;
		z.x = x;
		z.y = y;
	}

	gl_FragColor = texture1D(tex, (i == iter ? 0.0 : float(i)) / 64.0);
}
