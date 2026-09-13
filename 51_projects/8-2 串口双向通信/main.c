#include "UART.h"
#include <REGX52.H>
#include "Delay.h"


void main()
{
	UART_Init();
	while(1)
	{
		if (P3_1 == 0){Delay(20);while(P3_1 == 0);Delay(20);SBUF = 0xFF;while(TI == 0);TI = 0;}
	}
	
	
}



void UART() interrupt 4
{
	if (RI == 1)
	{
		P2 = SBUF;
		RI = 0;
	}
	
}