/*

name:	 		矩阵键盘密码锁
param:			
retval:			使用矩阵键盘的 S1-S10 来进行密码输入。
				使用 K1 来进行确认；使用 K2 来进行重置；使用 K3 来进行密码设置（初始密码为 123456。）：使用 K4 来进行锁死,再按下解锁。
				同时通过 LED 来进行次数限制，即输入错误一次就亮一个，如果全亮后无法再进行密码确认。
ref:			REGX52.H 
updatetime:		

*/

 #include "LCDShow.h"
 #include "LEDShow.h"
 #include "IndependentKey.h"
 #include "MatrixKey.h"
 #include "PasswdOperator.h"
 #include "Delay.h"

// 最大输入错误次数
#define MAX_ERROR 5
// 密码最大位数
#define MAX_PASSWD 6
// 宏 0
#define NONE 0
// 宏 1
#define OK 1
// 最大输入数
#define MAX_INPUT 10
// 最小输入数
#define MIN_INPUT 1


// independentkey 的状态
typedef enum{
	IKEY_NONE = 0,
	IKEY_OK,
	IKEY_RESET,
	IKEY_SET,
	IKEY_LOCK
} IKEY_STATE;

int main(void)
{
	// 原始密码数组
	unsigned char oripasswd[6] = {1,2,3,4,5,6};
	// 原始用户数组
	unsigned char userpasswd[6] = {0,0,0,0,0,0};
	// 独立按键返回值
	unsigned char independentkey = NONE;
	// 矩阵键盘返回值
	unsigned char matrixkey = NONE;
	// 当前错误次数
	unsigned char count_error = NONE;
	// 密码位数
	unsigned char count_passwd = NONE;
	// 重置密码位数
	unsigned char count_set = NONE;
	// 密码匹配成功标志
	unsigned char flag_match = NONE;
	// 密码可输入标志
	unsigned char flag_input = NONE;
	// 密码锁住标志
	unsigned char flag_locked = NONE;
	// 密码提前确认标志
	unsigned char flag_falseok = NONE;
	// 密码重置标志
	unsigned char flag_reset = NONE;
	// 密码设置标志
	unsigned char flag_set = NONE;
	
	
	// LCD 登录界面显示
	LCD_initial();
	// LED 初始化为全灭
	LED_initial();
	
	// 延时 2 s
	Delay(2000);
	
	// 当错误次数小于等于 8,可以输入密码
	while(count_error < MAX_ERROR)
	{
		// 把所有标志置 0
		flag_input = NONE;
		flag_falseok = NONE;
		flag_locked = NONE;
		flag_match = NONE;
		flag_reset = NONE;
		flag_set = NONE;
		// 首先将密码当前位数置到 1
		count_passwd = 1;
		
		// 用户密码数组清零
		passwd_reset(userpasswd);
		// 显示 LCD 未输入密码的密码输入界面
		LCD_input(NONE);
		// 开始进行密码输入
		while(count_passwd <= MAX_PASSWD)
		{
			// 获得当前 independentkey
			independentkey = independentkey_get();
			// 检测独立按键值
			switch(independentkey)
			{
				// 输入密码
				case IKEY_NONE:
					flag_input = OK;
					break;
				// 提前确认密码
				case IKEY_OK:
					// 密码提前确认报错标志置 1
					flag_falseok = OK;
					break;
				// 重置密码
				case IKEY_RESET:
					// 密码重置标志置 1
					flag_reset = OK;
					break;
				// 设置密码
				case IKEY_SET:
					// 密码设置标志置 1
					flag_set = OK;
					break;
				// 锁住密码
				case IKEY_LOCK:
					// 密码锁住标志置 1,除锁住按键其余按键均无效
					flag_locked = OK;
					break;
			}
			// 对于不同的标志做出相对反应
			// 密码可输入
			if (flag_input)
			{
				// 获得当前 matrixkey
				matrixkey = matrixkey_get();
				// matrixkey 有效范围位 1-10
				if (matrixkey >= MIN_INPUT && matrixkey <= MAX_INPUT)
				{
					// 将 matrixkey 输入到当前位的用户密码数组中
					passwd_input(userpasswd, count_passwd-1, matrixkey);
					// LCD 显示当前位已被输入
					LCD_input(count_passwd);
					// 将位数移动到下一位
					count_passwd++;
				}
				// 标志重置
				flag_input = NONE;
			}
			// 密码提前确认
			if (flag_falseok)
			{
				// LCD 显示密码提前确认错误
				LCD_error1();
				// 错误次数+1
				count_error++;
				// LED 亮起相应的灯数
				LED_error(count_error);
				// 标志重置
				flag_falseok = NONE;
				// 停留 2s
				Delay(2000);
				// 退出本次输入
				break;
			}
			// 密码重置
			if (flag_reset)
			{
				// 标志重置
				flag_reset = NONE;
				// 直接退出本次输入就行
				break;
			}
			// 密码锁住
			if (flag_locked)
			{
				// LCD 显示锁住界面
				LCD_locked();
				// 当一直锁住时
				while(flag_locked)
				{
					// 只用再次按下才能解开
					if (independentkey_get() == IKEY_LOCK)
					{
						// 显示 LCD 解开界面
						LCD_unlocked();
						// 延迟 2s
						Delay(2000);
						// 重置标志
						flag_locked = NONE;
						// 回到刚刚的密码输入界面,由于在上次的密码输入后现在的密码位数会多 1
						LCD_input(count_passwd-1);
						break;
					}
				}
			}
			if (flag_set)
			{
				// 重置标志
				flag_set = NONE;
				// 重置错误次数与密码位数
				count_error = 0;
				count_passwd = 1;
				// 重置用户数组用以验证
				passwd_reset(userpasswd);
				// 进行密码设置
				// 进行旧密码输入，旧密码输入正确再进行密码设置
				while(1)
				{
					// 旧密码初始位数
					count_set = 1;
					// 显示旧密码验证初始界面
					LCD_oldpasswd_set(count_set-1);
					while(count_set <= MAX_PASSWD)
					{
						// 密码输入
						matrixkey = matrixkey_get();
						if (matrixkey >= MIN_INPUT && matrixkey <= MAX_INPUT)
						{
							LCD_oldpasswd_set(count_set);
							userpasswd[count_set-1] = matrixkey;
							count_set++;
						}
					}
					// 密码匹配成功，跳出旧密码输入
					if(passwd_match(oripasswd, userpasswd))
					{
						break;
					}
					// 显示旧密码错误 2 s，并重新进行旧密码输入
					else
					{
						LCD_error0();
						Delay(2000);
					}
				}
				// 进行新密码输入
				// 新密码初始位数
				count_set = 1;
				// 显示新密码验证初始界面
				LCD_newpasswd_set(count_set-1);
				while(count_set <= MAX_PASSWD)
				{
					// 密码输入
					matrixkey = matrixkey_get();
					if (matrixkey >= MIN_INPUT && matrixkey <= MAX_INPUT)
					{
						LCD_newpasswd_set(count_set);
						oripasswd[count_set-1] = matrixkey;
						count_set++;
					}
				}
				// 进行新密码验证
				while(1)
				{
					// 新密码初始位数
					count_set = 1;
					// 显示新密码验证初始界面
					LCD_newpasswd_again(count_set-1);
					while(count_set <= MAX_PASSWD)
					{
						// 密码输入
						matrixkey = matrixkey_get();
						if (matrixkey >= MIN_INPUT && matrixkey <= MAX_INPUT)
						{
							LCD_newpasswd_again(count_set);
							userpasswd[count_set-1] = matrixkey;
							count_set++;
						}
					}
					// 密码匹配成功，跳出新密码验证，显示密码设置成功两秒，并退出密码设置
					if(passwd_match(oripasswd, userpasswd))
					{
						LCD_set_OK();
						Delay(2000);
						break;
					}
					// 显示新密码错误 2 s，并重新进行新密码输入
					else
					{
						LCD_error0();
						Delay(2000);
					}
				}	
				passwd_reset(userpasswd);
				break;
			}
		}
		// 到这里有三种情况:1. 重置(不用管);2. 密码完成输入 3. 提前确认密码(不用管)
		// 密码完成输入
		if (count_passwd > MAX_PASSWD)
		{
			// 只有确认后才会进行下一步
			while(independentkey_get() != IKEY_OK)
			{
				if (independentkey_get() == IKEY_LOCK)
				{
					LCD_locked();
					while(independentkey_get() != IKEY_LOCK)
					{
						
					}
					LCD_unlocked();
					Delay(2000);
					LCD_input(count_passwd-1);
				}
			}
			// 原密码与用户输入密码进行匹配
			flag_match = passwd_match(oripasswd,userpasswd);
			// 密码匹配成功
			if (flag_match)
			{
				break;
			}
			// 匹配失败
			else
			{
				// LCD 显示密码匹配失败界面
				LCD_error0();
				// 错误次数+1
				count_error++;
				// LED 亮起相应的灯数
				LED_error(count_error);
				// 延迟 2s
				Delay(2000);
			}
		}
	}
	// 两种可能:1. 密码匹配成功;2. 密码输入错误 8 次
	// 密码匹配成功
	if (flag_match)
	{
		// 重置标志
		flag_match = NONE;
		// LCD 显示密码匹配成功界面
		LCD_right();
		// LED 显示密码匹配成功
		LED_initial();
		while(OK)
		{
			
		}
	}
	// 密码输入错误 8 次
	if (count_error == MAX_ERROR)
	{
		// LCD 显示锁死界面
		LCD_down();
		while(OK)
		{
			
		}
	}
	return 0;
}