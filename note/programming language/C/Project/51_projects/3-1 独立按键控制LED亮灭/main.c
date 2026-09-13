/*

name:	 	独立按键控制 LED 亮灭
param:		20
retval:		无
ref:		REGX52.H Delay.h
use to:		K1 按下，所有 LED 亮；k2 按下，所有 LED 灭；K3 按下，只亮 D1。
updatetime:	2025-08-08

*/

#include <REGX52.H>
#include "Delay.h"

void main()
{
	// LED 初始化
	P2 = 0xFF;
	while(1)
	{
		// 防抖操作，且直到松开才操作。
		if (0 == P3_1){Delay(20);while(0 == P3_1);Delay(20);P2 = 0x00;}
		if (0 == P3_0){Delay(20);while(0 == P3_0);Delay(20);P2 = 0xFF;}
		if (0 == P3_2){Delay(20);while(0 == P3_2);Delay(20);P2 = 0xFF;P2_0 = 0;}
	}
}