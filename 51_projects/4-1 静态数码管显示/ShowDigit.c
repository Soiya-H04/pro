/*

name:	 	数码管显示任意数字
param:		locate num
retval:		无
ref:		REGX52.H
use to:		在 locate 的位置，显示数字 num。
updatetime:	2025-08-08

*/

#include <REGX52.H>

void showdigit(unsigned char locate,unsigned char num)
{
	if (locate <= 8 && locate >= 1) 
	{
		if (num <= 9 && num >= 0)
		{
			switch(locate)
			{
				case 1:	P2_4 = 0;P2_3 = 0;P2_2 = 0;break;
				case 2:	P2_4 = 0;P2_3 = 0;P2_2 = 1;break;
				case 3:	P2_4 = 0;P2_3 = 1;P2_2 = 0;break;
				case 4:	P2_4 = 0;P2_3 = 1;P2_2 = 1;break;
				case 5:	P2_4 = 1;P2_3 = 0;P2_2 = 0;break;
				case 6:	P2_4 = 1;P2_3 = 0;P2_2 = 1;break;
				case 7:	P2_4 = 1;P2_3 = 1;P2_2 = 0;break;
				case 8:	P2_4 = 1;P2_3 = 1;P2_2 = 1;break;
				default:break;
			}
			switch(num)
			{
				case 0:P0 = 0x3F;break;
				case 1:P0 = 0x06;break;
				case 2:P0 = 0x5B;break;
				case 3:P0 = 0x4F;break;
				case 4:P0 = 0x66;break;
				case 5:P0 = 0x6D;break;
				case 6:P0 = 0x7D;break;
				case 7:P0 = 0x07;break;
				case 8:P0 = 0x7F;break;
				case 9:P0 = 0x6F;break;
				default:break;
			}
		}
	}
}