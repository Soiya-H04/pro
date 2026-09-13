/*

name:	 	Delay 函数
param:		x
retval:		无
use to:		延迟 x ms
updatetime:	2025-8-7

*/

#include <REGX52.H>


void Delay(unsigned int x)	// 1ms
{
	unsigned char data i, j;
	while(x)
	{
		
		i = 2;
		j = 199;
		do
		{
			while (--j);
		} while (--i);
		x -= 1;
	}
}