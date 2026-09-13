t = 0:pi/20:2*pi;
r = sin(t) .* cos(t);
figure;
polar(t, r, 'b-');
hold on;
polar(t, r, 'ro');