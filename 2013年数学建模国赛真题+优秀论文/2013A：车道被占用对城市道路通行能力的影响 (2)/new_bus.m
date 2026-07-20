function [plaza, v,buspla] = new_bus(plaza, v, vmax, iteration,buspla)
newbusmerge=[4	5	60	182	304	425	536	585	598	662	667	941	1016 1080 1137 1147];
newbuslane=[2	2	2	2	2	2	3	2	2	3	2	2	2	3	2	2];
flag=find(newbusmerge==iteration);
if flag~=0
    for i=1:length(flag)
        plaza(1,newbuslane(flag(i))+1)=1;
        plaza(2,newbuslane(flag(i))+1)=1;
        buspla(1,newbuslane(flag(i))+1)=2;
        buspla(2,newbuslane(flag(i))+1)=1;
    v(1,newbuslane(flag(i))+1)=vmax;
    v(2,newbuslane(flag(i))+1)=vmax;
    end
end