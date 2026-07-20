format long
clear;
count=1;
for t=-pi/2:0.05:pi/2
    b=t;r=0;a=0;
    L=3.78;f=1577/3.78;
    Tx=-350;Ty=0;Tz=-350;
    R1=[L*f 0 0 0;
        0 L*f 0 0;
        0 0  0 1];
    R2=[cos(b)*cos(r)   sin(a)*sin(b)*cos(r)+cos(a)*sin(r)  -cos(a)*sin(b)*cos(r)+sin(a)*sin(r)  Tx;
        -cos(b)*sin(r)  -sin(a)*sin(b)*sin(r)+cos(a)*cos(r)  cos(a)*sin(b)*sin(r)+sin(a)*cos(r)  Ty;
        sin(b)         -sin(a)*cos(b)                       cos(a)*cos(b)                     Tz;
        0                0                                    0                                1;
        ];

    M=R1*R2;
    
    k=1;
    for w=0:2*pi/200:2*pi
        X=12*cos(w);
        Y=12*sin(w);
        Zc=R2(3,1:3)*[X Y 0]'-Tz;
        u(k)=1/Zc*M(1,:)*[X Y 0 1]';
        v(k)=1/Zc*M(2,:)*[X Y 0 1]';
        k=k+1;
    end

        x=ones(k-1,5);
        y=ones(k-1,1);
     for i=1:k-1
         x(i,:)=[1 v(i) u(i)  u(i)*v(i)  v(i)*v(i) ];
         y(i)=-u(i)*u(i);
     end

    [b,bint,r,rint,stats]=regress(y,x);
    A=[2 b(4);
       b(4) 2*b(5)];
    B=[-b(3);-b(2)];
    X=A\B;
    M=M/(-Tz);
    F(count)=sqrt((X(1)-M(1,4))*(X(1)-M(1,4))+(X(2)-M(2,4))*(X(2)-M(2,4)));
    count=count+1;
end
 plot(-pi/2:0.05:pi/2,F);
 xlabel('¦Â');ylabel('D')
 grid on;