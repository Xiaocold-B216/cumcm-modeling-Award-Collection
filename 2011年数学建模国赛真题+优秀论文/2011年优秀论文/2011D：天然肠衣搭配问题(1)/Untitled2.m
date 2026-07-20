clear
clc
Y=dlmread('f:/shuju.txt');
Y=reshape(Y,14,8);Y=Y'
Yx=floor(Y);
Ys=ceil(Y);
a=3:0.5:6.5;
 %a=7:0.5:13.5;
%a=14:0.5:25.5;
[m1 n1]=size(Y); 
kk=1;
for i=1:n1
    sx=Yx(:,i);
    ss=Ys(:,i);
    t=find(sx>0);
    p=[sx(t) ss(t)];p=reshape(p',1,2*length(t));
    pp=combntns(p,length(t));
    for j=1:length(pp)
        z=zeros(m1,1);
        z(t)=pp(j,:);
        if ismember(sum(z(t)),[19 20])&&ismember(a*z,[88.5 89 89.5])
            a*z
        Z(:,kk)=z';
        kk=kk+1;
        end
    end
end
dlmwrite('f:/z.txt',Z);
size(Z)

x=dlmread('f:/x.txt');
xlswrite('f:/x.xls',x)
xlswrite('f:/z.xls',Z)

        

