/*

name:	 		PasswdOperator.c
ref:			LCDShow.h
used to:		对密码进行一系列操作。
updatetime:		2025-08-08

*/

/*

function name:		passwd_input
param:				passwd[6] index num
retval:				none
description:		将 num 输入到 passwd[index]
updatetime:			2025-08-10

*/

void passwd_input(unsigned char passwd[6],unsigned char index,unsigned char num)
{
	switch(num)
	{
		case 1:passwd[index] = 1;break;
		case 2:passwd[index] = 2;break;
		case 3:passwd[index] = 3;break;
		case 4:passwd[index] = 4;break;
		case 5:passwd[index] = 5;break;
		case 6:passwd[index] = 6;break;
		case 7:passwd[index] = 7;break;
		case 8:passwd[index] = 8;break;
		case 9:passwd[index] = 9;break;
		case 10:passwd[index] = 0;break;
		default:break;
	}
}

/*

function name:		passwd_reset
param:				passwd
retval:				resetflag
description:		重置输入的密码，成功重置 flag_reset 返回 1，失败返回 0。
updatetime:			2025-08-10	

*/

void passwd_reset(unsigned char passwd[6])
{
	int i = 0;
	for (i;i < 6;i++)
	{
		passwd[i] = 0;
	}
}

/*

function name:		passwd_match
param:				rightpasswd userpasswd
retval:				state_matched
description:		比较用户输入的密码与正确密码，匹配成功返回 1，失败返回 0。
updatetime:			2025-08-10

*/

unsigned char passwd_match(unsigned char rightpasswd[6],unsigned char userpasswd[6])
{
	unsigned char state_matched = 0;
	int i = 0;
	for(i;i < 6; i++)
	{
		if (userpasswd[i] == rightpasswd[i])
		{
			state_matched = 1;
		}
		else
		{
			state_matched = 0;
			break;
		}
	}	
	return state_matched;
}

/*

function name:		passwd_set
param:				oldpasswd newpasswd
retval:				none
description:		更改密码，并重置错误次数,,更改成功返回 1，更改失败返回 0。
updatetime:			2025-08-10

*/

void passwd_set(unsigned char oldpasswd[6],unsigned char newpasswd[6])
{
	unsigned char  i = 0;
	for (i; i < 6;i++)
	{
		oldpasswd[i] = newpasswd[i];
	}
}