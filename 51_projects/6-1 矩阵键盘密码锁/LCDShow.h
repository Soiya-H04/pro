#ifndef __LCDSHOW_H__
#define __LCDSHOW_H__

void LCD_initial();
void LCD_input(unsigned char index);
void LCD_right();
void LCD_error0();
void LCD_error1();
void LCD_oldpasswd_set(unsigned char passwd_index);
void LCD_newpasswd_set(unsigned char passwd_index);
void LCD_newpasswd_again(unsigned char passwd_index);
void LCD_locked();
void LCD_unlocked();
void LCD_down();
void LCD_set_OK();

#endif