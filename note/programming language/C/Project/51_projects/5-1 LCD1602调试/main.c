/*

name:	 	测试 LCD1602 函数
param:		
retval:		无
ref:		REGX52.H LCD1602.h
use to:		
updatetime:	

*/

#include <REGX52.H>
#include "LCD1602.h"


void main()
{
	LCD_Init();
	LCD_ShowChar(1,1,'A');
	LCD_ShowString(1,3,"HAHA");
	LCD_ShowNum(1,8,2,1);
	LCD_ShowSignedNum(1,10,12,2);
	LCD_ShowHexNum(2,1,0x1A,2);
	LCD_ShowBinNum(2,6,1001,4);
	while(1)
	{
	}
}