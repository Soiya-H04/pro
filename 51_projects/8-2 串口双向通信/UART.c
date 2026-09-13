#include <REGX52.H>

void UART_Init()
{
	// PCON
	PCON = 0x80;
	
	// SCON
	SCON = 0x00;
	// receive
	REN = 1;
	// 8 bit UART
	SM1 = 1;
	
	// Timer1
	TMOD &= 0x0F;
	TMOD |= 0x20;
	TR1 = 1;
	ET1 = 0;
	TL1 = 0xF4;
	TH1 = 0xF4;
	
	// ES
	ES = 1;
	EA = 1;
	
}


void UART_send(unsigned char send_data)
{
	SBUF = send_data;
	while(TI == 0);
	TI = 0;
}
