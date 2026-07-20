function [plaza, v, time,buspla] = move_forward(plaza, v, time, vmax,buspla)
% 
% move_forward   car move forward governed by NS algorithm:
%
% 1. Acceleration. If the vehicle can speed up without hitting the speed limit
% vmax it will add one to its velocity, vn -> vn + 1. Otherwise, the vehicle 
% has constant speed, vn -> vn .
%
% 2. Collision prevention. If the distance between the vehicle and the car ahead
% of it, dn , is less than or equal to vn , i.e. the nth vehicle will collide
% if it doesnâ€™t slow down, then vn -> dn âˆ?1.
%
% 3. Random slowing. Vehicles often slow for non-traffic reasons (cell phones,
% coffee mugs, even laptops) and drivers occasionally make irrational choices.
% With some probability pbrake , vn -> vn âˆ?1, presuming vn > 0.
%
% 4. Vehicle movement. The vehicles are deterministically moved by their velocities, 
% xn -> xn + vn.
%
% USAGE: [plaza, v, time] = move_forward(plaza, v, time, vmax)
%        plaza = plaza matrix
%                1 = car, 0 = empty, -1 = forbid, -3 = empty&booth
%        v = velocity matrix
%        time = time matrix, to trace the time that the car cost to pass the plaza.
%        vmax = max speed of car
%
% zhou lvwen: zhou.lv.wen@gmail.com

Service = 0.8; % Service rate
dt = 0.2; % time step

% Prob acceleration
probac = 0.7;
% Prob deceleration
probdc = 1;
% Prob of random deceleration
probrd = 0.3;
t_h = 1; % time factor

[L,W] = size(plaza);
%bus
% b=find(plaza==-3);
% bf=b(find(plaza(b-1)==-3));
% for i=2:length(bf)
%     if bf(i)-bf(i-1)==1
%         for k=i:length(bf)-1
%             bf(k)=bf(k+1);
%         end
%     end
% % end
% bb=bf-1;
    
% for i=1:length(bf)
% if plaza(bf(i)+1)==0
% if bf~=404&bf~=303
%    %no crushing
%    if plaza(bf(i)+1)==0
%         plaza(bf(i)+1)=-3;
%         plaza(bb(i))=0;
%         v(bf(i)+1)=v(bf(i));
%         v(bb(i)+1)=v(bb(i));
%    end
%    if plaza(bf(i)+1)~=0&&plaza((bf(i))-L)==0&&plaza((bb(i))-L)==0
%         plaza(bf(i))=0;
%         plaza(bb(i))=0;
%         plaza(bf(i)-L)=-3;
%         plaza(bb(i)-L)=-3;
%         v(bf(i))=0;
%         v(bb(i))=0;
%         v(bf(i)-L)=0;
%         v(bb(i)-L)=0;
%    elseif plaza(bf(i)-L)~=0&(plaza(bf(i)+1)==1|plaza(bf(i)+1)==-3|plaza(bf(i)+1)==-1)
%         v(bf(i))=0;
%         v(bb(i))=0;
%    end
% else
% plaza(b(bf))=0;
% plaza(b(bb))=0;
% v(b(bf))=0;
% v(b(bb))=0;
% end
% end
% end



% gap measurement for car in (i,j)
gap = zeros(L,W);
f=find(plaza==1);

for k=1:length(f)
    d = plaza(:,ceil(f(k)/(L)));
    gap(f(k)) = min(find([d(rem(f(k),L)+1:end)~=0;1]))-1;
end
gap(end,:) = 0;

% update rules for speed:
% 1 Speed up, provided room
k = find((gap(f) > v(f)*t_h) & (v(f) + 1 <= vmax) & (rand(size(f)) <= probac));
v(f(k)) = v(f(k)) + 1;
% 2 No crashing
k = find((v(f)*t_h >(gap(f))) & (rand(size(f)) <= probdc));
for i=1:length(k)
if buspla(f(k(i)))~=2&&f(k(i))~=161&&f(k(i))~=242&&f(k(i))~=343
v(f(k))=gap(f(k));
end
end
% 3 Random decel
k = find((gap(f)<1) & (rand(size(f)) <= probdc));
for i=1:length(k)
if buspla(f(k(i)))~=2
v(f(k))=max(v(f(k)) - 1,0);
end
end
k=find(buspla(f)==2);
v(f(k))=v(f(k)+1);
% k=find((41-rem(f,L))<2);
% v(f(find(plaza(k+1)~=0)))=0;
% v(f(find(plaza(k+1)==0)))=2;
% 3 Random decel
% k = find(rand(size(f)) <= probrd);
% v(f(k)) = max(v(f(k)) - 1,0);

% % Service: enter and out the booths
% booth_row = ceil(L/2);
% for i = 2:W-1
%     if (plaza(booth_row,i) ~= 1)
%         if (plaza(booth_row-1,i) == 1)
%             v(booth_row - 1 ,i) = 1;% enter into booth
%         end
%         plaza(booth_row,i) = -3;
%     else % cars pass through service with exponential rate Service
%         if (plaza(booth_row+1,i) ~= 1)&(rand > exp(-Service*dt))
%             v(booth_row,i) = 1; % out booths
%         else
%             v(booth_row,i) = 0;
%         end
%      end
% end


%3b March
for i=1:length(f)
if buspla(f(i))==0

plaza(f(i)) = 0;
plaza(f(i)+v(f(i))) = 1;

time(f(i) + v(f(i))) = time(f(i)) + 1;
time(plaza~=1) = 0;

v(f(i) + v(f(i))) = v(f(i));
v(plaza~=1)=0;
else
    if buspla(f(i))==1%³µÍ·
plaza(f(i))=0;
plaza(f(i)-1)=0;
plaza(f(i)+v(f(i)))=1;
plaza(f(i)+v(f(i))-1)=1;
buspla(f(i))=0;
buspla(f(i)-1)=0;
buspla(f(i)+v(f(i)))=1;
buspla(f(i)+v(f(i))-1)=2;
    
time(f(i) + v(f(i))) = time(f(i)) + 1;
time(f(i) + v(f(i))-1) = time(f(i)) + 1;
time(plaza~=1) = 0;

v(f(i) + v(f(i))) = v(f(i));
v(f(i) + v(f(i))-1) = v(f(i));
v(plaza~=1)=0;
    end
end
end

