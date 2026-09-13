% 使用 plot3 绘制
subplot(2,1,1);
t1 = linspace(0,2*pi,200);
x1 = 3*sin(t1);
y1 = cos(t1);
z1 = 3*sin(t1)+cos(t1);
plot3(x1,y1,z1)
title('plot3 绘制');
xlabel('x 轴');
ylabel('y 轴');
zlabel('z 轴');
grid on

% 使用 fplot3 绘制
subplot(2,1,2);
x2 = @(t2)3*sin(t2);
y2 = @(t2)cos(t2);
z2 = @(t2)3*sin(t2)+cos(t2);
fplot3(x,y2,z,[0,2*pi])
title('fplot3 绘制');
xlabel('x 轴');
ylabel('y 轴');
zlabel('z 轴');
grid on