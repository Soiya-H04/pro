function f = example2(n)
f = 0;
for i=1:n
    f = sum([i.*(i+1),f]);
end
