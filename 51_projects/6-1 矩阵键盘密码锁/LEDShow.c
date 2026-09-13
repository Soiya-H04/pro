/*

name:		 	LEDShow.c
ref:			REGX52.H
use to:			使用 LED 对输入错误与正确进行表示。
updatetime:		2025-08-09

*/

#include <REGX52.H>
#include "Delay.h"

/*

function name:		LEDInit
param:				none
retval:				none
description:		LED 初始化及重置。
updatetime:			2025-08-10

*/

void LED_initial()
{
	P2 = 0xFF;
}

/*

function name:		LEDshow_error
param:				num_error
retval:				none
description:		密码每错一次，LED 就从 D1 到 D8 依次亮起。
updatetime:			2025-08-10

*/

void LED_error(unsigned char num_error)
{
	if(num_error == 1)
	{
		P2_0 = 0;
	}
	else
	{
		P2 = P2 << 1;
	}
}

/*

function name:		LEDshow_right
param:				无
retval:				无
description:		密码正确时，LED 的行为。
updatetime:			2025-08-10

*/

void LED_right()
{
	P2 = 0xF8;
	Delay(500);
	if(P2_7 == 1)
	{
		P2 = (P2 << 1) | 0x01;
	}
	else
	{
		P2 = P2 << 1;
	}
}