/*

name:	 	独立按键控制 LED 显示二进制
param:		20
retval:		无
ref:		REGX52.H Delay.h
use to:		按下一次 K1 ，显示相应二进制的进位。
updatetime:	2025-08-08

*/

#include <REGX52.H>
#include "Delay.h"

void main()
{
	unsigned char Num = 0;
	P2 = 0xFF;
	while(1)
	{
		if (P3_1 == 0){Delay(20);while(P3_1 == 0);Delay(20);Num++;P2 = ~Num;}
	}
}