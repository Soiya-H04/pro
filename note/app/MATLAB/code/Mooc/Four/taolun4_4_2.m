x1 = @(t)3*sin(t);
y2 = @(t)cos(t);
z2 = @(t)3*sin(t)+cos(t);
fplot3(x1,y2,z2,[0,2*pi],'ob--')
title('plot3 绘制1');
xlabel('x 轴');
ylabel('y 轴');
zlabel('z 轴');
hold on
x2 = @(t)cos(t);
y2 = @(t)3*sin(t)+cos(t);
z2 = @(t)3*sin(t);
fplot3(x2,y2,z2,[0,2*pi],'pr-.')
title('fplot3 绘制2');
xlabel('x 轴');
ylabel('y 轴');
zlabel('z 轴');
grid on