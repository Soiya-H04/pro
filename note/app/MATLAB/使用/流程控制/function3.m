function f = function3(n)
if n == 1
    f = 1;
else
    f = n*function3(n-1);
end