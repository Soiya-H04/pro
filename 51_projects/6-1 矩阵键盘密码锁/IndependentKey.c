/*

name:	 		IndependentKey.c
ref:			REGX52.H Delay.h
use to:			检测独立按键的按下与抬起。
				如果按键按下，independentkey 返回对应位置的数字；如果按键未按下，independentkey 返回 0。
updatetime:		2025-08-10

*/

#include <REGX52.H>
#include "Delay.h"

unsigned char independentkey_get()
{
	unsigned char independentkey = 0;
	if(P3_1 == 0){Delay(20);while(P3_1 == 0);Delay(20);independentkey = 1;}
	if(P3_0 == 0){Delay(20);while(P3_0 == 0);Delay(20);independentkey = 2;}
	if(P3_2 == 0){Delay(20);while(P3_2 == 0);Delay(20);independentkey = 3;}
	if(P3_3 == 0){Delay(20);while(P3_3 == 0);Delay(20);independentkey = 4;}
	return independentkey;
}
