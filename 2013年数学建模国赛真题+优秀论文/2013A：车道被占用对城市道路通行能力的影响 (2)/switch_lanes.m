function [plaza, v, time,buspla,busstop,carstop,sf] =  switch_lanes(plaza, v, time,buspla,busstop,carstop,sf)
%
% switch_lanes  Merge to avoid obstacles.
%  
% The vehicle will attempt to merge if its forward path is obstructed (dn = 0). 
% The vehicle then randomly chooses an intended direction, right or left. If 
% that intended direction is blocked, the car will move in the other direction
% unless both directions are blocked (the car is surrounded). 
% 
% USAGE: [plaza, v, time] =  switch_lanes(plaza, v, time)
%        plaza = plaza matrix
%                1 = car, 0 = empty, -1 = forbid, -3 = empty&booth
%        v = velocity matrix
%        time = time matrix, to trace the time that the car cost to pass the plaza.
%
% zhou lvwen: zhou.lv.wen@gmail.com

[L, W] = size(plaza);
found = find(plaza==1);
% if ~isempty(found)
%     found = found(randperm(length(found)));
% end
sf=0;
for k=1:length(found)
  if(buspla(found(k))==0)%car
    if (plaza(found(k)+1)~=0)%前方有障碍

        if carstop(found(k))<=0   %转向前计时

            if plaza(found(k)-L) == 0 
                plaza(found(k)-L) = 1;
                plaza(found(k)) = 0;
                v(found(k)-L) = 0;
                v(found(k)) = 0;
                time(found(k)-L) = time(found(k));
                time(found(k)) = 0;
                carstop(found(k))=3;
                sf=1;
            end
        else
            carstop(found(k))=carstop(found(k))-1;%计时
        end
    end
  else%bus
        if buspla(found(k))==1%找到车头
          if plaza(found(k)+1)~=0
              if busstop(found(k)+1)<=0   %转向前计时
                if plaza(found(k)-L)==0 && plaza(found(k)-L-1)==0
                    plaza(found(k)-L) = 1;
                    plaza(found(k)-L-1) = 1;
                    plaza(found(k)) = 0;
                    plaza(found(k)-1)=0;
                    buspla(found(k)-L) = 1;
                    buspla(found(k)-L-1) = 2;
                    buspla(found(k)) = 0;
                    buspla(found(k)-1)=0;
                    v(found(k)-L) = 0;
                    v(found(k)-L-1)=0;
                    v(found(k)) = 0;
                    time(found(k)-L) = time(found(k));
                    time(found(k)-L-1)=time(found(k)-1);
                    time(found(k)) = 0;
                    time(found(k)-1)=0;
                    busstop(found(k)+1)=6;
                    sf=1;
                end
              else
                  busstop(found(k)+1)=busstop(found(k)+1)-1;
              end
          end
        end
  end
end
    



%           elseif plaza(k+L) == 0 
%                 plaza(k+L) = 1;
%                 plaza(k) = 0;
%                 v(k+L) = v(k);
%                 v(k) = 0;
%                 time(k+L) = time(k);
%                 time(k) = 0;
%          elseif plaza(k-1)==0 
%                 plaza(k-1) = 1;
%                 plaza(k) = 0;
%                 v(k-1) = v(k);
%                 v(k) = 0;
%                 time(k-1) = time(k);
%                 time(k) = 0;
             
 