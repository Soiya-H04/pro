/*

name:	 	点亮 LED
param:		无
retval:		无
ref:		REGX52.H
use to:		点亮 D1 与 D7 的 LED。
updatetime:	2025-08-08

*/

#include <REGX52.H>


void main()
{
	P2 = 0xFF;
	P2_0 = 0;
	P2_6 = 0;
	while(1)
	{
		
	}
}