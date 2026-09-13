/*

name:	 	LED 闪烁
param:		200
retval:		无
ref:		REGX52.H Delay.h
use to:		让 D3 的 LED 每 200 ms 闪烁一次。
updatetime:	2025-08-08

*/

#include <REGX52.H>
#include "Delay.h"

void main()
{
	P2 = 0xFF;
	P2_2 = 0;
	while(1)
	{
		Delay(200);
		P2_2 = ~P2_2;
	}
}