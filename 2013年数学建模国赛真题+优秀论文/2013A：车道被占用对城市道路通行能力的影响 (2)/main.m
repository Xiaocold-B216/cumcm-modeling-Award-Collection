% main.m
%
% This is a main script to simulate the approach, service, and departure of 
% vehicles passing through a toll plaza, , as governed by the parameters 
% defined below
%
%   iterations      =  the maximal iterations of simulation
%   B               =  number booths
%   L               =  number lanes in highway before and after plaza
%   Arrival         =  the mean total number of cars that arrives 
%   plazalength     =  length of the plaza
%   Service         =  Service rate of booth
%   plaza           =  plaza matrix
%                      1 = car, 0 = empty, -1 = forbid, -3 = empty&booth
%   v               =  velocity matrix
%   vmax            =  max speed of car
%   time            =  time matrix, to trace the time that the car cost to
%                      pass the plaza.
%   dt              =  time step
%   t_h             =  time factor
%   departurescount =  number of cars that departure the plaza in the step
%   departurestime  =  time cost of the departure cars
%   influx          =  influx vector
%   outflux         =  outflux vector
%   timecost        =  time cost of all car
%   h               =  handle of the graphics
%   
% zhou lvwen: zhou.lv.wen@gmail.com


clear;clc
iterations = 1200; % the maximal iterations of simulation
B = 3; % number booths
L = 3; % number lanes in highway before and after plaza
Arrival=3; % the mean total number of cars that arrives 

plazalength = 81; % length of the plaza
[plaza, v, time,buspla] = create_plaza(B, L, plazalength);
h = show_plaza(plaza,buspla, NaN, 0.01);

timeblock=5;
dt = 0.2; % time step
t_h = 1; % time factor
vmax = 2; % max speed
vinit=1;%initial speed

busstop=6*ones(plazalength,B+2);
carstop=3*ones(plazalength,B+2);

timecost = [];
sf=0;%switchflag
for i = 1:iterations
    if i==14
        ss=0;
    end
    if i==370
        ss=0;
    end
    if i==490
        ss=0;
    end
    if i==550
        ss=0;
    end
    if i==602
        ss=0;
    end
    if i==711
        ss=0;
    end
    % introduce new cars
    [plaza, v, arrivalscount] = new_cars(Arrival, dt, plaza, v, vinit,i);
    [plaza, v, buspla] = new_bus(plaza, v, vinit, i,buspla);
    
    h = show_plaza(plaza,buspla, h, 0.02);

    [timeblock,plaza] = carblock(timeblock,plaza,sf);%转向导致堵车
    % update rules for lanes
    r=rand();
    if(r<0.3)
    [plaza, v, time,buspla,busstop,carstop,sf] = switch_lanes(plaza, v, time,buspla,busstop,carstop,sf); % lane changes
    [plaza, v, time,buspla] = move_forward(plaza, v, time, vmax,buspla); % move cars forward
    else
         [plaza, v, time,buspla] = move_forward(plaza, v, time, vmax,buspla); % move cars forward
         [plaza, v, time,buspla,busstop,carstop,sf] = switch_lanes(plaza, v, time,buspla,busstop,carstop,sf); % lane changes
    end
    [plaza,buspla, v, time, departurescount, departurestime] = clear_boundary(plaza,buspla, v, time);

    % flux calculations
    influx(i) = arrivalscount;
    outflux(i) = departurescount;
    timecost = [timecost, departurestime];
end

h = show_plaza(plaza, h, 0.01);
xlabel({strcat('B = ',num2str(B)), ...
strcat('mean cost time = ', num2str(round(mean(timecost))))})