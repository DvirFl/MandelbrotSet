#include "glm/detail/type_vec.hpp"
#include "glm/glm.hpp"
#include <stdio.h>

namespace glm {


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
     vec2 aS = Split32(a);
     vec2 bS = Split32(b);
    p.x = aS.x * bS.y + aS.y * bS.x + aS.x * bS.x;
    
    p.y = (aS.x * bS.x - p.x) + aS.x * bS.y + aS.y * bS.x + aS.y * bS.y;
    return p;
}

   vec2 df64_mul(   vec2 a,    vec2 b)
{
       vec2 p;
        vec2 R = twoProd(a.x, b.x);

    p.y =R.y + a.x * b.y + a.y * b.x;
    p.x = R.x;
    printf(" R parts are (%f,%f)",R.x, R.y);  
    p = quickTwoSum(p.x, p.y); // r
    printf(" r parts are (%f,%f)",p.x, p.y);  

    return p;
}
}
int main(int argc, char **argv)
{
    float f1 = 5.0, f2 = 6.0;
    glm::vec2 t =  glm::twoProd(f1, f2);
    printf(" t parts are (%f,%f)\n\n",t.x, t.y);  

    glm::vec2 a =  glm::vec2(1.0, 200000.0);
    if(argc > 1)
    {
        a.x = atof(argv[1]);
    }
    if(argc > 2)
    {
        a.y = atof(argv[2]);
    }
    glm::vec2 b =  glm::vec2(3.0, 400000.0);

    glm::vec2 result = df64_mul(a, b);
    printf("parts are (%f,%f)",result.x, result.y); 
    return 0;
}

//  The code is a simple implementation of double-double precision floating point arithmetic. 
//  The code is written in C++ and I want to convert it to GLSL. 
