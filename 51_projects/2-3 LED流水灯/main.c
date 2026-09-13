/*

name:	 	LED 流水线亮
param:		500
retval:		无
ref:		REGX52.H Delay.h
use to:		每次亮两个，由 D1 与 D4 开始向右移动，每 500 ms 移动一次。
updatetime:	2025-08-08

*/

#include <REGX52.H>
#include "Delay.h"

void main()
{
	// 先初始化 LED
	P2 = 0xFF;
	P2_0 = 0;
	P2_3 = 0;
	while(1)
	{
		// 由于右移不会将 1 移动到左边，所以要加判断。
		if(1 == P2_7)
		{
			Delay(500);
			// D8 << D1
			// P2 << 1
			P2 = P2 << 1;
			P2_0 = 1;
		}
		else
		{
			Delay(500);
			P2 = P2 << 1;
		}
	}
}