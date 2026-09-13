x = 0:0.05:2*pi;
y = @(x,a) cos(a*x).^3 + sin(x).^3;

figure;
plot(x, y(x,0.1), 'or--'); 
hold on;
plot(x, y(x,1), 'sb-.');
plot(x, y(x,2), '^g:'); 
hold off;

title('$y(x,a) = \cos(ax)^3 + \sin(x)^3$', 'Interpreter', 'latex');
xlabel('x');
ylabel('y');
legend('a=0.1', 'a=1', 'a=2');
grid on;