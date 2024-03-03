#include "glm/detail/type_vec.hpp"
#include "glm/glm.hpp"
#include <stdio.h>

namespace glm{
    vec2 quickTwoSum(   float a,    float b)
    {
         vec2 result;
        result.x = a + b;
        result.y = b - (result.x - a);
        return result;
    }

    vec2 Split32(   float a)
    {
         vec2 result;
        const float c = 4097.0; // 2^12 + 1
        
        float temp = c * a;
        result.x = temp - (temp - a);
        result.y = a - result.x;
        return result;
    }

    vec2 twoProd(   float a,    float b)
    {
         vec2 p;
        p.x = a * b;
         vec2 aS = Split32(a);
         vec2 bS = Split32(b);
        
        p.y = (aS.x * bS.x - p.x) + aS.x * bS.y + aS.y * bS.x + aS.y * bS.y;
        return p;
    }

    vec2 df64_mul(   vec2 a,    vec2 b)
    {
        vec2 p;
        //    vec2 R;
        p = twoProd(a.x, b.x);
        p.y += a.x * b.y + a.y * b.x;
        
        p = quickTwoSum(p.x, p.y); // r

        return p;
    }

    int main(int argc, char **argv)
    {
        vec2 a =  vec2(0.0, 2000000.0);
        if(argc > 1)
        {
            a.x = atof(argv[1]);
        }
        if(argc > 2)
        {
            a.y = atof(argv[2]);
        }
        vec2 b =  vec2(0.0, 4000.0);

        vec2 result = df64_mul(a, b);
        printf("parts are (%f,%f)",result.x, result.y); 
        return 0;
    }
}
//  The code is a simple implementation of double-double precision floating point arithmetic. 
//  The code is written in C++ and I want to convert it to GLSL. 
