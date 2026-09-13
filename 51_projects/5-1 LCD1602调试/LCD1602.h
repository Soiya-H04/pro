#ifndef __LCD1602_H__
#define __LCD1602_H__

// 用户调用函数：
// LCD 显示屏初始化
void LCD_Init();
// 显示字母
void LCD_ShowChar(unsigned char Line,unsigned char Column,char Char);
// 显示字符串
void LCD_ShowString(unsigned char Line,unsigned char Column,char *String);
// 显示无符号数字
void LCD_ShowNum(unsigned char Line,unsigned char Column,unsigned int Number,unsigned char Length);
// 显示有符号数字
void LCD_ShowSignedNum(unsigned char Line,unsigned char Column,int Number,unsigned char Length);
// 显示十六进制数字
void LCD_ShowHexNum(unsigned char Line,unsigned char Column,unsigned int Number,unsigned char Length);
// 显示二进制数字
void LCD_ShowBinNum(unsigned char Line,unsigned char Column,unsigned int Number,unsigned char Length);

#endif
