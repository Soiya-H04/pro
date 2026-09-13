score = input('请输入成绩：');
while score > 100 || score < 0
    score = input('输入错误，请重新输入：');
end
switch fix(score/10)
    case {10,9}
        disp('A')
    case 8
        disp('B')
    case 7
        disp('C')
    case 6
        disp('D')
    otherwise
        disp('E')
end
