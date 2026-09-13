#include <REGX52.H>
#include "Delay.h"


unsigned char change_mod()
{
	static unsigned char mode = 0;
	if(P3_1 == 0){Delay(20);while(P3_1 == 0);Delay(20);mode = 1;}
	if(P3_0 == 0){Delay(20);while(P3_0 == 0);Delay(20);mode = 2;}
	if(P3_2 == 0){Delay(20);while(P3_2 == 0);Delay(20);mode = 3;}
	return mode;
}