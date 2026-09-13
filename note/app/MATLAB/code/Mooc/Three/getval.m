n = input('请输入值：');
val1 = 1;
% 使用 for 循环
for i = 1:n
   val1 = val1*(((2*i)*(2*i))/((2*i+1)*(2*i-1)));
end


% 使用向量运算
% 建立向量
A = 1:n;
% 计算每个项
A = ((2*A).*(2*A)) ./ ((2*A+1).*(2*A-1));
val2 = prod(A);
fprintf('for 循环最终结果：%.6f\n', val1);
fprintf('向量运算最终结果：%.6f\n', val2);