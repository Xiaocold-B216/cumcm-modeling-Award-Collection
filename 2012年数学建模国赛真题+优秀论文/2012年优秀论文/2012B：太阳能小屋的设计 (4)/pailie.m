clear;clc
a=xlsread('cumcm.xls','sheet1','B1:F24');%电池的信息
b=xlsread('cumcm.xls','sheet2','A1:M18');%逆变器的信息
P=b(:,3).*b(:,4);
pai=[];pai2=[];
for k=1:18%第k种逆变器
    for h=1:24%第h种电池
        for i=1:65
            if i*a(h,3)>b(k,5)&&i*a(h,3)<b(k,6)
                pai=[pai;k,h,i];

            end
        end
    end
end
[m,n]=size(pai);
for i=1:m
    for j=1:600
        if j*a(pai(i,2),1)*pai(i,3)<=P(pai(i,1))&&j*a(pai(i,2),4)<=b(pai(i,1),4)
            pai2=[pai2;pai(i,:),j];
            %break
        end
    end
end
