function [plaza,buspla, v, time, departurescount, departurestime] = clear_boundary(plaza, buspla,v, time)
%
% clear_boundary  remove the cars of the exit cell
%
% USAGE: [plaza, v, time, departurescount, departurestime] = clear_boundary(plaza, v, time)
%        plaza = plaza matrix
%                1 = car, 0 = empty, -1 = forbid, -3 = empty&booth
%        v = velocity matrix
%        time = time matrix, to trace the time that the car cost to pass the plaza.
%
% zhou lvwen: zhou.lv.wen@gmail.com

departurescount = 0;
departurestime = [];
[a,b] = size(plaza);
for i = 2:b-1
    if plaza(a,i) > 0
        departurescount = departurescount + 1;
        departurestime(departurescount) = time(a,i);
        buspla(a-1,i)=0;
        buspla(a,i)=0;
        plaza(a,i) = 0;
        v(a,i) = 0;
        v(a-1,i)=0;
        time(a,i) = 0;
    end
end
