#include <REGX52.H>
#include "Timer0.h"
#include "chg_mod.h"

unsigned char mode = 0;

void main()
{
	// ��ʱ����ʼ��
	Timer0_Init();
	P2_0 = 0;
	P2_1 = 0;
	P2_2 = 0; 
	while(1)
	{
		mode = change_mod();
	}
}

void Timer0_Routine() interrupt 1
{
	static unsigned int T0Count = 0;
	TL0 = 0x18;				
	TH0 = 0xFC;	
	T0Count++;
	if(T0Count >= 200)
	{
		T0Count = 0;
		if(mode == 1)
		{
			if(P2_0 == 0)
			{
				P2 = (P2 >> 1) | 0x80;
				P2_7 = 0;
			}
			else
			{
				P2 = (P2 >> 1) | 0x80;
			}
		}
		else if(mode == 2)
		{
				P2 = 0xFF;
				P2_0 = 0;
				P2_1 = 0;
				P2_2 = 0; 
		}
		else if(mode == 3)
		{
			if(P2_7 == 0)
			{
				P2 = (P2 << 1) | 0x01;
				P2_0 = 0;
			}
			else
			{
				P2 = (P2 << 1) | 0x01;
			}
		}
			
	}
	
}