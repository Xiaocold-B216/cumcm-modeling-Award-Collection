function [time,plaza] = carblock(time,plaza,sf)
if plaza(122)~=1
if sf==1 
    plaza(122)=-1;
    time=5;
elseif time<3
    plaza(122)=0;
else
    time=time-1;
end
end