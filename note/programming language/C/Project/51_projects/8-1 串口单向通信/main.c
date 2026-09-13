#include <REGX52.H>
#include "Delay.h"


void UART_Init()
{
	//�����ʼӱ�
	PCON = 0x80;
	//8λUARTģʽ
	SCON = 0x40;
	//������1 ��λ����
	TMOD &= 0x0F;
	TMOD |= 0x20;
	
	TL1 = 0xF4;			
	TH1 = 0xF4;			
	TR1 = 1;
	ET1 = 0;
}

void UART_Send(unsigned char send_data)
{
    SBUF = send_data;
    while(TI == 0);
    TI = 0;
}

void main()
{
	unsigned char count = 1; 
	UART_Init();
	while(1)
	{
		count++;
		Delay(1000);
		if(count < 90)
		{
			UART_Send(count);
		}
	}
}

