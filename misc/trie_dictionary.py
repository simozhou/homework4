def pos_sicura(a,b,c,d):
    x = (a & (~b))|((~a) & b)
    y = (c & (~d))|((~c) & d)
    z = (x & (~y))|((~x) & y)
    return z

