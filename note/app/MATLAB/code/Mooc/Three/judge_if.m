score = input('请输入成绩：');
while score > 100 || score < 0
    score = input('输入错误，请重新输入：');
end
if score >= 90
    disp('A');
elseif score >= 80
    disp('B');
elseif score >= 70
    disp('C');
elseif score >= 60
    disp('D');
else
    disp('E')
end