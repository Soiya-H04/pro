% 使用 plot
% 1. 
X1 = -5:0.1:5;
Y1 = 1/(2*pi)*exp(-(X.^2)./2);
subplot(2,2,1);
plot(X1,Y1);
% 2.
t = -1:0.1:1;
X2 = t.^2;
Y2 = 5*t.^3;
subplot(2,2,3);
plot(X2,Y2);

% 使用 fplot
% 1.
f1 = @(x)1/(2*pi)*exp(-(x.^2)./2);
subplot(2,2,2);
fplot(f1,[-5 5]);

% 2.
f2 = @(t)t.^2;
f3 = @(t)5*t.^3;
subplot(2,2,4);
fplot(f2,f3,[-1 1]);