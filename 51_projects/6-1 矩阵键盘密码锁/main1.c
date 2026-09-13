/*

name:	 		密码锁
ref:			
use to:			
updatetime:		2025-08-09

*/

#include "LCDShow.h"
#include "LEDShow.h"
#include "IndependentKey.h"
#include "MatrixKey.h"
#include "PasswdOperator.h"
#include "Delay.h"

void main()
{
	// 开始进行初始化
	// LCD LCD 初始化
	LED_init();
	LCD_init();
	
	// 初始化正确密码数组与用户数组
	unsigned char oripasswd[6] = {1,2,3,4,5,6};
	unsigned char userpasswd[6] = {0,0,0,0,0,0};
	
	
	// 初始化错误次数
	unsigned char count_error = 0;
	
	Delay(2000);
	// 初始化完成
	while(count_error < 8)
	{
		// 进入密码输入界面(未输入状态)
		LCD_input_show(0);
		// 重置用户密码数组
		passwd_reset(userpasswd);
		// 密码正确标志
		unsigned char flag_match = 0;
		// 提前确认检测标志
		unsigned char flag_handin_false = 0;
		// 重置密码检测标志
		unsigned char flag_reset = 0;
		// 密码锁住检测标志
		unsigned char flag_locked = 0;
		// 设置当前位数位 1,开始进入第一位密码的输入
		unsigned char count_passwd = 1;
		unsigned char flag_down = 0;
		// 进行第 1 到第 6 位的输入
		while (count_passwd <= 6)
		{
			
			// 检测 independentkey
			independentkey = independentkey_get();
			switch(independentkey)
			{
				// 密码输入模式
				case 0:
					// 检测 matrixkey
					matrixkey = matrixkey_get();
					// matrixkey 的有效范围 1-10
					if (matrixkey <= 10 && matrixkey >= 1)
					{
						// 输入到用户密码数组的当前位
						passwd_input(userpasswd,count_passwd - 1,matrixkey);
						// LCD 显示已输入该位
						LCD_input_show(count_passwd);
						// 进入下一位
						count_passwd++;
					}
					break;
				// 密码提前确认
				// 因为在这时还是 1-5 位的输入,输入第 6 位后会退出本次密码输入,所以在这时按下确认是错误的
				case 1:
					// 提前确认检测标志置 1
					flag_handin_false = 1;
					break;
				// 密码重置
				case 2:
					// 重置密码检测标志置 1
					flag_reset = 1;
					break;
				// 密码设置
				case 3:
					break;
				// 密码锁住
				case 4:
					flag_locked = 1;
					LCD_locked();
					while(flag_locked)
					{
						independentkey = independentkey_get();
						if (independentkey == 4)
						{
							flag_locked = 0;
							LCD_unlocked();
							Delay(2000);
						}
					}
					break;
				// 确保无其他状态
				default:break;
			}
			// 在这里检测一下是否提前确认
			if(flag_handin_false)
			{
				// LCD 显示位数不足的错误
				LCD_error1_show();
				// 错误次数 + 1
				count_error++;
				// LED 亮一盏灯
				LED_error_show(count_error);
				// 退出本次密码输入
				Delay(2000);
				break;
			}
			if (flag_reset)
			{
				break;
			}
		}
		// 检测是否密码完全输入
		if (count_passwd == 7)
		{
			// 密码正确
			if (passwd_match(oripasswd,userpasswd))
			{
				// 密码正确标志置 1
				flag_match = 1;
				// 退出错误次数检测
				break;
			}
			// 密码不正确
			else
			{
				// LCD 显示密码不正确页面
				LCD_error0_show();
				// 错误次数 + 1
				count_error++;
				// LED 更新状态
				LED_error_show(count_error);
				// 持续两秒
				Delay(2000);
			}
		}
	}
	// 退出错误次数检测,有两种情况:1. 密码正确需要进行密码匹配 2. 密码 8 次输错
	// 密码输入完全,进行密码匹配
	if(flag_match)
	{
		// LCD 显示正确界面
		LCD_right_show();
		while(1)
		{
		// LED 持续执行流水灯
		LED_right_show();
		}

	}
	// 密码 8 次错误,锁死(防止出现两种情况)
	else if (count_error == 8)
	{
		// 锁死标志置 1
		flag_down = 1;
		// 显示锁死界面
		LCD_down();
		// 锁死在这里
		while(1)
		{
			
		}
	}
}