/*

name:	 	动态数码管显示
param:		5 3 1 2 2 1 3 
retval:		无
ref:		REGX52.H Delay.h
use to:		在不同的 locate 上显示不同的 num，采用动态显示。
updatetime:	

*/

#include <REGX52.H>
#include "Delay.h"
#include "ShowDigit.h"


void main()
{
	while(1)
	{
		showdigit(3,1);
		// 等待 5us 再清空，增强亮度
		Delay(5);
		P0 = 0x00;
		showdigit(2,2);
		Delay(5);
		P0 = 0x00;
		showdigit(1,3);
		Delay(5);
		P0 = 0x00;
	}
}