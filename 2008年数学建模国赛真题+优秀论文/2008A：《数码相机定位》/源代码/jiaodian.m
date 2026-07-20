function y = jiaodian(m1,n1,m2,n2,m3,n3,m4,n4)
A=[n1-n2 m2-m1;
    n3-n4 m4-m3]; 
B=[(n1-n2)*m1-(m1-m2)*n1;
    (n3-n4)*m3-(m3-m4)*n3];
y=A\B;

