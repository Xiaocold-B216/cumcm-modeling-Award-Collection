function y = jiaodian2(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8)
d1=jiaodian(x1,y1,x2,y2,x3,y3,x4,y4);
d2=jiaodian(x5,y5,x6,y6,x7,y7,x8,y8);
d3=jiaodian(x1,y1,x2,y2,x7,y7,x8,y8);
d4=jiaodian(x5,y5,x6,y6,x3,y3,x4,y4);
y=jiaodian(d1(1),d1(2),d2(1),d2(2),d3(1),d3(2),d4(1),d4(2));
    
    