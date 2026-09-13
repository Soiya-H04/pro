x = [1:0.01:2];
y=cos(tan(x));
subplot(2,1,1);
plot(x,y,'b--');
f =@(x) cos(tan(x));
subplot(2,1,2);
fplot(f,[1,2],'b--o')