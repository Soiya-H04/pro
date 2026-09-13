/*

name:	 		LCDShow.c
ref:			LCD1602.h REGX52.H
use to:			使用 LCD 显示相关信息。
updatetime:		2025-08-08

*/

#include "LCD1602.h"

/*

function name:		LCD_init
param:				none
retval:				none
description:		LCD 屏的初始化
updatetime:			2025-08-08

*/
void LCD_initial()
{
	LCD_Init();
	LCD_ShowString(1,1,"Welcome Home!");
	LCD_ShowString(2,1,"My Friend.");
}

/*

function name:		LCD_input_show
param:				index
retval:				none
description:		用 * 显示密码输入
updatetime:			2025-08-08

*/

void LCD_input(unsigned char index)
{
	unsigned char i = 1;
	LCD_Init();
	LCD_ShowString(1,1,"Passwd:");
	for (i;i <= index;i++)
	{
		LCD_ShowChar(2,i,'*');
	}
}

/*

function name:		LCD_right_show
param:				none
retval:				none
description:		密码输入正确以后的显示
updatetime:			2025-08-08

*/

void LCD_right()
{
	LCD_Init();
	LCD_ShowString(1,1,"Right!");
	LCD_ShowString(2,1,"Please Come In.");
}

/*

function name:		LCD_error0_show
param:				none
retval:				1
description:		密码输入错误的显示，返回 1
updatetime:			2025-08-08

*/

void LCD_error0()
{
	LCD_Init();
	LCD_ShowString(1,1,"error:");
	LCD_ShowString(2,1,"Passwd is wrong.");
}

/*

function name:		LCD_error1_show
param:				none
retval:				1
description:		密码输入位数不足的显示，返回 1
updatetime:			2025-08-08

*/

void LCD_error1()
{
	LCD_Init();
	LCD_ShowString(1,1,"error:");
	LCD_ShowString(2,1,"count is wrong.");
}

/*

function name:		LCD_oldpasswd_set_show
param:				passwd_index
retval:				none
description:		设置密码时，显示占位的 *
updatetime:			2025-08-09	

*/

void LCD_oldpasswd_set(unsigned char passwd_index)
{
	unsigned char i = 1;
	LCD_Init();
	LCD_ShowString(1,1,"Set passwd");
	LCD_ShowString(2,1,"Old:");
	for(i;i <= passwd_index;i++)
	{
		LCD_ShowChar(2,i+4,'*');
	}
}

/*

function name:		LCD_newpasswd_set_show
param:				passwd_index
retval:				none
description:		设置密码时，显示占位的 *
updatetime:			2025-08-09	

*/

void LCD_newpasswd_set(unsigned char passwd_index)
{
	unsigned char i = 1;
	LCD_Init();
	LCD_ShowString(1,1,"Set passwd");
	LCD_ShowString(2,1,"New:");
	for(i;i <= passwd_index;i++)
	{
		LCD_ShowChar(2,i+4,'*');
	}
}

/*

function name:		LCD_newpasswd_again
param:				passwd_index
retval:				none
description:		设置密码时，显示占位的 *
updatetime:			2025-08-09	

*/

void LCD_newpasswd_again(unsigned char passwd_index)
{
	unsigned char i = 1;
	LCD_Init();
	LCD_ShowString(1,1,"Set passwd");
	LCD_ShowString(2,1,"Again:");
	
	for(i;i <= passwd_index;i++)
	{
		LCD_ShowChar(2,i+6,'*');
	}
}

/*

function name:		LCD_set_OK
param:				none
retval:				none
description:		设置密码时，显示占位的 *
updatetime:			2025-08-09	

*/

void LCD_set_OK()
{
	LCD_Init();
	LCD_ShowString(1,1,"Set passwd");
	LCD_ShowString(2,1,"Successfully set");
}


/*

function name:		LCD_locked
param:				none
retval:				none
description:		将密码输入锁住。
updatetime:			2025-08-10

*/

void LCD_locked()
{
	LCD_Init();
	LCD_ShowString(1,1,"State:");
	LCD_ShowString(2,1,"Locked.");
}


/*

function name:		LCD_unlocked
param:				none
retval:				none
description:		解锁密码输入
updatetime:			2025-08-10

*/

void LCD_unlocked()
{
	LCD_Init();
	LCD_ShowString(1,1,"State:");
	LCD_ShowString(2,1,"Unlocked.");
}

/*

function name:		LCD_down
param:				none`
retval:				none`
description:		当密码输入超过八次错误，密码锁锁死，无法进行任何操作。
updatetime:			2025-08-10

*/

void LCD_down()
{
	LCD_Init();
	LCD_ShowString(1,1,"No chance!");
	LCD_ShowString(2,1,"Try another day.");
}