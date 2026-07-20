clear;clc
fushe=xlsread('cumcm.xls','sheet','E4:K8763');
dianban=xlsread('cumcm.xls','sheet1','B1:F24');

P=52.5;%组件额定功率
p0=30;%最低强度，单晶硅多晶硅为80，薄膜为30
for i=1:8760
    for j=1:7
        if fushe(i,j)<p0
            fushe(i,j)=0;
        end
    end
end
%for i=1:8760
%    for j=1:7
%        if fushe(i,j)<200
%            fushe(i,j)=fushe(i,j)*0.05;
%        end
%    end
%end
Q=sum(fushe*P/1000)/1000;
shuiping=Q(1)
dong=Q(4)
nan=Q(5)
xi=Q(6)
bei=Q(7)
