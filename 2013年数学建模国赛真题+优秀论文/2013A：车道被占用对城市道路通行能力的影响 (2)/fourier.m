T=[1:10:400]';
influx=[2	4	5	3	0	...
    0	1	2	4	3	2	...
    0	4	1	10	2	0	...
    0	1	3	4	2	0	...
    0	2	3	3	5	6	...
    0	1	5	5	6	1	...
    0	0	3	4	7]';
omega=2*pi/24;  %all fourier coefficients
fc=zeros(40,8);fs=zeros(40,8);
for n=1:8
    fc(:,n)=cos(n*omega*T);
    fs(:,n)=sin(n*omega*T);
end
[B,BINT,R]=regress(influx,[ones(40,1),fc,fs],0.05);
t=1:10:3600;
a0=B(1);a=B(2:9);b=B(10:end);
inrate=a0;
for n=1:8
    inrate=inrate+a(n)*cos(n*t.*omega)+b(n)*sin(n*t.*omega);
end
inrate1=a0;
for n=1:8
    inrate1=inrate1+a(n)*cos(n*T.*omega)+b(n)*sin(n*T.*omega);
end
inrate=inrate./10;
influx=influx./10;
inrate1=inrate1./10;
plot(T,influx,'r')
hold on
plot(T,inrate1,'b')

total=trapz(t,inrate);
rate=total/1500;
new_influx=ceil(influx/rate);
