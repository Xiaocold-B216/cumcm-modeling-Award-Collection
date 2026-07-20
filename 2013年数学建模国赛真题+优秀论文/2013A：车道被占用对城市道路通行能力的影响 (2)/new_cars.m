function [plaza, v, number_cars] = new_cars(Arrival, dt, plaza, v, vmax, iteration)
%
% new_cars   introduce new cars. Cars arrive at the toll plaza uniformly in
% time (the interarrival distribution is exponential with rate Arrival?). 
% "rush hour" phenomena can be consider by varying the arrival rate.
%
% USAGE: [plaza, v, number_cars] = new_cars(Arrival, dt, plaza, v, vmax)
%        Arrival = the mean total number of cars that arrives 
%        dt = time step
%        plaza = plaza matrix
%                1 = car, 0 = empty, -1 = forbid, -3 = empty&booth
%        v = velocity matrix
%        vmax = max speed of car
%
% zhou lvwen: zhou.lv.wen@gmail.com

% Find the empty lanes of the entrance where a new car can be add.
unoccupied = find(plaza(1,:) == 0);
n = length(unoccupied); % number of available lanes
% The number of vehicles must be integer and not exceeding the number of
% available lanes
number_cars =min( poissrnd(Arrival*dt,1), n);
% if number_cars > 0 
%     x = randperm(n);
%     for i = 1:number_cars
%          plaza(1, unoccupied(x(i))) = 1;
%          v(1, unoccupied(i)) = vmax;
%     end
% end
newcarmerge=[2	5	14	30	30	40	42	45	46	50	51	51	52	54	60	61	91	102	106	110	111	112	116	118	118	123	132	133	148	152	153	158	162	169	170	171	172	173	173	174	175	178	178	181	216	221	221	225	232	232	234	238	239	240	269	272	286	288	288	290	291	295	296	299	299	300	303	308	310	310	313	318	318	336	343	343	346	346	348	352	352	355	358	358	359	361	361	363	366	366	374	399	403	408	409	409	412	414	419	421	421	423	425	426	426	458	462	465	467	469	472	472	472	473	477	477	477	477	478	483	483	483	483	487	521	524	524	527	527	531	531	532	536	538	538	541	541	545	545	545	545	548	552	563	564	565	579	584	585	586	589	589	592	593	594	595	595	595	605	605	609	624	639	639	639	641	641	644	645	645	647	649	649	655	659	665	667	670	673	673	693	701	701	701	704	704	707	707	707	708	708	712	712	712	712	761	765	769	769	777	777	781	784	784	786	941	944	946	996	1004	1004	1010	1012	1014	1014	1016	1033	1135	1137	1137	1199	1143	1143	1143	1144];
mergelane=[3 3	3	2	3	2	2	2	3	2	2	3	2	2	3	2	1	3	3	2	3	3	2	2	3	3	1	2	2	2	3	3	2	2	3	2	3	2	3	2	1	2	3	2	2	2	3	2	3	3	2	1	1	3	2	2	2	2	3	2	3	2	2	2	3	3	3	2	2	3	1	2	3	1	3	2	2	3	3	2	2	3	2	1	2	2	3	3	2	3	2	2	2	2	2	3	3	2	3	3	3	3	2	1	1	1	3	2	3	2	2	2	3	3	2	2	2	3	3	1	2	2	3	1	3	2	3	2	3	2	2	2	2	2	3	2	2	2	2	1	3	3	1	1	2	2	3	3	3	3	2	3	2	2	2	3	1	2	3	2	2	2	3	1	2	2	1	2	3	2	2	3	2	2	2	2	2	2	2	1	2	2	2	3	2	3	2	2	3	3	2	2	3	2	3	2	3	1	2	1	2	3	1	2	2	2	3	3	2	2	3	2	3	2	2	3	2	3	3	2	3	3	2	3	1];
flag=find(newcarmerge==iteration);
if flag~=0
    for i=1:length(flag)
        plaza(1,mergelane(flag(i))+1)=1;
    v(1,mergelane(flag(i))+1)=vmax;
    end
%     end
%     else
%         if r<0.6 && plaza(2,3)==0 && plaza(1,3)==0
%             plaza(2,3)=-3;
%             plaza(1,3)=-3;
%             v(2,3)=vmax;
%             v(1,3)=vmax;
%         elseif plaza(2,4)==0 && plaza(1,4)==0
%             plaza(2,4)=-3;
%             plaza(1,4)=-3;
%             v(2,4)=vmax;
%             v(1,4)=vmax;
%         end
  
end


