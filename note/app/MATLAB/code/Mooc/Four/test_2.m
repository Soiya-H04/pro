% plot3
u = 0:0.1:pi;
v = 0:0.1:pi;
X1 = (1+cos(u)).*cos(v);
Y1 = (1+cos(u)).*sin(v);
Z1 = sin(u);
subplot(2,2,1);
plot3(X1,Y1,Z1);

% mesh
[U V] = meshgrid(u,v);
X2 = (1+cos(U)).*cos(V);
Y2 = (1+cos(U)).*sin(V);
Z2 = sin(U);
subplot(2,2,3);
mesh(X2,Y2,Z2);

% surf 
[U V] = meshgrid(u,v);
X3 = (1+cos(U)).*cos(V);
Y3 = (1+cos(U)).*sin(V);
Z3 = sin(U);
subplot(2,2,4);
surf(X3,Y3,Z3);
