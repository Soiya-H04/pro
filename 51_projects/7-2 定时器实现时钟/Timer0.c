#include <REGX52.H>

void Timer0_Init()
{
	TMOD &= 0xF0;
	TMOD |= 0x01;
    TF0 = 0;
	TR0 = 1;
	// 1ms
	TL0 = 0x18;				
	TH0 = 0xFC;				
	ET0 = 1;
	EA = 1;
	PT0 = 0;
}




/*

void Timer0_Routine() interrupt 1
{
	static unsigned int count;
	TL0 = 0x18;				
	TH0 = 0xFC;	
	count++;
	if (count >= 1000)
	{
		count = 0;
		|
	}
	
}

*/