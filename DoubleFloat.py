import glm

  glm.vec2 quickTwoSum(   float a,    float b)
{
      glm.vec2 result;
    result.x = a + b;
    result.y = b - (result.x - a);
    return result;
}

  glm.vec2 twoProd(   float a,    float b)
{
      glm.vec2 p;
    p.x = a * b;
      glm.vec2 aS = Split64(a);
      glm.vec2 bS = Split64(b);
    p.y = (aS.x * bS.x - p.x) + aS.x * bS.y + aS.y * bS.x + aS.y * bS.y;
    return p;
}

  glm.vec2 df128_mul(  glm.vec2 a,   glm.vec2 b)
{
      glm.vec2 p;
    p = twoProd(a.x, b.x);
    p.y += a.x * b.y + a.y * b.x;
    p = quickTwoSum(p.x, p.y);

    return p;
}