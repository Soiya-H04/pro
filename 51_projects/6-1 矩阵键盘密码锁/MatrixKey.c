/*

name:	 		MatrixKey.c
ref:			REGX52.H Delay.h
use to:			检测矩阵键盘的按键按下与抬起。
				如果按键按下，matrixkey 返回对应位置的数字；如果按键未按下，matrixkey 返回 0。
updatetime:		2025-08-09

*/

#include <REGX52.H>
#include "Delay.h"	

/*

function name:		matrixkey_get
param:				none
retval:				matrixkey
description:		扫描矩阵键盘，若有按键按下，matrixkey 就返回该位置对应数字，若无按键按下返回，则返回数字 0。
updatetime:			2025-08-010

*/

unsigned char matrixkey_get()
{
	unsigned char matrixkey = 0;
	// 逐列扫描，先将列置 0，然后扫描行
	// 再全置 1，再将下一列置 0
	P1 = 0xFF;
	P1_3 = 0;
	if(P1_7 == 0){Delay(20);while(P1_7 == 0);Delay(20);matrixkey = 1;}
	if(P1_6 == 0){Delay(20);while(P1_6 == 0);Delay(20);matrixkey = 5;}
	if(P1_5 == 0){Delay(20);while(P1_5 == 0);Delay(20);matrixkey = 9;}
	if(P1_4 == 0){Delay(20);while(P1_4 == 0);Delay(20);matrixkey = 13;}

	P1 = 0xFF;
	P1_2 = 0;
	if(P1_7 == 0){Delay(20);while(P1_7 == 0);Delay(20);matrixkey = 2;}
	if(P1_6 == 0){Delay(20);while(P1_6 == 0);Delay(20);matrixkey = 6;}
	if(P1_5 == 0){Delay(20);while(P1_5 == 0);Delay(20);matrixkey = 10;}
	if(P1_4 == 0){Delay(20);while(P1_4 == 0);Delay(20);matrixkey = 14;}
	
	P1 = 0xFF;
	P1_1 = 0;
	if(P1_7 == 0){Delay(20);while(P1_7 == 0);Delay(20);matrixkey = 3;}
	if(P1_6 == 0){Delay(20);while(P1_6 == 0);Delay(20);matrixkey = 7;}
	if(P1_5 == 0){Delay(20);while(P1_5 == 0);Delay(20);matrixkey = 11;}
	if(P1_4 == 0){Delay(20);while(P1_4 == 0);Delay(20);matrixkey = 15;}
	
	P1 = 0xFF;
	P1_0 = 0;
	if(P1_7 == 0){Delay(20);while(P1_7 == 0);Delay(20);matrixkey = 4;}
	if(P1_6 == 0){Delay(20);while(P1_6 == 0);Delay(20);matrixkey = 8;}
	if(P1_5 == 0){Delay(20);while(P1_5 == 0);Delay(20);matrixkey = 12;}
	if(P1_4 == 0){Delay(20);while(P1_4 == 0);Delay(20);matrixkey = 16;}
	
	return matrixkey;
}