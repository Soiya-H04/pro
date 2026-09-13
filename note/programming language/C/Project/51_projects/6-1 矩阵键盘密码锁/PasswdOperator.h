#ifndef __PASSWDOPERATOR_H__
#define __PASSWDOPERATOR_H__

void passwd_input(unsigned char passwd[6],unsigned char index,unsigned char num);
void passwd_reset(unsigned char passwd[6]);
unsigned char passwd_match(unsigned char rightpasswd[6],unsigned char userpasswd[6]);
void passwd_set(unsigned char oldpasswd[6],unsigned char newpasswd[6]);


#endif