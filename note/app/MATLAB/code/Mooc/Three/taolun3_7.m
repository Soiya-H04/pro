function f = taolun3_7(n)
if n == 1
    f = 1;
else
    f = n + taolun3_7(n-1);
end