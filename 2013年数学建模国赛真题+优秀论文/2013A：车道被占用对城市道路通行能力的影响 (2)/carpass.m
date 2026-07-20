function [flag,plaza] = carpass(plaza,index,L,flag)
if(flag(index)==1)
plaza(index-L)=0;
flag(index)=0;
end