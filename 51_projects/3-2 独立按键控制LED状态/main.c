/*

name:	 	独立按键控制 LED 状态
param:		20 200
retval:		无
ref:		REGX52.H Delay.h
use to:		开始 D1 一个 LED 亮。K1 按下后，LED 向左移动；K2 按下后，LED 不移动；K3 按下后， LED 向右移动；K4 按下后，LED 重置。
			在 Delay 时按键，不会有响应，在后面的定时器里可以解决这个问题。
updatetime:	2025-08-08

*/

#include <REGX52.H>
#include "Delay.h"

void main()
{
	unsigned int state = 0;
	P2 = 0xFF;
	P2_0 = 0;
	while(1)
	{
		if (0  == P3_1){Delay(20);while(0 == P3_1);Delay(20);state = 1;}
		if (0  == P3_0){Delay(20);while(0 == P3_0);Delay(20);state = 2;}
		if (0  == P3_2){Delay(20);while(0 == P3_2);Delay(20);state = 3;}
		if (0  == P3_3){Delay(20);while(0 == P3_3);Delay(20);state = 4;}
		switch (state)
		{
		case 1:	// 左移（板）
			Delay(200);
			if (P2_0 == 1)
			{
				// 右移补 1，>> 与 << 的优先级低于 |
				P2 = (P2 >> 1) | 0X80;
			}
			else
			{
				P2 = P2 >> 1;
			}
			break;
		case 2:	// 暂停
			break;
		case 3:	// 右移(板)
			Delay(200);
			if (P2_7 == 1)
			{
				P2 = (P2 << 1) | 0x01;
			}
			else
			{
				P2 = P2 << 1;
			}
			break;
		case 4:	// 重置
			P2 = 0xFF;
			P2_0 = 0;
			break;
		default:break;
		}
	}
}