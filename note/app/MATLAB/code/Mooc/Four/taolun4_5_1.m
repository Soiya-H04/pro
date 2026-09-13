% 设定 x 为 1-10，y 为 3-8
x = 1:0.1:10;
y = (3:0.1:8)';
[X Y] = meshgrid(x,y);
Z = sin(X+sin(Y))-X./10;
mesh(X,Y,Z);
