h=2*pi/100;                    
t=0:h:2*pi;r=0:0.05:1;
x=r'*cos(t);
y=r'*sin(t);
y(find(y>=0))=NaN;
z=sqrt(1-x.^2);
meshz(x,y,z); 