#include <REGX52.H>
#include "Timer0.h"
#include "LCD1602.h"

unsigned char second = 50;
unsigned char minute = 59;
unsigned char hour = 23;

void main()
{
	LCD_Init();
	Timer0_Init();
	LCD_ShowString(1,1,"Clock:");
	LCD_ShowString(2,1,"  :  :  ");
	while(1)
	{
		LCD_ShowNum(2,1,hour,2);
		LCD_ShowNum(2,4,minute,2);
		LCD_ShowNum(2,7,second,2);
	}
}


void Timer0_Routine() interrupt 1
{
	static unsigned int count = 0;
	TL0 = 0x18;				
	TH0 = 0xFC;	
	count++;
	if (count >= 1000)
	{
		count = 0;
		second++;
		if(second >= 60)
		{
			second = 0;
			minute++;
			if(minute >= 60)
			{
				minute =0;
				hour++;
				if(hour >= 24)
				{
					hour = 0;
				}
			}
		}
		
	}
	
}