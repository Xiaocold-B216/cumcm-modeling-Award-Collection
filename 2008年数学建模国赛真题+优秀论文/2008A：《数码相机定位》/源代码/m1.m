format long
P=imread('picture.bmp');
lefttop=[100 240
         142 244
         170 258
         450 545
         471 543];
rightbutton=[200 368
             375 466
             591 685
             200 330
             537 624];
         
for circle=1:5
    circle
    if(circle~=1)
        clear u;
        clear v;
    end
    k=1;
    for i=lefttop(circle,1):lefttop(circle,2)
        flag=0;
        for j=rightbutton(circle,1):rightbutton(circle,2)
            if flag==0 & P(i,j)<10
                u(k)=i;
                v(k)=j;
                k=k+1;
                flag=1;
            elseif flag==1 & P(i,j)<10 & P(i,j+1)>200
                u(k)=i;
                v(k)=j;
                k=k+1;
            end
        end
    end
    for j=rightbutton(circle,1):rightbutton(circle,2)
        flag=0;
        for i=lefttop(circle,1):lefttop(circle,2)
            if flag==0 & P(i,j)<10
                f1=0;
                for temp=1:k-1
                    if u(temp)==i & v(temp)==j
                        f1=1;
                    end
                end
                if f1==0
                    u(k)=i;
                    v(k)=j;
                    k=k+1;
                    flag=1;
                end
            elseif flag==1 & P(i,j)<10 & P(i+1,j)>200
                 f1=0;
                for temp=1:k-1
                    if u(temp)==i & v(temp)==j
                        f1=1;
                    end
                end
                if f1==0
                    u(k)=i;
                    v(k)=j;
                    k=k+1;
                    flag=1;
                end
            end
        end
    end
    axis equal;
    axis([1 768 1 1024]);
    
    plot(u,v,'.');grid on ;hold on;
  
    x=ones(k-1,5);
    y=ones(k-1,1);

    for i=1:k-1
        x(i,:)=[1 v(i) u(i)  u(i)*v(i)  v(i)*v(i) ];
        y(i)=-u(i)*u(i);
    end

    [b,bint,r,rint,stats]=regress(y,x);
    b
    bint
    stats
    A=[2 b(4);
       b(4) 2*b(5)];
    B=[-b(3);-b(2)];
    X=A\B
    xo=(X(2)-512)/3.78
    yo=(384-X(1))/3.78
    xlswrite(strcat('d:/',num2str(circle),'.xls'),[u;v]');
end
