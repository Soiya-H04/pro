import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QStyledItemDelegate
from openai import OpenAI
from openpyxl import Workbook
import os
from datetime import datetime
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import re
import traceback
import sqlite3
import pandas as pd
import json

class MealPlanExcelGenerator:
    """一周食谱 Excel 生成器"""

    def __init__(self):
        self.wb = None
        self.ws = None

    def calculate_text_col_span(self, weekly_recipe):
        """根据所有餐食文本计算需要的列合并格数"""
        max_length = 0
        max_text = ""
        for day, meal_recipe in weekly_recipe.items():
            for meal, meal_texts in meal_recipe.items():
                for meal_text in meal_texts:
                    length = len(meal_text)
                    if length > max_length:
                        max_length = length
                        max_text = meal_text

        chars_per_col = 3
        col_span = (max_length + chars_per_col - 1) // chars_per_col

        if col_span <=6:
            col_span = 6
        return col_span

    def calculate_text_row_span(self, combo_count):
        """根据组合个数计算需要的行合并格数"""
        if not combo_count:
            return 7

        if combo_count <= 4:
            row_span = 7
        else:
            extra = (combo_count - 4 + 1) // 2
            row_span = 7 + extra * 3

        return row_span

    def set_cell_style(self, cell, font_name='宋体', font_size=14, bold=False,
                       horizontal='center', vertical='center', wrap_text=True, fill_color=None):
        """设置单元格样式"""
        cell.font = Font(name=font_name, size=font_size, bold=bold)
        cell.alignment = Alignment(horizontal=horizontal, vertical=vertical, wrap_text=wrap_text)
        if fill_color:
            cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type='solid')

    def set_border(self, cell, left=True, right=True, top=True, bottom=True,
                   left_style='thin', right_style='thin', top_style='thin', bottom_style='thin'):
        """设置单元格边框"""
        border = Border(
            left=Side(style=left_style if left else None),
            right=Side(style=right_style if right else None),
            top=Side(style=top_style if top else None),
            bottom=Side(style=bottom_style if bottom else None)
        )
        cell.border = border

    def generate_excel(self, structured_data, output_filename=None):
        """生成Excel表格"""

        # 数据标头
        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        meals = ["早餐", "午餐", "晚餐"]

        if not structured_data:
            return None

        # 创建周食谱结构
        weekly_recipe = {}
        for day in days:
            weekly_recipe[day] = {}
            for meal in meals:
                weekly_recipe[day][meal] = []

        # 添加周食谱数据
        for combo in structured_data:
            combo_name = combo["组合"]
            combo_recipe = combo["周食谱"]
            for day in days:
                for meal in meals:
                    meal_text = f"{combo_name}：{combo_recipe[day][meal]}"
                    weekly_recipe[day][meal].append(meal_text)

        # 行合并数
        combo_count = len(structured_data)
        row_span = self.calculate_text_row_span(combo_count)
        # 列合并数
        col_span = self.calculate_text_col_span(weekly_recipe)

        # 创建工作簿
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "青年篮球运动员周食谱"

        # 设置默认行高列宽
        self.ws.sheet_format.defaultRowHeight = 14
        self.ws.sheet_format.defaultColWidth = 8.08

        # 1. 标题栏
        # 起始行列
        start_row = 1
        start_col = 1
        # 尾行列
        end_row = 8
        end_col = 3 + 7 * col_span
        #  合并
        self.ws.merge_cells(start_row=start_row, start_column=start_col, end_row=end_row, end_column=end_col)
        # 锁定单元格
        title_cell = self.ws.cell(row=start_row, column=start_col)
        # 设置文本
        title_cell.value = "青年篮球运动员周食谱"
        # 设置格式
        self.set_cell_style(title_cell, font_size=48, bold=True, fill_color='E2EFDA')

        # 2. 餐次栏
        # 起始行列
        start_row = 9
        start_col = 1
        # 尾行列
        end_row = start_row + 4
        end_col = 3
        # 合并
        self.ws.merge_cells(start_row=start_row, start_column=start_col,
                            end_row=end_row, end_column=end_col)
        # 锁定单元格
        meal_category_cell = self.ws.cell(row=start_row, column=start_col)
        # 设置文本
        meal_category_cell.value = "餐次"
        # 设置格式
        self.set_cell_style(meal_category_cell, font_size=26, fill_color='D9E1F2')

        # 3. 星期栏
        for i, day in enumerate(days):
            # 起始行列
            start_row = 9
            start_col = 4 + i * col_span
            # 尾行列
            end_row = start_row + 4
            end_col = start_col + col_span - 1
            # 合并
            self.ws.merge_cells(start_row=start_row, start_column=start_col,
                                end_row=end_row, end_column=end_col)
            # 锁定单元格
            cell = self.ws.cell(row=start_row, column=start_col)
            # 设置文本
            cell.value = day
            # 设置格式
            self.set_cell_style(cell, font_size=26, fill_color='FFE699')

        # 4. 具体餐次
        # 餐次颜色
        meal_colors = {
            "早餐": "FFF2CC",
            "午餐": "C4D2B0",
            "晚餐": "8EB19C"
        }
        for i, meal in enumerate(meals):
            # 起始行列
            start_row = 14 + i * row_span
            start_col = 1
            # 尾行列
            end_row = start_row + row_span - 1
            end_col = 3
            # 合并
            self.ws.merge_cells(start_row=start_row, start_column=start_col,
                                end_row=end_row, end_column=end_col)
            # 锁定单元格
            meal_cell = self.ws.cell(row=start_row, column=start_col)
            # 设置文本
            meal_cell.value = meal
            # 设置格式
            self.set_cell_style(meal_cell, font_size=22, fill_color=meal_colors.get(meal, 'F9F9F9'))

        # 5. 具体数据
        for i_d, day in enumerate(days):
            for i_m, meal in enumerate(meals):
                # 起始行列
                start_row = 14 + i_m * row_span
                start_col = 4 + i_d * col_span
                # 尾行列
                end_row = start_row + row_span - 1
                end_col = start_col + col_span - 1
                # 合并
                self.ws.merge_cells(start_row=start_row, start_column=start_col,
                                    end_row=end_row, end_column=end_col)
                # 锁定单元格
                day_cell = self.ws.cell(row=start_row, column=start_col)
                # 设置文本
                cell_text = "\n".join(weekly_recipe[day][meal])
                day_cell.value = cell_text
                # 设置格式
                self.set_cell_style(day_cell)

        # 6. 设置边框
        for row in range(1, end_row + 1):
            for col in range(1, end_col + 1):
                cell = self.ws.cell(row=row, column=col)
                self.set_border(cell, left_style='thin', right_style='thin',
                                top_style='thin', bottom_style='thin')

        # 7. 设置特殊边框
        for row in range(1, end_row + 1):
            for col in range(1, end_col + 1):
                cell = self.ws.cell(row=row, column=col)
                left = (col == 1)
                right = (col == end_col)
                top = (row == 1)
                bottom = (row == end_row)

                border = cell.border
                new_left = Side(style='thick') if left else border.left
                new_right = Side(style='thick') if right else border.right
                new_top = Side(style='thick') if top else border.top
                new_bottom = Side(style='thick') if bottom else border.bottom

                cell.border = Border(left=new_left, right=new_right, top=new_top, bottom=new_bottom)

        # 保存文件
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"青年篮球运动员周食谱_{timestamp}.xlsx"

        filepath = os.path.join(os.getcwd(), output_filename)
        self.wb.save(filepath)
        return filepath

class AIRecipeWorker(QObject):
    """AI生成食谱工作线程"""
    finished = Signal(bool, str, object)

    def __init__(self, api_key, combinations):
        super().__init__()
        self.api_key = api_key
        self.combinations = combinations

    def get_recipes_data(self):
        """从数据库获取食谱数据"""

        try:
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, category, ingredients FROM recipes")
            rows = cursor.fetchall()
            conn.close()

            # 按新类别分类
            recipes_by_category = {
                "早餐主食": [], "早餐饮品": [],
                "午晚餐主食": [],
                "午晚餐鸡类": [], "午晚餐鸭类": [], "午晚餐牛类": [],
                "午晚餐猪类": [], "午晚餐鱼虾类": [],
                "午晚餐蛋类": [], "午晚餐蔬菜类": []
            }

            for row in rows:
                category = row[2]
                if category in recipes_by_category:
                    recipes_by_category[category].append(row[1])

            return recipes_by_category
        except Exception as e:
            return None

    def get_nutrition_data(self):
        """从数据库获取食材营养数据"""
        try:
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, protein, carbs, fat, fiber, sugar, calories 
                FROM ingredients
            """)
            rows = cursor.fetchall()
            conn.close()

            nutrition_text = ""
            for row in rows:
                nutrition_text += f"{row[0]}: 蛋白质{row[1]}g, 碳水{row[2]}g, 脂肪{row[3]}g, 膳食纤维{row[4]}g, 糖类{row[5]}g, 热量{row[6]}千卡\n"
            return nutrition_text
        except Exception as e:
            return f"读取营养数据失败: {e}"

    def get_meat_weight_from_db(self, dish_name):
        """从数据库获取菜品对应的肉类重量"""
        try:
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()

            # 清理菜名，去除可能的前缀空格和括号内容
            original_name = dish_name
            dish_name = dish_name.strip()
            # 去除已有的括号标注
            dish_name = re.sub(r'\([^)]*\)', '', dish_name).strip()

            # 先精确匹配
            cursor.execute("SELECT name, ingredients FROM recipes WHERE name = ?", (dish_name,))
            row = cursor.fetchone()

            if row:
                pass
            conn.close()
            if not row:
                return None

            matched_name = row[0]
            ingredients = row[1] if row[1] else ""

            # 解析食材配量，提取肉类重量
            meat_pattern = r'(鸡胸肉|鸡腿肉|鸡肉|鸭胸肉|鸭腿肉|鸭肉|牛肉|猪瘦肉|猪排骨|猪肉|草鱼|鲈鱼|虾|鱼)\s*(\d+)g'
            matches = re.findall(meat_pattern, ingredients, re.IGNORECASE)

            if matches:
                # 取重量最大的
                max_weight = 0
                selected_match = None
                for meat_name, weight in matches:
                    w = int(weight)
                    if w > max_weight:
                        max_weight = w
                        selected_match = (meat_name, weight)

                if selected_match:
                    meat_name, weight = selected_match
                    return f"{weight}g"
            return None

        except Exception as e:
            return None

    def add_meat_weight_to_dish(self, dish_text):
        """为菜品添加肉类分量标注"""
        if not dish_text:
            return dish_text

        # 处理卤鸡腿和卤鸭腿
        dish_text = re.sub(r'卤鸡腿(?!\s*\()', '卤鸡腿(2个)', dish_text)
        dish_text = re.sub(r'卤鸭腿(?!\s*\()', '卤鸭腿(2个)', dish_text)

        # 按多种分隔符分割
        parts = re.split(r'\s*\+\s*|\s*、\s*', dish_text)

        # 先识别这一餐的肉类组合
        meat_parts = []  # 存储肉菜部分
        egg_parts = []  # 存储炒蛋部分
        other_parts = []  # 存储菜类部分
        has_egg = False
        has_beef = False

        # 非肉菜不加分量
        non_meat_keywords = [
            '米饭', '面包', '馒头', '花卷', '米粉', '面条', '荞麦面', '全麦面包'
            '牛奶', '酸奶', '豆浆',
            '时蔬', '炒时蔬', '蔬菜',
            '红薯', '玉米', '芋头',
            '水煮蛋', '鸡蛋青菜饼', '瘦肉米粉', '叉烧包', '肉包', '煎饺'
        ]

        other_meat_keyword = ['鸡', '鸭', '猪', '排骨', '鱼', '虾']



        for part in parts:
            part = part.strip()
            if not part:
                continue

            # 判断是否是非肉菜
            is_non_meat = any(kw in part for kw in non_meat_keywords)
            if is_non_meat:
                other_parts.append(part)
                continue

            # 判断是否是炒蛋类
            if '炒鸡蛋' in part or '炒蛋' in part:
                has_egg = True
                egg_parts.append(part)
                continue

            # 判断是否包含牛肉
            if '牛' in part:
                has_beef = True
                meat_parts.append(('beef', part))
                continue

            # 判断是否包含其他肉类（鸡、鸭、猪、鱼、虾、排骨）
            if any(kw in part for kw in other_meat_keyword):
                meat_parts.append(('other', part))
                continue

            other_parts.append(part)

        # 判断是否是牛肉+炒蛋组合
        is_beef_with_egg = has_beef and has_egg

        # 处理每个部分
        processed_parts = []

        # 处理肉菜
        for meat_type, part in meat_parts:
            # 如果已经有括号标注，跳过
            if re.search(r'\(\d+g\)|\(\d+个/\d+g\)|\(\d+个\)', part):
                processed_parts.append(part)
                continue
            if meat_type == 'other':
                # 非牛肉类直接加分量
                weight_info = self.get_meat_weight_from_db(part)
                if weight_info:
                    part = f"{part}({weight_info})"
                else:
                    # 如果数据库没找到，默认加150g
                    part = f"{part}(150g)"
            elif meat_type == 'beef':
                # 牛肉类：只有配炒蛋时才加分量
                if is_beef_with_egg:
                    weight_info = self.get_meat_weight_from_db(part)
                    if weight_info:
                        part = f"{part}({weight_info})"
                    else:
                        part = f"{part}(150g)"
                else:
                    # 牛肉配其他肉类，不加分量
                    pass

            processed_parts.append(part)

        # 重新组合，保持原有顺序
        final_parts = []
        processed_copy = list(processed_parts)
        egg_copy = list(egg_parts)
        other_copy = list(other_parts)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # 在已处理的部分中查找匹配
            found = False

            # 检查肉菜
            for i, pp in enumerate(processed_copy):
                pp_clean = re.sub(r'\(\d+g\)|\(\d+个/\d+g\)|\(\d+个\)', '', pp).strip()
                if pp_clean == part or part in pp or pp in part:
                    final_parts.append(pp)
                    processed_copy.pop(i)
                    found = True
                    break

            if found:
                continue

            # 检查炒蛋
            for i, ep in enumerate(egg_copy):
                if ep == part or part in ep or ep in part:
                    final_parts.append(ep)
                    egg_copy.pop(i)
                    found = True
                    break

            if found:
                continue

            # 检查其他部分
            for i, op in enumerate(other_copy):
                if op == part or part in op or op in part:
                    final_parts.append(op)
                    other_copy.pop(i)
                    found = True
                    break

            if not found:
                final_parts.append(part)

        # 添加遗漏的部分
        final_parts.extend(processed_copy)
        final_parts.extend(egg_copy)
        final_parts.extend(other_copy)

        result = ' + '.join(final_parts)
        return result

    def parse_ai_response(self, response_text, combo_text):
        """解析AI返回的文本，提取菜式数据"""
        result = {
            "组合": combo_text,
            "早餐营养标准": {},
            "午餐营养标准": {},
            "晚餐营养标准": {},
            "周食谱": {}
        }
        result_with_g = {
            "组合": combo_text,
            "早餐营养标准": {},
            "午餐营养标准": {},
            "晚餐营养标准": {},
            "周食谱": {}
        }

        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

        # 提取营养标准
        nutrition_pattern = r'营养标准[：:]\s*\n早餐[：:]\s*蛋白质\s*([\d.]+)g，碳水\s*([\d.]+)g，脂肪\s*([\d.]+)g，膳食纤维\s*([\d.]+)g，糖类\s*([\d.]+)g，热量\s*([\d.]+)千卡\s*\n午餐[：:]\s*蛋白质\s*([\d.]+)g，碳水\s*([\d.]+)g，脂肪\s*([\d.]+)g，膳食纤维\s*([\d.]+)g，糖类\s*([\d.]+)g，热量\s*([\d.]+)千卡\s*\n晚餐[：:]\s*蛋白质\s*([\d.]+)g，碳水\s*([\d.]+)g，脂肪\s*([\d.]+)g，膳食纤维\s*([\d.]+)g，糖类\s*([\d.]+)g，热量\s*([\d.]+)千卡'

        nutrition_match = re.search(nutrition_pattern, response_text, re.DOTALL)
        if nutrition_match:
            result["早餐营养标准"] = {
                "蛋白质": nutrition_match.group(1),
                "碳水": nutrition_match.group(2),
                "脂肪": nutrition_match.group(3),
                "膳食纤维": nutrition_match.group(4),
                "糖类": nutrition_match.group(5),
                "卡路里": nutrition_match.group(6)
            }
            result["午餐营养标准"] = {
                "蛋白质": nutrition_match.group(7),
                "碳水": nutrition_match.group(8),
                "脂肪": nutrition_match.group(9),
                "膳食纤维": nutrition_match.group(10),
                "糖类": nutrition_match.group(11),
                "卡路里": nutrition_match.group(12)
            }
            result["晚餐营养标准"] = {
                "蛋白质": nutrition_match.group(13),
                "碳水": nutrition_match.group(14),
                "脂肪": nutrition_match.group(15),
                "膳食纤维": nutrition_match.group(16),
                "糖类": nutrition_match.group(17),
                "卡路里": nutrition_match.group(18)
            }
            result_with_g["早餐营养标准"] = {
                "蛋白质": nutrition_match.group(1),
                "碳水": nutrition_match.group(2),
                "脂肪": nutrition_match.group(3),
                "膳食纤维": nutrition_match.group(4),
                "糖类": nutrition_match.group(5),
                "卡路里": nutrition_match.group(6)
            }
            result_with_g["午餐营养标准"] = {
                "蛋白质": nutrition_match.group(7),
                "碳水": nutrition_match.group(8),
                "脂肪": nutrition_match.group(9),
                "膳食纤维": nutrition_match.group(10),
                "糖类": nutrition_match.group(11),
                "卡路里": nutrition_match.group(12)
            }
            result_with_g["晚餐营养标准"] = {
                "蛋白质": nutrition_match.group(13),
                "碳水": nutrition_match.group(14),
                "脂肪": nutrition_match.group(15),
                "膳食纤维": nutrition_match.group(16),
                "糖类": nutrition_match.group(17),
                "卡路里": nutrition_match.group(18)
            }

        # 提取周食谱
        for day in days:
            day_pattern = rf'{day}\s*\n早餐[：:]\s*(.+?)\s*\n午餐[：:]\s*(.+?)\s*\n晚餐[：:]\s*(.+?)(?=\n\n|\n星期二|\n星期三|\n星期四|\n星期五|\n星期六|\n星期日|$)'
            day_match = re.search(day_pattern, response_text, re.DOTALL)
            if day_match:
                breakfast = day_match.group(1).strip()
                lunch = day_match.group(2).strip()
                dinner = day_match.group(3).strip()

                # 将顿号替换为加号
                breakfast = breakfast.replace('、', ' + ')
                lunch = lunch.replace('、', ' + ')
                dinner = dinner.replace('、', ' + ')

                result["周食谱"][day] = {
                    "早餐": breakfast,
                    "午餐": lunch,
                    "晚餐": dinner
                }
                result_with_g["周食谱"][day] = {
                    "早餐": breakfast,
                    "午餐": self.add_meat_weight_to_dish(lunch),
                    "晚餐": self.add_meat_weight_to_dish(dinner)
                }

        return result, result_with_g

    def enforce_meal_consistency(self, structured_data):
        """
        强制保证所有组合的菜式一致性
        以第一个组合的菜式为标准，应用到所有其他组合
        """
        if not structured_data or len(structured_data) <= 1:
            return structured_data

        # 以第一个组合的菜式为标准
        base_combo = structured_data[0]
        base_meals = base_combo["周食谱"]

        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        meals = ["午餐", "晚餐"]

        # 提取第一个组合每天的午餐和晚餐的菜式（去除主食）
        base_dishes = {}
        for day in days:
            base_dishes[day] = {}
            for meal in meals:
                dish_text = base_meals[day][meal]
                # 格式：主食 + 肉菜1 + 肉菜2 + 菜类菜式
                parts = dish_text.split(' + ')
                if len(parts) >= 4:
                    # 保留后三个（肉菜1、肉菜2、菜类菜式）
                    base_dishes[day][meal] = ' + '.join(parts[1:])
                else:
                    base_dishes[day][meal] = dish_text

        # 应用到其他组合
        for i in range(1, len(structured_data)):
            combo = structured_data[i]
            for day in days:
                for meal in meals:
                    original_text = combo["周食谱"][day][meal]
                    parts = original_text.split(' + ')
                    if len(parts) >= 4:
                        # 保留主食，替换菜式部分
                        staple = parts[0]
                        new_dish = f"{staple} + {base_dishes[day][meal]}"
                        combo["周食谱"][day][meal] = new_dish

        return structured_data

    def enforce_breakfast_drink_consistency(self, structured_data):
        """
        强制保证所有组合的早餐饮品一致
        """
        if not structured_data or len(structured_data) <= 1:
            return structured_data

        # 提取第一个组合星期一的早餐饮品
        base_combo = structured_data[0]
        base_breakfast = base_combo["周食谱"]["星期一"]["早餐"]

        # 提取饮品（通常是最后一个加号后的部分，包含牛奶/豆浆/酸奶）
        drink_match = re.search(r'[+、]\s*([^+、]+(?:牛奶|豆浆|酸奶)[^+、]*)$', base_breakfast)
        if not drink_match:
            # 如果没找到，尝试其他日期
            for day in ["星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]:
                base_breakfast = base_combo["周食谱"][day]["早餐"]
                drink_match = re.search(r'[+、]\s*([^+、]+(?:牛奶|豆浆|酸奶)[^+、]*)$', base_breakfast)
                if drink_match:
                    break

        if not drink_match:
            return structured_data

        base_drink = drink_match.group(1).strip()

        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

        # 应用到其他组合
        for i in range(1, len(structured_data)):
            combo = structured_data[i]
            for day in days:
                breakfast = combo["周食谱"][day]["早餐"]
                # 替换饮品部分
                breakfast = re.sub(r'[+、]\s*[^+、]+(?:牛奶|豆浆|酸奶)[^+、]*$', f' + {base_drink}', breakfast)
                combo["周食谱"][day]["早餐"] = breakfast

        return structured_data

    def enforce_breakfast_egg_consistency(self, structured_data):
        """
        如果早餐中有水煮蛋，则固定为2个
        """
        if not structured_data:
            return structured_data

        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

        for combo in structured_data:
            for day in days:
                breakfast = combo["周食谱"][day]["早餐"]
                if '水煮蛋' in breakfast:
                    # 匹配水煮蛋后面的数量
                    breakfast = re.sub(r'水煮蛋\s*\d*\s*个', '水煮蛋2个', breakfast)
                    combo["周食谱"][day]["早餐"] = breakfast

        return structured_data

    def run(self):
        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )

            # 获取食谱数据
            recipes_data = self.get_recipes_data()
            if not recipes_data:
                self.finished.emit(False, "无法获取食谱数据", {})
                return

            # 获取营养数据
            nutrition_data = self.get_nutrition_data()

            # 构建食谱库文本
            recipes_text = "可用的食谱库：\n"

            if recipes_data.get("早餐主食"):
                recipes_text += f"\n【早餐主食】: {', '.join(recipes_data['早餐主食'])}\n"
            if recipes_data.get("早餐饮品"):
                recipes_text += f"\n【早餐饮品】: {', '.join(recipes_data['早餐饮品'])}\n"
            if recipes_data.get("午晚餐主食"):
                recipes_text += f"\n【午晚餐主食】: {', '.join(recipes_data['午晚餐主食'])}\n"
            if recipes_data.get("午晚餐鸡类"):
                recipes_text += f"\n【鸡肉类】: {', '.join(recipes_data['午晚餐鸡类'])}\n"
            if recipes_data.get("午晚餐鸭类"):
                recipes_text += f"\n【鸭肉类】: {', '.join(recipes_data['午晚餐鸭类'])}\n"
            if recipes_data.get("午晚餐牛类"):
                recipes_text += f"\n【牛肉类】: {', '.join(recipes_data['午晚餐牛类'])}\n"
            if recipes_data.get("午晚餐猪类"):
                recipes_text += f"\n【猪肉类】: {', '.join(recipes_data['午晚餐猪类'])}\n"
            if recipes_data.get("午晚餐鱼虾类"):
                recipes_text += f"\n【鱼虾类】: {', '.join(recipes_data['午晚餐鱼虾类'])}\n"
            if recipes_data.get("午晚餐蛋类"):
                recipes_text += f"\n【蛋类/豆腐类】: {', '.join(recipes_data['午晚餐蛋类'])}\n"
            if recipes_data.get("午晚餐蔬菜类"):
                recipes_text += f"\n【蔬菜类】: {', '.join(recipes_data['午晚餐蔬菜类'])}\n"

            all_results = []
            all_structured_data = []
            all_structured_data_with_g = []

            for combo in self.combinations:
                combo_text = "/".join([f"{value}" for cat, value in combo.items()])

                prompt = f"""根据用户条件，制定一周食谱。

                用户条件：{combo_text}

                可用食谱：
                {recipes_text}

                食材营养标准（每100g）：
                {nutrition_data}

                ═══════════════════════════════════════════════════════════════
                【核心规则 - 必须严格遵守】
                ═══════════════════════════════════════════════════════════════

                一、早餐规则：
                   格式：早餐主食1 + 数量单位 + 早餐主食2 + 数量单位 + 早餐饮品 + 数量单位

                   规则：
                   1. 早餐主食不能相同，必须选择2项不同的主食
                   2. 早餐主食要加量词，如个/杯/碗/片/根/份
                   3. 一周至少出现5次水煮蛋，且水煮蛋个数固定为2个
                   4. 必须包含【早餐饮品】1杯
                   5. 【关键】所有组合的早餐饮品必须100%完全相同
                   6. 不同组合的早餐主食可以根据营养需求不同而不同
                   7. 早餐主食的量词数要跟运动员的营养摄入匹配（根据AI智能搭配）但也要满足最低配置：
                        - 如果选取芋头的话，至少要2个
                        - 如果选取红薯的话，至少要2个
                        - 如果选取玉米的话，至少要1个
                        - 如果选取全麦面包的话，至少要2个
                        - 如果选取馒头的话，至少要2个
                        - 如果选取花卷的话，至少要2个
                        - 如果选取叉烧包的话，至少要2个
                        - 如果选取肉包的话，至少要2个
                        - 如果选取鸡蛋青菜饼的话，至少要1个
                        - 如果选取瘦肉米饭的话，至少要1碗
                        
                   8. 不要加分量

                   示例：
                   水煮蛋2个 + 全麦面包2片 + 牛奶1杯
                   水煮蛋2个 + 玉米1根 + 酸奶1杯

                二、午餐规则：
                   格式：午晚餐主食 + 肉类菜式1 + 肉类菜式2 + 菜类菜式

                   规则：
                   1. 主食必须从【白米饭、糙米饭】中选取
                   2. 肉类菜式1与肉类菜式2不能相同，且使用的肉类种类不能相同（如鸡肉+牛肉，不能鸡肉+鸡肉）
                   3. 肉类从【鸡肉类、鸭肉类、牛肉类、猪肉类、鱼虾类、蛋类】中选取
                   4. 菜类菜式只能是【炒时蔬】
                   5. 【关键】所有组合同一天的午餐，主食可以不同，但肉类菜式与菜类菜式必须100%完全相同
                   6. 所有组合不同天的午餐，肉类菜式要有变化，尽量每天不同（可以有重复菜式，但不能完全相同）
                   7. 7天的午餐之间，肉类种类要轮换使用

                   示例：
                   增肌：白米饭 + 清蒸鲈鱼 + 洋葱炒鸡蛋 + 炒时蔬
                   减脂：糙米饭 + 清蒸鲈鱼 + 洋葱炒鸡蛋 + 炒时蔬

                三、晚餐规则：
                   格式：午晚餐主食 + 肉类菜式1 + 肉类菜式2 + 菜类菜式

                   规则：
                   1. 主食必须从【白米饭、糙米饭】中选取
                   2. 肉类菜式1与肉类菜式2不能相同，且使用的肉类种类不能相同
                   3. 肉类从【鸡肉类、鸭肉类、牛肉类、猪肉类、鱼虾类、蛋类】中选取
                   4. 菜类菜式只能是【炒时蔬】
                   5. 【关键】所有组合同一天的晚餐，主食可以不同，但肉类菜式与菜类菜式必须100%完全相同
                   6. 所有组合不同天的晚餐，肉类菜式要有变化，尽量每天不同（可以有重复菜式，但不能完全相同）
                   7. 7天的晚餐之间，肉类种类要轮换使用
                   8. 午餐和晚餐之间，肉类菜式也要尽量不同

                   示例：
                   增肌：白米饭 + 香煎鸭胸肉排 + 蒜苗炒猪肉 + 炒时蔬
                   减脂：糙米饭 + 香煎鸭胸肉排 + 蒜苗炒猪肉 + 炒时蔬

                四、炒蛋安排规则：
                   1. 【重要】炒蛋类菜品（番茄炒鸡蛋、洋葱炒鸡蛋、青椒炒鸡蛋）算作肉菜！
                   2. 每天必须有一餐且最多一餐包含炒蛋类菜品（午餐或晚餐），一周7天都要有炒蛋
                   3. 炒蛋算作两道肉菜中的一道
                   4. 另一道肉菜从其他肉类（鸡、鸭、牛、猪、鱼虾）中选择
                   5. 炒蛋可以安排在午餐或晚餐，一周内要交替安排

                五、肉类轮换规则：
                   1. 鱼虾类一周最多出现2次
                   2. 鸡肉、鸭肉、牛肉、猪肉要在一周内均衡使用
                   3. 每天的两餐（午餐和晚餐）肉类种类要有变化

                六、所有菜式必须从上面食谱库中选择，不要编造不存在的菜品！

                ═══════════════════════════════════════════════════════════════
                【错误示例 - 绝对禁止】
                ═══════════════════════════════════════════════════════════════

                星期一晚餐：
                增肌：香煎鸭胸肉排 + 蒜苗炒猪肉 + 炒时蔬
                减脂：香煎鸭胸肉排 + 白灼虾 + 炒时蔬  ← 错误！肉菜不一样！

                ═══════════════════════════════════════════════════════════════
                【正确示例 - 必须遵守】
                ═══════════════════════════════════════════════════════════════

                星期一晚餐：
                增肌：糙米饭 + 香煎鸭胸肉排 + 蒜苗炒猪肉 + 炒时蔬
                减脂：糙米饭 + 香煎鸭胸肉排 + 蒜苗炒猪肉 + 炒时蔬
                （注意：肉菜完全一样，只有主食可以不同）

                ═══════════════════════════════════════════════════════════════
                【输出格式 - 必须严格遵守】
                ═══════════════════════════════════════════════════════════════

                请先输出第一个组合的完整一周食谱，然后输出其他组合的食谱。
                其他组合的菜式必须与第一个组合完全相同，只修改主食和早餐主食！

                {combo_text}：
                所需营养标准：
                早餐：蛋白质 Xg，碳水 Xg，脂肪 Xg，膳食纤维 Xg，糖类 Xg，热量 X千卡
                午餐：蛋白质 Xg，碳水 Xg，脂肪 Xg，膳食纤维 Xg，糖类 Xg，热量 X千卡
                晚餐：蛋白质 Xg，碳水 Xg，脂肪 Xg，膳食纤维 Xg，糖类 Xg，热量 X千卡

                周食谱：
                星期一
                早餐：早餐主食1+数量、早餐主食2+数量、早餐饮品+数量
                午餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬
                晚餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬

                星期二
                早餐：早餐主食1+数量、早餐主食2+数量、早餐饮品+数量
                午餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬
                晚餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬

                星期三
                早餐：早餐主食1+数量、早餐主食2+数量、早餐饮品+数量
                午餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬
                晚餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬

                星期四
                早餐：早餐主食1+数量、早餐主食2+数量、早餐饮品+数量
                午餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬
                晚餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬

                星期五
                早餐：早餐主食1+数量、早餐主食2+数量、早餐饮品+数量
                午餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬
                晚餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬

                星期六
                早餐：早餐主食1+数量、早餐主食2+数量、早餐饮品+数量
                午餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬
                晚餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬

                星期日
                早餐：早餐主食1+数量、早餐主食2+数量、早餐饮品+数量
                午餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬
                晚餐：午晚餐主食、肉类菜式1、肉类菜式2、炒时蔬

                ═══════════════════════════════════════════════════════════════
                【特别要求 - 每次生成必须不同】
                ═══════════════════════════════════════════════════════════════
                1. 从可用食谱库中选择不同的菜品组合
                2. 优先选择之前未使用过的菜品
                3. 早餐主食要有所变化
                4. 午餐和晚餐的肉类菜式要轮换使用不同的菜品

                ═══════════════════════════════════════════════════════════════
                现在请严格按照以上规则和格式，为用户条件 {combo_text} 制定一周食谱。
                记住：
                - 同一天同一餐的所有组合，肉类菜式和菜类菜式必须完全一样！只有主食可以不同！
                - 菜类固定为炒时蔬！
                - 每天必须有一餐包含炒蛋！
                - 早餐水煮蛋固定为2个！
                ═══════════════════════════════════════════════════════════════
                """

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是营养师。直接按要求输出，不要添加任何解释或额外文字。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3500
                )

                result = response.choices[0].message.content

                structured_data, structured_data_with_g= self.parse_ai_response(result, combo_text)
                all_results.append(result)
                all_structured_data.append(structured_data)
                all_structured_data_with_g.append(structured_data_with_g)

            final_result = "\n\n".join(all_results)

            all_structured_data_with_g = self.enforce_meal_consistency(all_structured_data_with_g)
            all_structured_data_with_g = self.enforce_breakfast_drink_consistency(all_structured_data_with_g)
            all_structured_data_with_g = self.enforce_breakfast_egg_consistency(all_structured_data_with_g)

            self.finished.emit(True, final_result, all_structured_data_with_g)

        except Exception as e:
            self.finished.emit(False, str(e), {})

class AIPlannerWidget(QWidget):
    """AI搭配界面"""

    def __init__(self):
        super().__init__()
        self.categories = []  # 存储分类标签列表
        self.setup_ui()
        self.api_key = "sk-2d0a9f8be62343e08de2c623aeb75c5a"
        self.current_structured_data = []
        self.setup_connections()

    def setup_ui(self):
        # 设置背景颜色（浅色渐变）
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #e8f4f8, stop:1 #d1e9f2);
                border-radius: 10px;
            }
        """)

        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 标题（居中）
        title = QLabel("🤖 AI 搭配")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #bdc3c7; max-height: 2px;")
        layout.addWidget(line)

        # + 按钮行（左上角）
        button_row = QHBoxLayout()
        self.add_btn = QPushButton("大类 +")
        self.add_btn.setFixedSize(100, 40)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        button_row.addWidget(self.add_btn)
        button_row.addStretch()
        layout.addLayout(button_row)

        # 内容区域（滚动区域）
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: none;
                border-radius: 10px;
            }
        """)

        # 分类容器
        self.categories_widget = QWidget()
        self.categories_layout = QGridLayout(self.categories_widget)
        self.categories_layout.setContentsMargins(20, 20, 20, 20)
        self.categories_layout.setSpacing(15)
        self.categories_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.content_area.setWidget(self.categories_widget)
        layout.addWidget(self.content_area, stretch=1)

        # 底部按钮区域
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        bottom_layout.setContentsMargins(0, 10, 0, 0)

        # 生成食谱按钮
        self.generate_btn = QPushButton("✨ 生成食谱")
        self.generate_btn.setFixedSize(180, 50)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
            QPushButton:pressed {
                background-color: #6A1B9A;
            }
        """)

        # 导入食谱按钮
        self.import_btn = QPushButton("📁 导入食谱")
        self.import_btn.setFixedSize(180, 50)
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
        """)

        # 添加弹性空间，让按钮居中
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.generate_btn)
        bottom_layout.addSpacing(30)
        bottom_layout.addWidget(self.import_btn)
        bottom_layout.addStretch()

        layout.addLayout(bottom_layout)

    def get_selected_combination(self):
        """获取用户选择的细类组合 - 返回笛卡尔积"""
        categories = []
        sub_items_list = []

        for container in self.categories:
            for child in container.findChildren(QPushButton):
                if hasattr(child, 'category_name'):
                    category_name = child.category_name
                    sub_items = getattr(child, 'sub_items', [])
                    sub_names = []
                    for sub_item in sub_items:
                        name_label = sub_item.findChild(QLabel)
                        if name_label:
                            sub_names.append(name_label.text())
                    if sub_names:
                        categories.append(category_name)
                        sub_items_list.append(sub_names)
                    break

        if not categories:
            return []

        # 生成笛卡尔积
        from itertools import product
        combinations = list(product(*sub_items_list))

        result = []
        for combo in combinations:
            combo_dict = {}
            for i, category in enumerate(categories):
                combo_dict[category] = combo[i]
            result.append(combo_dict)

        return result

    def show_recipe_result(self, result_text):
        """显示生成的食谱结果 - 美化版"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setMinimumSize(800, 650)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
            }
            QTextEdit {
                background-color: #fafafa;
                color: #333;
                font-size: 13px;
                font-family: Microsoft YaHei;
                border: none;
                padding: 20px;
                line-height: 1.8;
            }
            QScrollArea {
                background-color: #fafafa;
                border: none;
            }
            QPushButton {
                background-color: #9C27B0;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #e0e0e0;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9e9e9e;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #9C27B0; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 20, 25, 25)
        content_layout.setSpacing(15)

        # 标题行
        title_layout = QHBoxLayout()

        icon_label = QLabel("📅")
        icon_label.setStyleSheet("font-size: 32px;")
        title_layout.addWidget(icon_label)

        title_label = QLabel("AI 智能搭配的一周食谱")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #9C27B0;")
        title_layout.addWidget(title_label)

        title_layout.addStretch()
        content_layout.addLayout(title_layout)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e0e0e0; max-height: 1px;")
        content_layout.addWidget(line)

        # 结果显示区域（带滚动）
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #fafafa;
                border: 1px solid #eee;
                border-radius: 12px;
            }
        """)

        result_display = QTextEdit()
        result_display.setPlainText(result_text)
        result_display.setReadOnly(True)
        result_display.setStyleSheet("""
            QTextEdit {
                background-color: #fafafa;
                color: #333;
                font-size: 13px;
                font-family: Microsoft YaHei;
                border: none;
                padding: 20px;
                line-height: 1.8;
            }
        """)

        scroll_area.setWidget(result_display)
        content_layout.addWidget(scroll_area, 1)

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        # 复制按钮
        copy_btn = QPushButton("📋 复制内容")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
        """)
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(result_text, dialog))

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
                padding: 8px 25px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        close_btn.clicked.connect(dialog.accept)

        btn_layout.addWidget(copy_btn)
        btn_layout.addSpacing(15)
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        dialog.exec()

    def setup_connections(self):
        """设置信号连接"""
        self.add_btn.clicked.connect(self.show_input_dialog)
        self.generate_btn.clicked.connect(self.on_generate_clicked)
        self.import_btn.clicked.connect(self.on_import_clicked)

    def on_generate_clicked(self):
        """生成食谱按钮点击事件"""
        # 获取用户选择的组合（笛卡尔积）
        combinations = self.get_selected_combination()

        if not combinations:
            QMessageBox.warning(self, "警告", "请先添加大类并选择细类！")
            return

        # 构建选择的文本
        selected_text = ""
        for combo in combinations:
            combo_text = " + ".join([f"{cat}:{value}" for cat, value in combo.items()])
            selected_text += f"• {combo_text}\n"

        # 创建自定义确认对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(550, 450)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                color: #333;
            }
            QPushButton {
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
            QScrollArea {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }
            QScrollBar:vertical {
                width: 6px;
                background: #e0e0e0;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                border-radius: 3px;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #9C27B0; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(35, 30, 35, 35)

        # 图标
        icon_label = QLabel("✨")
        icon_label.setStyleSheet("font-size: 52px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("确认生成食谱")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #9C27B0;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e0e0e0; max-height: 1px;")
        content_layout.addWidget(line)

        # 提示信息
        info_label = QLabel(f"将生成 {len(combinations)} 种组合的食谱：")
        info_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
            font-weight: bold;
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(info_label)

        # 选择内容显示区域
        scroll_area = QScrollArea()
        scroll_area.setFixedHeight(150)

        selected_widget = QWidget()
        selected_layout = QVBoxLayout(selected_widget)
        selected_layout.setContentsMargins(15, 15, 15, 15)
        selected_layout.setSpacing(10)

        for combo in combinations:
            combo_text = " + ".join([f"{cat}:{value}" for cat, value in combo.items()])
            combo_label = QLabel(f"• {combo_text}")
            combo_label.setStyleSheet("""
                font-size: 13px;
                color: #333;
                background: transparent;
            """)
            selected_layout.addWidget(combo_label)

        selected_layout.addStretch()
        scroll_area.setWidget(selected_widget)
        content_layout.addWidget(scroll_area)

        # 询问信息
        ask_label = QLabel("是否根据这些条件生成一周食谱？")
        ask_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)
        ask_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(ask_label)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.addStretch()

        confirm_btn = QPushButton("确认生成")
        confirm_btn.setFixedSize(130, 44)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        confirm_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(confirm_btn)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(130, 44)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #666;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        if dialog.exec() == QDialog.Accepted:
            # 禁用按钮，显示加载状态
            self.generate_btn.setEnabled(False)
            self.generate_btn.setText("⏳ AI 生成中...")

            # 在新线程中调用API
            self.ai_thread = QThread()
            self.ai_worker = AIRecipeWorker(self.api_key, combinations)
            self.ai_worker.moveToThread(self.ai_thread)
            self.ai_thread.started.connect(self.ai_worker.run)
            self.ai_worker.finished.connect(self.on_ai_response)
            self.ai_worker.finished.connect(self.ai_thread.quit)
            self.ai_worker.finished.connect(self.ai_worker.deleteLater)
            self.ai_thread.finished.connect(self.ai_thread.deleteLater)
            self.ai_thread.start()

    def on_api_response(self, success, message):
        """API响应回调"""
        # 恢复按钮状态
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("✨ 生成食谱")

        if success:
            QMessageBox.information(self, "DeepSeek 响应", f"✅ 连接成功！\n\nDeepSeek 回复：\n{message}")
        else:
            QMessageBox.critical(self, "连接失败", f"❌ DeepSeek API 连接失败！\n\n错误信息：\n{message}")

    def on_ai_response(self, success, message, structured_data):
        """AI生成食谱响应回调"""
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("✨ 生成食谱")

        if success:
            self.current_structured_data = structured_data
            self.show_recipe_result_with_excel(message, structured_data)
        else:
            QMessageBox.critical(self, "生成失败", f"AI 生成食谱失败！\n\n错误信息：\n{message}")

    def show_input_dialog(self):
        """显示输入对话框（美化版）"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(450, 340)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QLineEdit {
                background-color: #f8f9fa;
                color: #333;
                padding: 12px 16px;
                font-size: 14px;
                border: 2px solid #e9ecef;
                border-radius: 12px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                background-color: white;
            }
            QPushButton {
                border: none;
                border-radius: 22px;
                font-weight: bold;
                font-size: 14px;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #2196F3; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(35, 30, 35, 35)

        # 图标
        icon_label = QLabel("📁")
        icon_label.setStyleSheet("font-size: 52px; background: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("添加大类")
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            background: transparent;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #ecf0f1; max-height: 1px;")
        content_layout.addWidget(line)

        # 提示标签
        hint_label = QLabel("请输入大类的名称：")
        hint_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
            background: transparent;
        """)
        content_layout.addWidget(hint_label)

        # 输入框
        input_edit = QLineEdit()
        input_edit.setPlaceholderText("例如：体质类型、训练目标等")
        input_edit.setMinimumHeight(48)
        input_edit.returnPressed.connect(dialog.accept)
        content_layout.addWidget(input_edit)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.addStretch()

        # 确定按钮
        ok_btn = QPushButton("确 定")
        ok_btn.setFixedSize(130, 44)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        ok_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(ok_btn)

        # 取消按钮
        cancel_btn = QPushButton("取 消")
        cancel_btn.setFixedSize(130, 44)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ecf0f1;
                color: #7f8c8d;
            }
            QPushButton:hover {
                background-color: #dfe6e9;
                color: #2c3e50;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        # 设置输入框焦点
        input_edit.setFocus()

        # 显示对话框并获取输入
        if dialog.exec() == QDialog.Accepted:
            text = input_edit.text().strip()
            if text:
                self.add_category(text)

    def add_category(self, category_name):
        """添加分类标签"""
        # 创建容器（包含按钮和细类区域）
        container = QWidget()
        container.setFixedWidth(240)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # 主按钮容器（包含大类名、编辑、删除、箭头）
        btn_container = QWidget()
        btn_container.setFixedSize(240, 50)
        btn_container.setStyleSheet("""
            QWidget {
                background-color: #e3f2fd;
                border: 2px solid #90caf9;
                border-radius: 25px;
            }
            QWidget:hover {
                background-color: #bbdefb;
                border-color: #64b5f6;
            }
        """)

        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(15, 0, 10, 0)
        btn_layout.setSpacing(8)

        # 大类名称标签
        name_label = QLabel(category_name)
        name_label.setStyleSheet("""
            QLabel {
                color: #1976d2;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)

        # 编辑按钮
        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(32, 32)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                border: none;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # 删除按钮
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(32, 32)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                border: none;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        # 展开/收起箭头按钮
        arrow_btn = QPushButton("▶")
        arrow_btn.setFixedSize(32, 32)
        arrow_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #1976d2;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.08);
            }
        """)

        btn_layout.addWidget(name_label)
        btn_layout.addStretch()
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(arrow_btn)

        # 细类下拉区域（整体容器，初始隐藏）
        dropdown_area = QWidget()
        dropdown_area.setVisible(False)
        dropdown_area.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }
        """)
        dropdown_layout = QVBoxLayout(dropdown_area)
        dropdown_layout.setContentsMargins(8, 8, 8, 8)
        dropdown_layout.setSpacing(8)

        # 细类滚动区域
        sub_scroll = QScrollArea()
        sub_scroll.setFixedHeight(130)
        sub_scroll.setWidgetResizable(True)
        sub_scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                width: 6px;
                background: #e8e8e8;
                border-radius: 3px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9e9e9e;
            }
        """)

        # 细类内容容器
        sub_content = QWidget()
        sub_content.setStyleSheet("background-color: transparent;")
        sub_layout = QVBoxLayout(sub_content)
        sub_layout.setContentsMargins(4, 4, 4, 4)
        sub_layout.setSpacing(6)
        sub_layout.addStretch()

        sub_scroll.setWidget(sub_content)

        # 存储细类按钮的列表
        sub_items = []

        # 添加细类的按钮
        add_sub_btn = QPushButton("+ 添加细类")
        add_sub_btn.setFixedHeight(36)
        add_sub_btn.setStyleSheet("""
            QPushButton {
                background-color: #e3f2fd;
                color: #1976d2;
                font-size: 13px;
                font-weight: bold;
                border: 1px dashed #90caf9;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: #bbdefb;
                border: 1px solid #64b5f6;
            }
        """)

        dropdown_layout.addWidget(sub_scroll)
        dropdown_layout.addWidget(add_sub_btn)

        layout.addWidget(btn_container)
        layout.addWidget(dropdown_area)

        # 记录展开状态和相关组件
        setattr(arrow_btn, 'expanded', False)
        setattr(arrow_btn, 'dropdown_area', dropdown_area)
        setattr(arrow_btn, 'sub_layout', sub_layout)
        setattr(arrow_btn, 'container', container)
        setattr(arrow_btn, 'name_label', name_label)
        setattr(arrow_btn, 'category_name', category_name)
        setattr(arrow_btn, 'sub_items', sub_items)
        setattr(arrow_btn, 'add_sub_btn', add_sub_btn)

        def add_sub_category():
            """添加细类"""
            if len(sub_items) >= 5:
                # 创建自定义警告对话框
                warn_dialog = QDialog(container)
                warn_dialog.setWindowTitle("")
                warn_dialog.setModal(True)
                warn_dialog.setFixedSize(420, 300)
                warn_dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
                warn_dialog.setStyleSheet("""
                    QDialog {
                        background-color: white;
                        border-radius: 20px;
                    }
                """)

                # 主布局
                main_layout = QVBoxLayout(warn_dialog)
                main_layout.setSpacing(0)
                main_layout.setContentsMargins(0, 0, 0, 0)

                # 顶部装饰条
                top_bar = QWidget()
                top_bar.setFixedHeight(8)
                top_bar.setStyleSheet("background-color: #ff9800; border-radius: 20px 20px 0 0;")
                main_layout.addWidget(top_bar)

                # 内容区域
                content_widget = QWidget()
                content_layout = QVBoxLayout(content_widget)
                content_layout.setSpacing(15)
                content_layout.setContentsMargins(40, 25, 40, 35)

                # 图标
                icon_label = QLabel("⚠️")
                icon_label.setStyleSheet("font-size: 56px; background: transparent;")
                icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                content_layout.addWidget(icon_label)

                # 标题
                title_label = QLabel("无法添加")
                title_label.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: #2c3e50;
                    background: transparent;
                """)
                title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                content_layout.addWidget(title_label)

                # 分隔线
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setStyleSheet("background-color: #ecf0f1; max-height: 1px;")
                content_layout.addWidget(line)

                # 警告信息
                msg_label = QLabel("最多只能添加 5 个细类！")
                msg_label.setStyleSheet("""
                    font-size: 16px;
                    font-weight: bold;
                    color: #ff9800;
                    background: #fff3e0;
                    padding: 12px 20px;
                    border-radius: 12px;
                """)
                msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                content_layout.addWidget(msg_label)

                # 提示信息
                hint_label = QLabel(f"当前已有 {len(sub_items)} 个细类，已达到上限")
                hint_label.setStyleSheet("""
                    font-size: 13px;
                    color: #7f8c8d;
                    background: transparent;
                """)
                hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                content_layout.addWidget(hint_label)

                content_layout.addStretch()

                # 按钮区域
                btn_layout = QHBoxLayout()
                btn_layout.addStretch()

                # 确定按钮
                ok_btn = QPushButton("知道了")
                ok_btn.setFixedSize(150, 44)
                ok_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ff9800;
                        color: white;
                        font-size: 14px;
                        font-weight: bold;
                        border: none;
                        border-radius: 22px;
                    }
                    QPushButton:hover {
                        background-color: #f57c00;
                    }
                """)
                ok_btn.clicked.connect(warn_dialog.accept)
                btn_layout.addWidget(ok_btn)

                btn_layout.addStretch()
                content_layout.addLayout(btn_layout)

                main_layout.addWidget(content_widget)

                warn_dialog.exec()
                return

            # 创建细类输入对话框（原有代码保持不变）
            dialog = QDialog(container)
            dialog.setWindowTitle("")
            dialog.setModal(True)
            dialog.setFixedSize(450, 340)
            dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
            dialog.setStyleSheet("""
                QDialog {
                    background-color: white;
                    border-radius: 20px;
                }
            """)

            # 主布局
            main_layout = QVBoxLayout(dialog)
            main_layout.setSpacing(0)
            main_layout.setContentsMargins(0, 0, 0, 0)

            # 顶部装饰条
            top_bar = QWidget()
            top_bar.setFixedHeight(8)
            top_bar.setStyleSheet("background-color: #4CAF50; border-radius: 20px 20px 0 0;")
            main_layout.addWidget(top_bar)

            # 内容区域
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(15)
            content_layout.setContentsMargins(40, 25, 40, 35)

            # 图标
            icon_label = QLabel("📝")
            icon_label.setStyleSheet("font-size: 52px; background: transparent;")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(icon_label)

            # 标题
            title_label = QLabel("添加细类")
            title_label.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                background: transparent;
            """)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(title_label)

            # 分隔线
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("background-color: #ecf0f1; max-height: 1px;")
            content_layout.addWidget(line)

            # 所属大类提示
            category_label = QLabel(f"为「{arrow_btn.category_name}」添加细类")
            category_label.setStyleSheet("""
                font-size: 14px;
                color: #2c3e50;
                background: #e8f5e9;
                padding: 10px 20px;
                border-radius: 12px;
            """)
            category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            category_label.setWordWrap(True)
            content_layout.addWidget(category_label)

            # 输入框
            input_edit = QLineEdit()
            input_edit.setPlaceholderText("请输入细类名称")
            input_edit.setMinimumHeight(48)
            input_edit.setStyleSheet("""
                QLineEdit {
                    padding: 12px 16px;
                    font-size: 14px;
                    color: #333;
                    background-color: #f8f9fa;
                    border: 2px solid #e9ecef;
                    border-radius: 12px;
                }
                QLineEdit:focus {
                    border-color: #4CAF50;
                    background-color: white;
                }
            """)
            input_edit.returnPressed.connect(dialog.accept)
            content_layout.addWidget(input_edit)

            # 计数器显示
            count_label = QLabel(f"当前已有 {len(sub_items)} / 5 个细类")
            count_label.setStyleSheet("""
                font-size: 12px;
                color: #7f8c8d;
                background: transparent;
            """)
            count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(count_label)

            content_layout.addStretch()

            # 按钮区域
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(15)
            btn_layout.addStretch()

            # 确定按钮
            ok_btn = QPushButton("添 加")
            ok_btn.setFixedSize(140, 44)
            ok_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 22px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            ok_btn.clicked.connect(dialog.accept)
            btn_layout.addWidget(ok_btn)

            # 取消按钮
            cancel_btn = QPushButton("取 消")
            cancel_btn.setFixedSize(140, 44)
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ecf0f1;
                    color: #7f8c8d;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 22px;
                }
                QPushButton:hover {
                    background-color: #dfe6e9;
                    color: #2c3e50;
                }
            """)
            cancel_btn.clicked.connect(dialog.reject)
            btn_layout.addWidget(cancel_btn)

            btn_layout.addStretch()
            content_layout.addLayout(btn_layout)

            main_layout.addWidget(content_widget)

            # 设置输入框焦点
            input_edit.setFocus()

            if dialog.exec() == QDialog.Accepted:
                sub_name = input_edit.text().strip()
                if sub_name:
                    # 创建细类项
                    sub_item = QWidget()
                    sub_item.setStyleSheet("""
                        QWidget {
                            background-color: #e8f5e9;
                            border: 1px solid #c8e6c9;
                            border-radius: 10px;
                        }
                    """)
                    sub_item_layout = QHBoxLayout(sub_item)
                    sub_item_layout.setContentsMargins(12, 8, 8, 8)
                    sub_item_layout.setSpacing(8)

                    # 细类名称
                    sub_name_label = QLabel(sub_name)
                    sub_name_label.setStyleSheet("""
                        QLabel {
                            color: #2e7d32;
                            font-size: 13px;
                            font-weight: 500;
                            background: transparent;
                            border: none;
                        }
                    """)

                    # 删除按钮
                    sub_del_btn = QPushButton("✕")
                    sub_del_btn.setFixedSize(24, 24)
                    sub_del_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #ffcdd2;
                            color: #c62828;
                            font-size: 12px;
                            font-weight: bold;
                            border: none;
                            border-radius: 12px;
                        }
                        QPushButton:hover {
                            background-color: #ef9a9a;
                            color: #b71c1c;
                        }
                    """)

                    sub_item_layout.addWidget(sub_name_label)
                    sub_item_layout.addStretch()
                    sub_item_layout.addWidget(sub_del_btn)

                    def delete_sub():
                        sub_item.deleteLater()
                        sub_items.remove(sub_item)

                    sub_del_btn.clicked.connect(delete_sub)

                    # 在stretch之前插入
                    sub_layout.insertWidget(len(sub_items), sub_item)
                    sub_items.append(sub_item)

        def on_arrow_click():
            arrow_btn.expanded = not arrow_btn.expanded

            if arrow_btn.expanded:
                arrow_btn.setText("▼")
                dropdown_area.setVisible(True)
                container.setFixedHeight(50 + dropdown_area.sizeHint().height() + 8)
            else:
                arrow_btn.setText("▶")
                dropdown_area.setVisible(False)
                container.setFixedHeight(50)

        def on_edit():
            """编辑大类名称"""
            dialog = QDialog(container)
            dialog.setWindowTitle("")
            dialog.setModal(True)
            dialog.setFixedSize(450, 320)
            dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
            dialog.setStyleSheet("""
                QDialog {
                    background-color: white;
                    border-radius: 20px;
                }
            """)

            # 主布局
            main_layout = QVBoxLayout(dialog)
            main_layout.setSpacing(0)
            main_layout.setContentsMargins(0, 0, 0, 0)

            # 顶部装饰条
            top_bar = QWidget()
            top_bar.setFixedHeight(8)
            top_bar.setStyleSheet("background-color: #2196F3; border-radius: 20px 20px 0 0;")
            main_layout.addWidget(top_bar)

            # 内容区域
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(20)
            content_layout.setContentsMargins(35, 30, 35, 35)

            # 图标
            icon_label = QLabel("✏️")
            icon_label.setStyleSheet("font-size: 52px; background: transparent;")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(icon_label)

            # 标题
            title_label = QLabel("编辑大类")
            title_label.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                background: transparent;
            """)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(title_label)

            # 当前名称提示
            current_label = QLabel(f"当前名称：{arrow_btn.category_name}")
            current_label.setStyleSheet("""
                font-size: 13px;
                color: #7f8c8d;
                background: #f8f9fa;
                padding: 8px 16px;
                border-radius: 20px;
            """)
            current_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            current_label.setWordWrap(True)
            content_layout.addWidget(current_label)

            # 输入框 - 确保完全显示
            input_edit = QLineEdit()
            input_edit.setText(arrow_btn.category_name)
            input_edit.setPlaceholderText("请输入新的大类名称")
            input_edit.setMinimumHeight(48)
            input_edit.setStyleSheet("""
                QLineEdit {
                    padding: 12px 16px;
                    font-size: 14px;
                    color: #333;
                    background-color: #f8f9fa;
                    border: 2px solid #e9ecef;
                    border-radius: 12px;
                }
                QLineEdit:focus {
                    border-color: #2196F3;
                    background-color: white;
                }
            """)
            input_edit.returnPressed.connect(dialog.accept)
            content_layout.addWidget(input_edit)

            content_layout.addStretch()

            # 按钮区域
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(15)
            btn_layout.addStretch()

            # 确定按钮
            ok_btn = QPushButton("保 存")
            ok_btn.setFixedSize(140, 44)
            ok_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 22px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            ok_btn.clicked.connect(dialog.accept)
            btn_layout.addWidget(ok_btn)

            # 取消按钮
            cancel_btn = QPushButton("取 消")
            cancel_btn.setFixedSize(140, 44)
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ecf0f1;
                    color: #7f8c8d;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 22px;
                }
                QPushButton:hover {
                    background-color: #dfe6e9;
                    color: #2c3e50;
                }
            """)
            cancel_btn.clicked.connect(dialog.reject)
            btn_layout.addWidget(cancel_btn)

            btn_layout.addStretch()
            content_layout.addLayout(btn_layout)

            main_layout.addWidget(content_widget)

            # 设置输入框焦点并选中所有文本
            input_edit.setFocus()
            input_edit.selectAll()

            if dialog.exec() == QDialog.Accepted:
                new_name = input_edit.text().strip()
                if new_name and new_name != arrow_btn.category_name:
                    arrow_btn.category_name = new_name
                    name_label.setText(new_name)

        def on_delete():
            """删除大类"""
            dialog = QDialog(container)
            dialog.setWindowTitle("")
            dialog.setModal(True)
            dialog.setFixedSize(450, 340)
            dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
            dialog.setStyleSheet("""
                QDialog {
                    background-color: white;
                    border-radius: 20px;
                }
            """)

            # 主布局
            main_layout = QVBoxLayout(dialog)
            main_layout.setSpacing(0)
            main_layout.setContentsMargins(0, 0, 0, 0)

            # 顶部装饰条
            top_bar = QWidget()
            top_bar.setFixedHeight(8)
            top_bar.setStyleSheet("background-color: #f44336; border-radius: 20px 20px 0 0;")
            main_layout.addWidget(top_bar)

            # 内容区域
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(20)
            content_layout.setContentsMargins(35, 30, 35, 35)

            # 图标
            icon_label = QLabel("⚠️")
            icon_label.setStyleSheet("font-size: 56px; background: transparent;")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(icon_label)

            # 标题
            title_label = QLabel("确认删除")
            title_label.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                background: transparent;
            """)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(title_label)

            # 分隔线
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("background-color: #ecf0f1; max-height: 1px; margin: 5px 0;")
            content_layout.addWidget(line)

            # 要删除的分类名称
            category_label = QLabel(f"「{arrow_btn.category_name}」")
            category_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #f44336;
                background: #ffebee;
                padding: 10px 20px;
                border-radius: 12px;
            """)
            category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            category_label.setWordWrap(True)
            content_layout.addWidget(category_label)

            # 提示信息
            msg_label = QLabel("确定要删除此大类吗？")
            msg_label.setStyleSheet("""
                font-size: 14px;
                color: #555;
                background: transparent;
            """)
            msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(msg_label)

            # 警告信息
            warning_label = QLabel("⚠️ 此操作将同时删除该大类下的所有细类，且不可恢复！")
            warning_label.setStyleSheet("""
                font-size: 12px;
                color: #c62828;
                background: #ffebee;
                padding: 10px 15px;
                border-radius: 10px;
            """)
            warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            warning_label.setWordWrap(True)
            content_layout.addWidget(warning_label)

            content_layout.addStretch()

            # 按钮区域
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(15)
            btn_layout.addStretch()

            # 确认删除按钮
            confirm_btn = QPushButton("确认删除")
            confirm_btn.setFixedSize(140, 44)
            confirm_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 22px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            confirm_btn.clicked.connect(dialog.accept)
            btn_layout.addWidget(confirm_btn)

            # 取消按钮
            cancel_btn = QPushButton("取 消")
            cancel_btn.setFixedSize(140, 44)
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ecf0f1;
                    color: #7f8c8d;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 22px;
                }
                QPushButton:hover {
                    background-color: #dfe6e9;
                    color: #2c3e50;
                }
            """)
            cancel_btn.clicked.connect(dialog.reject)
            btn_layout.addWidget(cancel_btn)

            btn_layout.addStretch()
            content_layout.addLayout(btn_layout)

            main_layout.addWidget(content_widget)

            if dialog.exec() == QDialog.Accepted:
                # 从网格布局中移除
                for i in range(self.categories_layout.count()):
                    item = self.categories_layout.itemAt(i)
                    if item and item.widget() == container:
                        self.categories_layout.removeWidget(container)
                        break
                # 删除容器
                container.deleteLater()
                # 从列表中移除
                if container in self.categories:
                    self.categories.remove(container)

        # 连接信号
        arrow_btn.clicked.connect(on_arrow_click)
        edit_btn.clicked.connect(on_edit)
        delete_btn.clicked.connect(on_delete)
        add_sub_btn.clicked.connect(add_sub_category)

        # 初始容器高度
        container.setFixedHeight(50)

        # 计算当前行列
        row = len(self.categories) // 4
        col = len(self.categories) % 4

        # 添加到网格布局
        self.categories_layout.addWidget(container, row, col)
        self.categories.append(container)

    def show_recipe_result_with_excel(self, result_text, structured_data):
        """显示生成的食谱结果，带Excel导出按钮"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setMinimumSize(850, 700)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
            }
            QTextEdit {
                background-color: #fafafa;
                color: #333;
                font-size: 13px;
                font-family: Microsoft YaHei;
                border: none;
                padding: 20px;
                line-height: 1.8;
            }
            QScrollArea {
                background-color: #fafafa;
                border: none;
            }
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
                padding: 10px 25px;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #e0e0e0;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                border-radius: 4px;
            }
        """)

        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #9C27B0; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 20, 25, 25)
        content_layout.setSpacing(15)

        # 标题行
        title_layout = QHBoxLayout()
        icon_label = QLabel("📅")
        icon_label.setStyleSheet("font-size: 32px;")
        title_layout.addWidget(icon_label)

        title_label = QLabel("AI 搭配周食谱")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #9C27B0;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        content_layout.addLayout(title_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e0e0e0; max-height: 1px;")
        content_layout.addWidget(line)

        # 结果显示区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #fafafa;
                border: 1px solid #eee;
                border-radius: 12px;
            }
        """)

        result_display = QTextEdit()
        result_display.setPlainText(result_text)
        result_display.setReadOnly(True)
        result_display.setStyleSheet("""
            QTextEdit {
                background-color: #fafafa;
                color: #333;
                font-size: 13px;
                font-family: Microsoft YaHei;
                border: none;
                padding: 20px;
                line-height: 1.8;
            }
        """)

        scroll_area.setWidget(result_display)
        content_layout.addWidget(scroll_area, 1)

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        copy_btn = QPushButton("📋 复制内容")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
        """)

        copy_btn.clicked.connect(lambda checked, t=result_text, d=dialog: self.copy_to_clipboard(t, d))

        excel_btn = QPushButton("📊 导出Excel表格")
        excel_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        # 修复：使用默认参数捕获变量值
        excel_btn.clicked.connect(lambda checked, d=structured_data: self.export_to_excel(d))

        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        close_btn.clicked.connect(dialog.accept)

        btn_layout.addWidget(copy_btn)
        btn_layout.addSpacing(15)
        btn_layout.addWidget(excel_btn)
        btn_layout.addSpacing(15)
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)
        dialog.exec()

    def export_to_excel(self, structured_data):
        """导出为Excel表格"""
        if not structured_data:
            QMessageBox.warning(self, "警告", "没有可导出的数据！")
            return

        if isinstance(structured_data, list):
            data_list = structured_data
        elif isinstance(structured_data, dict):
            data_list = [structured_data]
        else:
            QMessageBox.warning(self, "错误", f"数据格式错误：{type(structured_data)}")
            return

        try:
            generator = MealPlanExcelGenerator()
            filepath = generator.generate_excel(data_list)

            if filepath:
                # 美化成功弹窗
                self.show_export_success_dialog(filepath)
            else:
                QMessageBox.warning(self, "导出失败", "生成Excel表格失败！")

        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出Excel失败：\n{str(e)}")
            traceback.print_exc()

    def show_export_success_dialog(self, filepath):
        """显示导出成功的美化弹窗"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(450, 380)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QPushButton {
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #4CAF50; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(40, 35, 40, 35)

        # 成功图标
        icon_label = QLabel("📊")
        icon_label.setStyleSheet("font-size: 64px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("导出成功！")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e8e8e8; max-height: 1px; margin: 5px 0;")
        content_layout.addWidget(line)

        # 文件信息
        filename = os.path.basename(filepath)
        file_dir = os.path.dirname(filepath)

        info_label = QLabel(f"文件已保存至：")
        info_label.setStyleSheet("font-size: 13px; color: #555;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(info_label)

        # 文件名（可复制）
        filename_label = QLabel(f"📄 {filename}")
        filename_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2196F3;
            background-color: #e3f2fd;
            padding: 8px 15px;
            border-radius: 10px;
        """)
        filename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filename_label.setWordWrap(True)
        content_layout.addWidget(filename_label)

        # 路径信息
        path_label = QLabel(f"位置：{file_dir}")
        path_label.setStyleSheet("""
            font-size: 11px;
            color: #888;
            background-color: #f5f5f5;
            padding: 8px 12px;
            border-radius: 8px;
        """)
        path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path_label.setWordWrap(True)
        content_layout.addWidget(path_label)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.addStretch()

        # 打开文件夹按钮
        open_folder_btn = QPushButton("📂 打开文件夹")
        open_folder_btn.setFixedSize(130, 44)
        open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 13px;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        open_folder_btn.clicked.connect(lambda: self._open_file_folder(filepath, dialog))

        # 确定按钮
        ok_btn = QPushButton("确 定")
        ok_btn.setFixedSize(130, 44)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        ok_btn.clicked.connect(dialog.accept)

        btn_layout.addWidget(open_folder_btn)
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        dialog.exec()

    def _open_file_folder(self, filepath, dialog):
        """打开文件所在文件夹"""
        import subprocess
        import platform

        file_dir = os.path.dirname(filepath)

        try:
            if platform.system() == "Windows":
                os.startfile(file_dir)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_dir])
            else:  # Linux
                subprocess.run(["xdg-open", file_dir])
        except Exception as e:
            QMessageBox.warning(self, "提示", f"无法打开文件夹：{str(e)}")

    def copy_to_clipboard(self, text, dialog):
        """复制内容到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        tip = QLabel("✅ 已复制到剪贴板", dialog)
        tip.setStyleSheet("""
            QLabel {
                background-color: #4CAF50;
                color: white;
                font-size: 12px;
                padding: 8px 15px;
                border-radius: 20px;
            }
        """)
        tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tip.adjustSize()
        tip.move(dialog.width() // 2 - tip.width() // 2, dialog.height() - 60)
        tip.show()
        QTimer.singleShot(1500, tip.deleteLater)

    def parse_excel_to_categories(self, df):
        """解析Excel，提取大类和小类"""
        try:
            # 查找包含分类信息的行（通常是早餐、午餐或晚餐的第一行数据）
            categories_data = {}

            # 遍历所有行，查找包含"/"的分类文本
            for row_idx in range(min(20, len(df))):  # 只查找前20行
                for col_idx in range(min(50, len(df.columns))):
                    cell_value = str(df.iloc[row_idx, col_idx]) if pd.notna(df.iloc[row_idx, col_idx]) else ""

                    # 查找包含分类格式的文本，如 "瘦弱/高：白米饭..."
                    if "：" in cell_value and "/" in cell_value:
                        # 提取所有组合条件
                        lines = cell_value.split('\n')
                        for line in lines:
                            if "：" in line and "/" in line:
                                # 提取冒号前的分类条件，如 "瘦弱/高"
                                combo_part = line.split("：")[0].strip()

                                # 按"/"分割得到各个细类
                                sub_categories = combo_part.split('/')

                                # 假设第一个细类对应第一个大类，第二个细类对应第二个大类...
                                for i, sub_cat in enumerate(sub_categories):
                                    category_key = f"要求{i + 1}"
                                    if category_key not in categories_data:
                                        categories_data[category_key] = set()
                                    categories_data[category_key].add(sub_cat)

                        # 找到第一个有效数据后就跳出
                        if categories_data:
                            break
                if categories_data:
                    break

            # 如果上述方法没找到，尝试另一种解析方式：从表头或特定位置读取
            if not categories_data:
                # 尝试从组合名称中解析（如果有的话）
                for row_idx in range(len(df)):
                    for col_idx in range(len(df.columns)):
                        cell_value = str(df.iloc[row_idx, col_idx]) if pd.notna(df.iloc[row_idx, col_idx]) else ""
                        # 查找类似 "组合1：瘦弱/高" 的格式
                        if "组合" in cell_value and "：" in cell_value and "/" in cell_value:
                            combo_part = cell_value.split("：")[1].strip()
                            sub_categories = combo_part.split('/')
                            for i, sub_cat in enumerate(sub_categories):
                                category_key = f"要求{i + 1}"
                                if category_key not in categories_data:
                                    categories_data[category_key] = set()
                                categories_data[category_key].add(sub_cat)

            # 将set转换为排序后的列表
            result = {}
            for key, value_set in categories_data.items():
                # 按照常见逻辑排序：瘦弱、肥胖、高、矮等
                sorted_list = sorted(list(value_set))
                result[key] = sorted_list

            return result

        except Exception as e:
            traceback.print_exc()
            return {}

    def show_import_confirm_dialog(self, categories_data):
        """显示导入确认对话框"""
        if not categories_data:
            QMessageBox.warning(self, "警告", "未能从Excel中解析出分类数据！")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(500, 450)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                color: #333;
            }
            QPushButton {
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
            QScrollArea {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }
        """)

        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #FF9800; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(35, 30, 35, 35)

        # 图标
        icon_label = QLabel("📁")
        icon_label.setStyleSheet("font-size: 52px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("导入分类配置")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #FF9800;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e0e0e0; max-height: 1px;")
        content_layout.addWidget(line)

        # 提示信息
        info_label = QLabel(f"将从Excel导入 {len(categories_data)} 个大类：")
        info_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
            font-weight: bold;
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(info_label)

        # 分类内容显示区域
        scroll_area = QScrollArea()
        scroll_area.setFixedHeight(180)

        categories_widget = QWidget()
        categories_layout = QVBoxLayout(categories_widget)
        categories_layout.setContentsMargins(15, 15, 15, 15)
        categories_layout.setSpacing(10)

        for cat_name, sub_list in categories_data.items():
            cat_label = QLabel(f"📌 {cat_name}：{', '.join(sub_list)}")
            cat_label.setStyleSheet("""
                font-size: 13px;
                color: #333;
                background: #f8f9fa;
                padding: 8px 12px;
                border-radius: 8px;
            """)
            cat_label.setWordWrap(True)
            categories_layout.addWidget(cat_label)

        categories_layout.addStretch()
        scroll_area.setWidget(categories_widget)
        content_layout.addWidget(scroll_area)

        # 询问信息
        ask_label = QLabel("是否导入这些分类？")
        ask_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)
        ask_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(ask_label)

        # 提示：将清空现有分类
        if self.categories:
            warning_label = QLabel("⚠️ 导入将清空当前已添加的所有分类！")
            warning_label.setStyleSheet("""
                font-size: 12px;
                color: #f44336;
                background: #ffebee;
                padding: 8px 15px;
                border-radius: 20px;
            """)
            warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            warning_label.setWordWrap(True)
            content_layout.addWidget(warning_label)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.addStretch()

        confirm_btn = QPushButton("确认导入")
        confirm_btn.setFixedSize(130, 44)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        confirm_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(confirm_btn)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(130, 44)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #666;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        if dialog.exec() == QDialog.Accepted:
            # 清空现有分类
            self.clear_all_categories()
            # 添加新分类
            for cat_name, sub_list in categories_data.items():
                self.add_category(cat_name)
                # 获取刚添加的container并添加细类
                if self.categories:
                    container = self.categories[-1]
                    for child in container.findChildren(QPushButton):
                        if hasattr(child, 'category_name') and child.category_name == cat_name:
                            # 找到对应的arrow_btn，添加细类
                            for sub_name in sub_list:
                                self.add_sub_category_to_container(child, sub_name)
                            break

        return categories_data

    def clear_all_categories(self):
        """清空所有已添加的分类"""
        for container in self.categories[:]:
            container.deleteLater()
        self.categories.clear()

    def add_sub_category_to_container(self, arrow_btn, sub_name):
        """向指定容器添加细类"""
        if not hasattr(arrow_btn, 'sub_items'):
            return

        sub_items = arrow_btn.sub_items
        sub_layout = arrow_btn.sub_layout

        # 检查是否已存在相同名称的细类
        for sub_item in sub_items:
            name_label = sub_item.findChild(QLabel)
            if name_label and name_label.text() == sub_name:
                return

        # 创建细类项
        sub_item = QWidget()
        sub_item.setStyleSheet("""
            QWidget {
                background-color: #e8f5e9;
                border: 1px solid #c8e6c9;
                border-radius: 10px;
            }
        """)
        sub_item_layout = QHBoxLayout(sub_item)
        sub_item_layout.setContentsMargins(12, 8, 8, 8)
        sub_item_layout.setSpacing(8)

        # 细类名称
        sub_name_label = QLabel(sub_name)
        sub_name_label.setStyleSheet("""
            QLabel {
                color: #2e7d32;
                font-size: 13px;
                font-weight: 500;
                background: transparent;
                border: none;
            }
        """)

        # 删除按钮
        sub_del_btn = QPushButton("✕")
        sub_del_btn.setFixedSize(24, 24)
        sub_del_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffcdd2;
                color: #c62828;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #ef9a9a;
                color: #b71c1c;
            }
        """)

        sub_item_layout.addWidget(sub_name_label)
        sub_item_layout.addStretch()
        sub_item_layout.addWidget(sub_del_btn)

        def delete_sub():
            sub_item.deleteLater()
            sub_items.remove(sub_item)

        sub_del_btn.clicked.connect(delete_sub)

        # 在stretch之前插入
        sub_layout.insertWidget(len(sub_items), sub_item)
        sub_items.append(sub_item)

    def on_import_clicked(self):
        """导入食谱按钮点击事件 - 从Excel导入细类配置"""
        # 弹出文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择Excel文件",
            "",
            "Excel文件 (*.xlsx *.xls)"
        )

        if not file_path:
            return

        try:
            # 读取Excel文件
            df = pd.read_excel(file_path, header=None)  # 不将第一行作为表头

            # 解析Excel，提取大类和小类
            categories_data = self.parse_excel_to_categories(df)

            if not categories_data:
                QMessageBox.warning(self, "警告",
                                    "Excel文件中没有找到有效的分类数据！\n\n请确保Excel中包含类似'瘦弱/高'格式的分类信息。")
                return

            # 显示导入确认对话框
            self.show_import_confirm_dialog(categories_data)

        except ImportError:
            QMessageBox.critical(self, "错误", "请先安装pandas库：pip install pandas openpyxl")
        except Exception as e:
            QMessageBox.critical(self, "导入失败", f"读取Excel文件失败：\n{str(e)}")
            traceback.print_exc()

class NutritionCalcWidget(QWidget):
    """营养计算界面"""

    def __init__(self):
        super().__init__()
        self.current_recipe_data = None
        self.nutrition_result = None
        self.setup_ui()

    def setup_ui(self):
        # 设置背景颜色（浅色渐变）
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #e8f8f0, stop:1 #d1f0e0);
                border-radius: 10px;
            }
        """)

        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 标题
        title = QLabel("🧮 营养计算")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #bdc3c7; max-height: 2px;")
        layout.addWidget(line)

        # 导入食谱按钮行
        import_layout = QHBoxLayout()
        import_layout.addStretch()

        self.import_btn = QPushButton("📁 导入食谱")
        self.import_btn.setFixedSize(160, 45)
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.import_btn.clicked.connect(self.on_import_clicked)
        import_layout.addWidget(self.import_btn)
        import_layout.addStretch()

        layout.addLayout(import_layout)

        # 内容区域
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: none;
                border-radius: 10px;
            }
        """)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(15)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.content_area.setWidget(self.content_widget)
        layout.addWidget(self.content_area, stretch=1)

        # 初始显示提示
        self.show_placeholder()

    def show_placeholder(self):
        """显示占位提示"""
        self.clear_content()
        placeholder = QLabel("📊 请导入食谱文件进行营养计算")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 16px; color: #7f8c8d; padding: 40px;")
        self.content_layout.addWidget(placeholder)

    def clear_content(self):
        """清空内容区域"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def on_import_clicked(self):
        """导入食谱按钮点击事件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择食谱Excel文件",
            "",
            "Excel文件 (*.xlsx *.xls)"
        )

        if not file_path:
            return

        try:
            # 读取Excel文件
            df = pd.read_excel(file_path, header=None)

            # 解析食谱数据
            recipe_data = self.parse_recipe_excel(df)

            if not recipe_data:
                QMessageBox.warning(self, "警告", "未能从Excel中解析出食谱数据！")
                return

            self.current_recipe_data = recipe_data

            # 计算营养成分
            self.nutrition_result = self.calculate_nutrition(recipe_data)

            if not self.nutrition_result:
                QMessageBox.warning(self, "警告", "营养计算失败！")
                return

            # 显示结果
            self.display_nutrition_result()

            # 美化成功弹窗
            self.show_calculation_success_dialog()

        except Exception as e:
            QMessageBox.critical(self, "导入失败", f"处理Excel文件失败：\n{str(e)}")
            traceback.print_exc()

    def show_calculation_success_dialog(self):
        """显示计算成功的美化弹窗"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(400, 320)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QPushButton {
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条（根据结果颜色不同）
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #4CAF50; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(40, 35, 40, 35)

        # 成功图标
        icon_label = QLabel("✅")
        icon_label.setStyleSheet("font-size: 64px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("计算完成！")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e8e8e8; max-height: 1px; margin: 5px 0;")
        content_layout.addWidget(line)

        # 统计信息
        combo_count = len(self.nutrition_result) if self.nutrition_result else 0
        info_label = QLabel(f"已成功计算 {combo_count} 种组合的营养成分")
        info_label.setStyleSheet("""
            font-size: 14px;
            color: #555555;
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(info_label)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("查看结果")
        ok_btn.setFixedSize(160, 44)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        ok_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(ok_btn)

        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        dialog.exec()

    def parse_recipe_excel(self, df):
        """
        智能解析食谱Excel文件，支持多种格式
        支持：
        1. 简单格式：增肌：xxx / 减脂：xxx
        2. 复杂格式：增肌/高：xxx / 增肌/矮：xxx / 减脂/高：xxx / 减脂/矮：xxx
        """
        try:
            recipe_data = {}
            days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
            meals = ["早餐", "午餐", "晚餐"]

            # 1. 找到包含"餐次"的行
            meal_row_idx = None
            for row_idx in range(min(30, len(df))):
                for col_idx in range(min(10, len(df.columns))):
                    cell_value = str(df.iloc[row_idx, col_idx]) if pd.notna(df.iloc[row_idx, col_idx]) else ""
                    if "餐次" in cell_value:
                        meal_row_idx = row_idx
                        break
                if meal_row_idx is not None:
                    break

            if meal_row_idx is None:
                return None

            # 2. 找到星期对应的列（考虑合并单元格）
            day_cols = self._find_day_columns(df, meal_row_idx, days)

            # 3. 找到早餐、午餐、晚餐的行
            meal_rows = self._find_meal_rows(df, meal_row_idx, meals)

            # 4. 提取数据
            for day, col_idx in day_cols.items():
                recipe_data[day] = {}

                for meal, row_idx in meal_rows.items():
                    # 获取该餐次的数据
                    cell_value = self._get_cell_value(df, row_idx, col_idx)

                    if cell_value:
                        recipe_data[day][meal] = cell_value
                    else:
                        recipe_data[day][meal] = ""

            # 5. 合并同一餐次的多行内容
            recipe_data = self._merge_multi_row_content(df, recipe_data, meal_rows, day_cols, days, meals)

            # 6. 解析每个单元格中的组合数据
            parsed_data = self._parse_combinations_from_cells(recipe_data, days, meals)

            for combo_name in parsed_data.get("组合列表", []):
                for day in days:
                    if day in parsed_data.get(combo_name, {}):
                        for meal in meals:
                            text = parsed_data[combo_name][day].get(meal, "")[:50]
                            if text:
                                pass

            return parsed_data

        except Exception as e:
            traceback.print_exc()
            return None

    def _find_day_columns(self, df, meal_row_idx, days):
        """找到星期对应的列（处理合并单元格）"""
        day_cols = {}

        # 先找出所有非空的星期列
        for col_idx in range(3, min(50, len(df.columns))):
            cell_value = str(df.iloc[meal_row_idx, col_idx]) if pd.notna(df.iloc[meal_row_idx, col_idx]) else ""
            if cell_value and cell_value != "nan":
                for day in days:
                    if day in cell_value:
                        day_cols[day] = col_idx
                        break

        # 如果找不到，尝试在更宽的范围内查找
        if len(day_cols) < 7:
            for col_idx in range(3, min(80, len(df.columns))):
                cell_value = str(df.iloc[meal_row_idx, col_idx]) if pd.notna(df.iloc[meal_row_idx, col_idx]) else ""
                if cell_value and cell_value != "nan":
                    for day in days:
                        if day in cell_value and day not in day_cols:
                            day_cols[day] = col_idx
                            break

        # 处理合并单元格：如果某些星期没找到，根据列顺序推断
        if len(day_cols) < 7:
            # 获取已找到的星期列，按列索引排序
            found_days = sorted(day_cols.items(), key=lambda x: x[1])

            if found_days:
                # 计算平均列间距
                first_col = found_days[0][1]
                last_col = found_days[-1][1]
                avg_spacing = (last_col - first_col) / (len(found_days) - 1) if len(found_days) > 1 else 1

                # 按顺序推断缺失的星期
                for i, day in enumerate(days):
                    if day not in day_cols:
                        # 根据位置推断列索引
                        expected_col = first_col + int(i * avg_spacing)
                        # 检查该列是否为空（合并单元格）
                        for c in range(expected_col - 2, expected_col + 3):
                            if c < len(df.columns):
                                val = df.iloc[meal_row_idx, c]
                                if pd.isna(val) or str(val).strip() == "" or str(val) == "nan":
                                    day_cols[day] = c
                                    break

        return day_cols

    def _find_meal_rows(self, df, meal_row_idx, meals):
        """找到早餐、午餐、晚餐的行"""
        meal_rows = {}
        for row_idx in range(meal_row_idx + 1, min(meal_row_idx + 30, len(df))):
            first_col_val = str(df.iloc[row_idx, 0]) if pd.notna(df.iloc[row_idx, 0]) else ""

            for meal in meals:
                if meal in first_col_val and meal not in meal_rows:
                    meal_rows[meal] = row_idx
                    break

        return meal_rows

    def _get_cell_value(self, df, row_idx, col_idx):
        """获取单元格值，处理合并单元格"""
        if col_idx >= len(df.columns):
            return None

        val = df.iloc[row_idx, col_idx]
        if pd.notna(val) and str(val).strip() and str(val) != "nan":
            return str(val).strip()

        # 如果当前列为空，向右查找非空的合并单元格
        for c in range(col_idx, min(col_idx + 20, len(df.columns))):
            check_val = df.iloc[row_idx, c] if c < len(df.columns) else None
            if pd.notna(check_val) and str(check_val).strip() and str(check_val) != "nan":
                return str(check_val).strip()

        return None

    def _merge_multi_row_content(self, df, recipe_data, meal_rows, day_cols, days, meals):
        """合并同一餐次的多行内容"""

        for day in days:
            if day not in recipe_data:
                continue
            if day not in day_cols:
                continue

            col_idx = day_cols[day]

            for meal in meals:
                if meal not in recipe_data[day]:
                    continue

                current_text = recipe_data[day][meal]
                if not current_text:
                    continue

                # 检查下方是否有属于同一餐次的内容
                meal_row = meal_rows.get(meal)
                if meal_row is not None:
                    # 获取该餐次的数据范围
                    next_meal_row = None
                    for m in meals:
                        if m != meal and m in meal_rows:
                            next_meal_row = meal_rows[m]
                            break

                    if next_meal_row is None:
                        next_meal_row = meal_row + 15  # 默认向下15行

                    # 合并该餐次范围内的所有非空内容
                    combined_text = current_text
                    for r in range(meal_row + 1, next_meal_row):
                        if r >= len(df):
                            break
                        row_text = self._get_cell_value(df, r, col_idx)

                        if row_text and row_text not in combined_text:
                            combined_text += "\n" + row_text

                    recipe_data[day][meal] = combined_text

        return recipe_data

    def _parse_combinations_from_cells(self, recipe_data, days, meals):
        """
        从单元格文本中解析组合数据
        支持格式：
        - "增肌：xxx" 或 "增肌: xxx"
        - "减脂：xxx"
        - "增肌/高：xxx"（组合名包含"/"）
        - 多行格式（用<br>或换行分隔）
        """
        result = {
            "组合列表": []  # 存储所有组合名称
        }

        # 收集所有出现的组合名
        all_combo_names = set()

        # 第一遍：收集所有组合名
        for day in days:
            if day not in recipe_data:
                continue
            for meal in meals:
                if meal not in recipe_data[day]:
                    continue

                text = recipe_data[day][meal]
                if not text:
                    continue

                # 按<br>或换行分割
                lines = re.split(r'<br>|\n', text)

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    # 匹配格式：组合名：内容 或 组合名: 内容
                    match = re.match(r'^([^：:]+)[：:](.+)$', line)
                    if match:
                        combo_name = match.group(1).strip()
                        all_combo_names.add(combo_name)

        # 如果没有找到标准格式，尝试从行首提取组合名
        if not all_combo_names:
            for day in days:
                if day not in recipe_data:
                    continue
                for meal in meals:
                    if meal not in recipe_data[day]:
                        continue

                    text = recipe_data[day][meal]
                    if not text:
                        continue

                    lines = re.split(r'<br>|\n', text)

                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue

                        # 尝试匹配常见的组合名前缀
                        for prefix in ['增肌', '减脂', '瘦弱', '肥胖', '标准', '高', '矮']:
                            if line.startswith(prefix):
                                # 提取组合名（可能包含/，如"增肌/高"）
                                combo_end = line.find('：')
                                if combo_end == -1:
                                    combo_end = line.find(':')
                                if combo_end != -1:
                                    combo_name = line[:combo_end].strip()
                                    all_combo_names.add(combo_name)
                                break

        result["组合列表"] = sorted(list(all_combo_names))

        # 初始化每个组合的数据结构（确保所有天和餐次都有默认值）
        for combo_name in result["组合列表"]:
            result[combo_name] = {}
            for day in days:
                result[combo_name][day] = {}
                for meal in meals:
                    result[combo_name][day][meal] = ""

        # 第二遍：填充数据
        for day in days:
            if day not in recipe_data:
                continue
            for meal in meals:
                if meal not in recipe_data[day]:
                    continue

                text = recipe_data[day][meal]
                if not text:
                    continue

                # 按<br>或换行分割
                lines = re.split(r'<br>|\n', text)

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    # 尝试匹配每个组合
                    for combo_name in result["组合列表"]:
                        # 检查行是否以该组合名开头
                        if line.startswith(combo_name + '：') or line.startswith(combo_name + ':'):
                            # 提取内容
                            content = re.sub(r'^[^：:]+[：:]', '', line).strip()
                            result[combo_name][day][meal] = content
                            break
                    else:
                        # 如果没有匹配到任何组合，尝试模糊匹配
                        for combo_name in result["组合列表"]:
                            if combo_name in line:
                                content = re.sub(r'^[^：:]+[：:]', '', line).strip()
                                result[combo_name][day][meal] = content
                                break

        for combo_name in result["组合列表"]:
            for day in days:
                has_data = False
                for meal in meals:
                    if result[combo_name][day].get(meal, ""):
                        has_data = True
                        break
                if has_data:
                    pass
                else:
                    pass

        return result

    def calculate_nutrition(self, recipe_data):
        """计算营养成分（新版）"""
        result = {}

        try:
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()

            days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
            meals = ["早餐", "午餐", "晚餐"]

            combo_names = recipe_data.get("组合列表", [])

            for combo_name in combo_names:
                result[combo_name] = {}
                combo_data = recipe_data.get(combo_name, {})

                for day in days:
                    if day not in combo_data:
                        continue

                    result[combo_name][day] = {}

                    for meal in meals:
                        if meal not in combo_data[day]:
                            continue

                        dishes_text = combo_data[day][meal]

                        if not dishes_text:
                            continue

                        # 解析菜式列表
                        dishes = self.parse_dishes_from_text(dishes_text)

                        # 计算该餐的营养
                        nutrition = self.calculate_meal_nutrition(cursor, dishes)

                        result[combo_name][day][meal] = nutrition

            conn.close()
            return result

        except Exception as e:
            traceback.print_exc()
            return None

    def parse_combos_from_text(self, text):
        """从文本中解析不同组合的菜式"""
        combos = {}

        if not text:
            return combos

        # 按换行分割
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 格式1：组合名：菜式
            if '：' in line:
                parts = line.split('：', 1)
                combo_name = parts[0].strip()
                dishes = parts[1].strip()
                combos[combo_name] = dishes
            elif ':' in line:
                parts = line.split(':', 1)
                combo_name = parts[0].strip()
                dishes = parts[1].strip()
                combos[combo_name] = dishes
            else:
                # 如果没有冒号，可能是纯菜式文本，尝试识别组合名
                # 常见组合名：增肌、减脂、瘦弱、肥胖等
                for combo_prefix in ['增肌', '减脂', '瘦弱', '肥胖', '标准', '高', '矮']:
                    if line.startswith(combo_prefix):
                        combo_name = combo_prefix
                        dishes = line[len(combo_prefix):].strip()
                        # 去掉可能的前缀分隔符
                        if dishes.startswith('：') or dishes.startswith(':'):
                            dishes = dishes[1:].strip()
                        if dishes.startswith('+'):
                            dishes = dishes[1:].strip()
                        combos[combo_name] = dishes
                        break
                else:
                    # 没有识别到组合名，作为默认组合
                    if "默认" not in combos:
                        combos["默认"] = line
                    else:
                        combos["默认"] += " + " + line

        # 如果没有解析到任何组合，整个文本作为一个组合
        if not combos and text:
            combos["默认"] = text

        return combos

    def parse_dishes_from_text(self, dishes_str):
        """从菜式文本中解析出菜品列表（增强版）"""
        dishes = []

        if not dishes_str:
            return dishes

        # 先按加号分割
        if ' + ' in dishes_str:
            parts = dishes_str.split(' + ')
        elif '+' in dishes_str:
            parts = dishes_str.split('+')
        elif '、' in dishes_str:
            parts = dishes_str.split('、')
        else:
            parts = [dishes_str]

        for part in parts:
            part = part.strip()
            if part:
                dishes.append(part)

        return dishes

    def calculate_meal_nutrition(self, cursor, dishes, meal_type=None):
        """计算一餐的营养成分（增强版，支持带分量的菜品和数量单位）"""
        total_nutrition = {
            "热量": 0,
            "蛋白质": 0,
            "碳水": 0,
            "脂肪": 0,
            "膳食纤维": 0,
            "糖类": 0,
            "菜品明细": []
        }

        # 判断餐次类型
        is_breakfast = False
        breakfast_keywords = ['水煮蛋', '牛奶', '酸奶', '豆浆', '全麦面包', '玉米', '红薯', '芋头', '馒头', '花卷',
                              '肉包', '叉烧包']
        for dish_str in dishes:
            for kw in breakfast_keywords:
                if kw in dish_str:
                    is_breakfast = True
                    break
            if is_breakfast:
                break

        for dish_str in dishes:
            dish_name, quantity, weight_grams, quantity_unit = self.parse_dish_and_quantity(dish_str)

            if not dish_name:
                continue

            # 查询菜式的食材配量
            cursor.execute("SELECT ingredients FROM recipes WHERE name = ?", (dish_name,))
            row = cursor.fetchone()

            if not row:
                clean_name = re.sub(r'\([^)]*\)', '', dish_name).strip()
                if clean_name != dish_name:
                    cursor.execute("SELECT ingredients FROM recipes WHERE name = ?", (clean_name,))
                    row = cursor.fetchone()

            if not row:
                cursor.execute("SELECT ingredients, name FROM recipes WHERE name LIKE ?", (f'%{dish_name}%',))
                row = cursor.fetchone()

            if not row:
                continue

            ingredients_text = row[0] if row[0] else ""

            ingredients = self.parse_ingredients(ingredients_text)

            # 数量因子
            if is_breakfast:
                quantity_factor = quantity
                dish_factor = 1
            else:
                quantity_factor = 1
                dish_factor = 1

            if '蛋' in dish_name and quantity > 1:
                quantity_factor = quantity

            dish_nutrition = {
                "菜名": dish_str,
                "热量": 0,
                "蛋白质": 0,
                "碳水": 0,
                "脂肪": 0,
                "膳食纤维": 0,
                "糖类": 0,
                "食材明细": [],
                "数量": quantity,
                "数量单位": quantity_unit,
                "重量标注": weight_grams,
                "是早餐": is_breakfast
            }

            for ing_name, amount in ingredients.items():
                ing_amount = amount * quantity_factor * dish_factor

                # 清理食材名称（去除空格和特殊字符）
                clean_ing_name = ing_name.strip()

                # 先精确匹配
                cursor.execute("""
                    SELECT protein, carbs, fat, fiber, sugar, calories 
                    FROM ingredients WHERE name = ?
                """, (clean_ing_name,))
                ing_row = cursor.fetchone()

                # 如果精确匹配失败，尝试模糊匹配
                if not ing_row:
                    cursor.execute("""
                        SELECT protein, carbs, fat, fiber, sugar, calories 
                        FROM ingredients WHERE name LIKE ?
                    """, (f'%{clean_ing_name}%',))
                    ing_row = cursor.fetchone()
                    if ing_row:
                        pass

                if not ing_row:
                    continue


                ing_factor = ing_amount / 100
                protein = (ing_row[0] or 0) * ing_factor
                carbs = (ing_row[1] or 0) * ing_factor
                fat = (ing_row[2] or 0) * ing_factor
                fiber = (ing_row[3] or 0) * ing_factor
                sugar = (ing_row[4] or 0) * ing_factor
                calories = (ing_row[5] or 0) * ing_factor

                dish_nutrition["蛋白质"] += protein
                dish_nutrition["碳水"] += carbs
                dish_nutrition["脂肪"] += fat
                dish_nutrition["膳食纤维"] += fiber
                dish_nutrition["糖类"] += sugar
                dish_nutrition["热量"] += calories

                dish_nutrition["食材明细"].append({
                    "食材": ing_name,
                    "用量": f"{round(ing_amount, 1)}g",
                    "热量": round(calories, 1),
                    "蛋白质": round(protein, 1),
                    "碳水": round(carbs, 1),
                    "脂肪": round(fat, 1),
                    "膳食纤维": round(fiber, 1),
                    "糖类": round(sugar, 1),
                    "原始配方用量": amount,
                    "数量因子": quantity_factor,
                    "数量单位": quantity_unit,
                    "重量标注": weight_grams
                })

                total_nutrition["蛋白质"] += protein
                total_nutrition["碳水"] += carbs
                total_nutrition["脂肪"] += fat
                total_nutrition["膳食纤维"] += fiber
                total_nutrition["糖类"] += sugar
                total_nutrition["热量"] += calories

            for key in ["蛋白质", "碳水", "脂肪", "膳食纤维", "糖类", "热量"]:
                dish_nutrition[key] = round(dish_nutrition[key], 1)


            if dish_nutrition["热量"] > 0:
                total_nutrition["菜品明细"].append(dish_nutrition)

        for key in ["蛋白质", "碳水", "脂肪", "膳食纤维", "糖类", "热量"]:
            total_nutrition[key] = round(total_nutrition[key], 1)

        return total_nutrition

    def parse_dish_and_quantity(self, dish_str):
        """
        解析菜名和分量（增强版）
        支持格式：
        - "蒜蓉蒸鸡胸肉(150g)" -> 菜名:蒜蓉蒸鸡胸肉, 重量标注:150g（仅用于显示，不用于缩放）
        - "水煮蛋2个" -> 菜名:水煮蛋, 数量:2个
        - "全麦面包2片" -> 菜名:全麦面包, 数量:2片
        - "牛奶1杯" -> 菜名:牛奶, 数量:1杯
        """
        dish_name = dish_str
        quantity = 1
        weight_mark = 0  # 重量标注，仅用于显示，不用于计算缩放
        quantity_unit = ""

        # 匹配数量格式（如 2个, 2片, 2碗, 2杯, 2根, 2份）
        quantity_match = re.search(r'(\d+)\s*(个|片|碗|杯|根|份|条|块|粒|勺|包|盒|袋)', dish_str)
        if quantity_match:
            quantity = int(quantity_match.group(1))
            quantity_unit = quantity_match.group(2)
            dish_name = re.sub(r'\s*\d+\s*(个|片|碗|杯|根|份|条|块|粒|勺|包|盒|袋)', '', dish_str).strip()

        # 匹配重量标注 (150g) - 仅用于显示，表示肉类的重量
        weight_match = re.search(r'\((\d+)g\)', dish_name)
        if weight_match:
            weight_mark = int(weight_match.group(1))
            dish_name = re.sub(r'\s*\(\d+g\)', '', dish_name).strip()

        # 匹配只有数字没有单位的情况（如 "150g" 但没有括号）
        if weight_mark == 0:
            simple_match = re.search(r'(\d+)g', dish_name)
            if simple_match:
                weight_mark = int(simple_match.group(1))
                dish_name = re.sub(r'\s*\d+g', '', dish_name).strip()

        return dish_name, quantity, weight_mark, quantity_unit

    def parse_ingredients(self, ingredients_text):
        """解析食材和用量（增强版）"""
        ingredients = {}

        # 匹配模式：食材名称 + 数字 + g
        pattern = r'([^+\d]+?)\s*(\d+)g'
        matches = re.findall(pattern, ingredients_text)

        for ing_name, amount in matches:
            ing_name = ing_name.strip()
            ing_name = re.sub(r'[（(][^）)]*[）)]', '', ing_name).strip()
            ing_name = re.sub(r'\s+', ' ', ing_name)
            ing_name = ing_name.strip()
            if ing_name:
                ingredients[ing_name] = int(amount)

        # 也支持 ml 单位
        pattern_ml = r'([^+\d]+?)\s*(\d+)ml'
        matches_ml = re.findall(pattern_ml, ingredients_text)
        for ing_name, amount in matches_ml:
            ing_name = ing_name.strip()
            ing_name = re.sub(r'[（(][^）)]*[）)]', '', ing_name).strip()
            ing_name = re.sub(r'\s+', ' ', ing_name)
            ing_name = ing_name.strip()
            if ing_name:
                ingredients[ing_name] = int(amount)

        if not ingredients:
            pass

        return ingredients

    def display_nutrition_result(self):
        """显示营养计算结果（新版，支持多组合标签页）"""
        self.clear_content()

        if not self.nutrition_result:
            return

        # 标题
        title = QLabel("📊 营养计算结果")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        self.content_layout.addWidget(title)

        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        meals = ["早餐", "午餐", "晚餐"]

        # 创建标签页
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                color: #333;
                font-size: 13px;
                font-weight: bold;
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e0e0e0;
            }
        """)

        # 获取所有组合名称
        combo_names = list(self.nutrition_result.keys())

        if not combo_names:
            combo_names = ["默认"]

        # 为每个组合创建标签页
        for combo_name in combo_names:
            combo_widget = self.create_combo_widget(combo_name, days, meals)
            tab_widget.addTab(combo_widget, combo_name)

        self.content_layout.addWidget(tab_widget)

    def create_combo_widget(self, combo_name, days, meals):
        """创建组合的营养显示组件（新版）"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        combo_data = self.nutrition_result.get(combo_name, {})

        # 汇总统计
        total_stats = {
            "热量": 0, "蛋白质": 0, "碳水": 0, "脂肪": 0, "膳食纤维": 0, "糖类": 0
        }

        for day in days:
            if day not in combo_data:
                continue

            # 日期标题
            day_label = QLabel(day)
            day_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #1565C0;
                background-color: #e3f2fd;
                padding: 8px 15px;
                border-radius: 8px;
                margin-top: 5px;
            """)
            layout.addWidget(day_label)

            # 创建三餐的网格布局
            grid = QGridLayout()
            grid.setSpacing(10)
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            grid.setColumnStretch(2, 1)

            for i, meal in enumerate(meals):
                if meal not in combo_data[day]:
                    continue

                nutrition = combo_data[day][meal]

                # 累加到总计
                for key in total_stats:
                    total_stats[key] += nutrition.get(key, 0)

                # 餐次标题
                meal_title = QLabel(f"🍽️ {meal}")
                meal_title.setStyleSheet("""
                    font-size: 14px;
                    font-weight: bold;
                    color: #333;
                    padding: 5px 0;
                """)
                grid.addWidget(meal_title, 0, i, Qt.AlignmentFlag.AlignCenter)

                # 营养数据
                nutrition_text = f"""
                <div style='background-color: #f8f9fa; padding: 12px; border-radius: 10px;'>
                <b>热量</b>: {nutrition.get('热量', 0)}千卡<br>
                <b>蛋白质</b>: {nutrition.get('蛋白质', 0)}g<br>
                <b>碳水</b>: {nutrition.get('碳水', 0)}g<br>
                <b>脂肪</b>: {nutrition.get('脂肪', 0)}g<br>
                <b>膳食纤维</b>: {nutrition.get('膳食纤维', 0)}g<br>
                <b>糖类</b>: {nutrition.get('糖类', 0)}g
                </div>
                """

                nutrition_label = QLabel(nutrition_text)
                nutrition_label.setStyleSheet("font-size: 12px; color: #555;")
                nutrition_label.setWordWrap(True)
                grid.addWidget(nutrition_label, 1, i, Qt.AlignmentFlag.AlignTop)

                # 查看详情按钮
                detail_btn = QPushButton("查看详情")
                detail_btn.setFixedSize(90, 30)
                detail_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        font-size: 11px;
                        font-weight: bold;
                        border: none;
                        border-radius: 15px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
                detail_btn.clicked.connect(
                    lambda checked, d=day, m=meal, n=nutrition:
                    self.show_meal_detail(d, m, n)
                )
                grid.addWidget(detail_btn, 2, i, Qt.AlignmentFlag.AlignCenter)

            layout.addLayout(grid)

            # 分隔线
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("background-color: #e0e0e0; max-height: 1px;")
            layout.addWidget(line)

        # 一周总计
        total_label = QLabel(f"""
        <div style='background-color: #e8f5e9; padding: 15px; border-radius: 12px; margin-top: 10px;'>
        <b style='font-size: 16px;'>📊 一周总计</b><br>
        <span style='font-size: 14px;'>
        热量: {round(total_stats['热量'], 1)}千卡 | 
        蛋白质: {round(total_stats['蛋白质'], 1)}g | 
        碳水: {round(total_stats['碳水'], 1)}g<br>
        脂肪: {round(total_stats['脂肪'], 1)}g | 
        膳食纤维: {round(total_stats['膳食纤维'], 1)}g | 
        糖类: {round(total_stats['糖类'], 1)}g
        </span>
        </div>
        """)
        total_label.setStyleSheet("font-size: 13px; color: #333;")
        total_label.setWordWrap(True)
        layout.addWidget(total_label)

        layout.addStretch()
        return widget

    def show_meal_detail(self, day, meal, nutrition):
        """显示餐次详情对话框，包含计算过程"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(900, 750)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QPushButton {
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
            QScrollArea {
                background-color: #fafafa;
                border: none;
            }
            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #2196F3; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(30, 25, 30, 25)

        # 标题
        title = QLabel(f"{day} {meal} 营养详情")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #1565C0;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)

        # 总计
        total_text = f"""
        <div style='background-color: #e3f2fd; padding: 15px; border-radius: 12px;'>
        <b style='font-size: 14px;'>📊 总计</b><br>
        <table style='width: 100%; margin-top: 8px;'>
            <tr>
                <td><b>热量</b></td>
                <td>{nutrition.get('热量', 0)} 千卡</td>
                <td><b>蛋白质</b></td>
                <td>{nutrition.get('蛋白质', 0)} g</td>
            </tr>
            <tr>
                <td><b>碳水</b></td>
                <td>{nutrition.get('碳水', 0)} g</td>
                <td><b>脂肪</b></td>
                <td>{nutrition.get('脂肪', 0)} g</td>
            </tr>
            <tr>
                <td><b>膳食纤维</b></td>
                <td>{nutrition.get('膳食纤维', 0)} g</td>
                <td><b>糖类</b></td>
                <td>{nutrition.get('糖类', 0)} g</td>
            </tr>
        </table>
        </div>
        """
        total_label = QLabel(total_text)
        total_label.setStyleSheet("font-size: 13px; color: #333;")
        total_label.setWordWrap(True)
        content_layout.addWidget(total_label)

        # 菜品明细（带计算过程）
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #fafafa;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #e0e0e0;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                border-radius: 4px;
            }
        """)

        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setSpacing(15)

        for idx, dish in enumerate(nutrition.get("菜品明细", [])):
            # 创建菜品卡片
            dish_card = QWidget()
            dish_card.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                }
            """)
            dish_layout = QVBoxLayout(dish_card)
            dish_layout.setSpacing(10)
            dish_layout.setContentsMargins(15, 12, 15, 12)

            # 菜品名称（带数量信息）
            dish_name_text = dish.get('菜名', '未知菜品')
            quantity = dish.get('数量', 1)
            quantity_unit = dish.get('数量单位', '')
            if quantity > 1 and quantity_unit:
                dish_name_text = f"{dish_name_text}"

            dish_name = QLabel(f"🍲 {dish_name_text}")
            dish_name.setStyleSheet("font-size: 15px; font-weight: bold; color: #2e7d32;")
            dish_layout.addWidget(dish_name)

            # 菜品总计营养
            dish_total = QLabel(
                f"热量: {dish.get('热量', 0)}千卡 | 蛋白质: {dish.get('蛋白质', 0)}g | "
                f"碳水: {dish.get('碳水', 0)}g | 脂肪: {dish.get('脂肪', 0)}g |"
                f"糖类: {dish.get('糖类', 0)}g | 膳食纤维: {dish.get('膳食纤维', 0)}g"
            )
            dish_total.setStyleSheet("font-size: 12px; color: #555; padding: 5px 0;")
            dish_layout.addWidget(dish_total)

            # 分隔线
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("background-color: #e8e8e8; max-height: 1px;")
            dish_layout.addWidget(line)

            # 食材明细（带计算过程）
            ingredients_label = QLabel("📋 食材明细及计算过程：")
            ingredients_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #666; margin-top: 5px;")
            dish_layout.addWidget(ingredients_label)

            # 获取食材明细
            ingredients = dish.get("食材明细", [])

            if ingredients and len(ingredients) > 0:
                for ing in ingredients:
                    # 创建食材项容器
                    ing_container = QWidget()
                    ing_container.setStyleSheet("""
                        QWidget {
                            background-color: #f8f9fa;
                            border-radius: 8px;
                            margin: 2px;
                        }
                    """)
                    ing_layout = QVBoxLayout(ing_container)
                    ing_layout.setSpacing(5)
                    ing_layout.setContentsMargins(12, 8, 12, 8)

                    # 食材名称和用量
                    ing_name = ing.get('食材', '未知食材')
                    ing_amount = ing.get('用量', '0g')

                    # 获取数量和因子信息用于显示
                    quantity_factor = ing.get('数量因子', 1)
                    dish_factor = ing.get('菜品重量因子', 1)

                    # 构建食材头部信息
                    if quantity_factor > 1:
                        ing_header = QLabel(f"• {ing_name} ({ing_amount})")
                    elif dish_factor != 1 and dish_factor > 0:
                        ing_header = QLabel(f"• {ing_name} ({ing_amount}) [菜品缩放因子: {dish_factor:.2f}]")
                    else:
                        ing_header = QLabel(f"• {ing_name} ({ing_amount})")
                    ing_header.setStyleSheet("font-size: 13px; font-weight: bold; color: #333;")
                    ing_layout.addWidget(ing_header)

                    # 计算过程
                    calc_text = self.get_ingredient_calculation_process_text(ing_name, ing_amount, ing)
                    calc_label = QLabel(calc_text)
                    calc_label.setStyleSheet("font-size: 11px; color: #666; margin-left: 10px;")
                    calc_label.setWordWrap(True)
                    ing_layout.addWidget(calc_label)

                    dish_layout.addWidget(ing_container)
            else:
                # 没有食材明细时，显示提示
                no_detail_label = QLabel("  暂无详细食材数据")
                no_detail_label.setStyleSheet("font-size: 11px; color: #999; margin-left: 10px;")
                dish_layout.addWidget(no_detail_label)

            detail_layout.addWidget(dish_card)

        if not nutrition.get("菜品明细"):
            empty_label = QLabel("暂无菜品明细数据")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("font-size: 14px; color: #999; padding: 40px;")
            detail_layout.addWidget(empty_label)

        detail_layout.addStretch()
        scroll_area.setWidget(detail_widget)
        content_layout.addWidget(scroll_area, 1)

        # 底部按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        # 关闭按钮
        close_btn = QPushButton("关 闭")
        close_btn.setFixedSize(140, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        close_btn.clicked.connect(dialog.accept)

        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        dialog.exec()

    def get_ingredient_calculation_process(self, ingredient_name, usage_str, ing_data):
        """获取食材的计算过程说明"""
        try:
            # 解析用量（格式如 "150g"）
            import re
            match = re.search(r'(\d+(?:\.\d+)?)', usage_str)
            if not match:
                return f"计算过程：{ing_data['热量']}千卡"

            amount = float(match.group(1))

            # 从数据库获取每100g的营养数据
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT protein, carbs, fat, fiber, sugar, calories 
                FROM ingredients WHERE name = ? OR name LIKE ?
            """, (ingredient_name, f'%{ingredient_name}%'))
            row = cursor.fetchone()
            conn.close()

            if row:
                protein_per_100 = row[0] or 0
                carbs_per_100 = row[1] or 0
                fat_per_100 = row[2] or 0
                fiber_per_100 = row[3] or 0
                sugar_per_100 = row[4] or 0
                calories_per_100 = row[5] or 0

                # 计算因子
                factor = amount / 100

                # 构建计算过程
                calc_lines = [
                    f"📐 计算过程：",
                    f"   用量 = {amount}g",
                    f"   每100g营养：",
                    f"     热量 = {calories_per_100}千卡，蛋白质 = {protein_per_100}g，碳水 = {carbs_per_100}g，脂肪 = {fat_per_100}g，糖类 = {sugar_per_100}g，膳食纤维 = {fiber_per_100}g",
                    f"   计算结果：",
                    f"     热量 = {calories_per_100} × {amount} ÷ 100 = {ing_data['热量']} 千卡",
                    f"     蛋白质 = {protein_per_100} × {amount} ÷ 100 = {ing_data['蛋白质']} g",
                    f"     碳水 = {carbs_per_100} × {amount} ÷ 100 = {ing_data['碳水']} g",
                    f"     脂肪 = {fat_per_100} × {amount} ÷ 100 = {ing_data['脂肪']} g",
                    f"     糖类 = {fat_per_100} × {amount} ÷ 100 = {ing_data['糖类']} g"
                    f"     膳食纤维 = {fat_per_100} × {amount} ÷ 100 = {ing_data['膳食纤维']} g"
                ]

                # 可选营养
                extra = []
                if fiber_per_100 > 0:
                    extra.append(f"膳食纤维 = {fiber_per_100} × {amount} ÷ 100 = {ing_data.get('膳食纤维', 0)} g")
                if sugar_per_100 > 0:
                    extra.append(f"糖类 = {sugar_per_100} × {amount} ÷ 100 = {ing_data.get('糖类', 0)} g")

                if extra:
                    calc_lines.append(f"     {', '.join(extra)}")

                return "<br>".join(calc_lines)
            else:
                return f"📐 计算过程：{ing_data['热量']}千卡 (基于菜品配比)"

        except Exception as e:
            return f"📐 计算过程：{ing_data['热量']}千卡"

    def get_ingredient_calculation_process_text(self, ingredient_name, usage_str, ing_data):
        """获取食材的计算过程说明"""
        try:
            import re
            # 解析用量（格式如 "150g"）
            match = re.search(r'(\d+(?:\.\d+)?)', usage_str)
            if not match:
                return f"📐 计算过程：{ing_data.get('热量', 0)}千卡"

            amount = float(match.group(1))

            # 获取因子信息
            quantity_factor = ing_data.get('数量因子', 1)
            dish_factor = ing_data.get('菜品重量因子', 1)
            quantity_unit = ing_data.get('数量单位', '')

            # 从数据库获取每100g的营养数据
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()

            # 尝试精确匹配
            cursor.execute("""
                SELECT protein, carbs, fat, fiber, sugar, calories 
                FROM ingredients WHERE name = ?
            """, (ingredient_name,))
            row = cursor.fetchone()

            # 如果精确匹配失败，尝试模糊匹配
            if not row:
                cursor.execute("""
                    SELECT protein, carbs, fat, fiber, sugar, calories 
                    FROM ingredients WHERE name LIKE ?
                """, (f'%{ingredient_name}%',))
                row = cursor.fetchone()

            conn.close()

            if row:
                protein_per_100 = row[0] or 0
                carbs_per_100 = row[1] or 0
                fat_per_100 = row[2] or 0
                fiber_per_100 = row[3] or 0
                sugar_per_100 = row[4] or 0
                calories_per_100 = row[5] or 0

                # 计算各项营养
                calc_calories = calories_per_100 * amount / 100
                calc_protein = protein_per_100 * amount / 100
                calc_carbs = carbs_per_100 * amount / 100
                calc_fat = fat_per_100 * amount / 100
                calc_suger = sugar_per_100 * amount / 100
                calc_fiber = fiber_per_100 * amount / 100

                # 构建计算过程（使用HTML格式）
                calc_lines = [
                    f"<span style='color:#888;'>📐 计算过程：</span>",
                    f"<span style='margin-left:15px;'>用量 = {amount}g</span>",
                ]

                # 如果有数量因子，显示计算说明
                if quantity_factor > 1:
                    if quantity_unit:
                        calc_lines.append(
                            f"<span style='margin-left:15px;color:#FF9800;'>数量说明：{quantity_factor}{quantity_unit}（1{quantity_unit} = {ing_data.get('原始配方用量', amount / quantity_factor):.1f}g）</span>")
                        calc_lines.append(
                            f"<span style='margin-left:15px;'>总用量 = {ing_data.get('原始配方用量', amount / quantity_factor):.1f}g × {quantity_factor} = {amount}g</span>")
                    else:
                        calc_lines.append(
                            f"<span style='margin-left:15px;color:#FF9800;'>数量说明：{quantity_factor}份</span>")

                if dish_factor != 1 and dish_factor > 0:
                    calc_lines.append(
                        f"<span style='margin-left:15px;color:#FF9800;'>菜品重量因子 = {dish_factor:.2f}</span>")

                calc_lines.extend([
                    f"<span style='margin-left:15px;'>每100g营养：热量={calories_per_100}千卡，蛋白质={protein_per_100}g，碳水={carbs_per_100}g，脂肪={fat_per_100}g，糖类={sugar_per_100}g"
                    f"，膳食纤维={fiber_per_100}g</span>",
                    f"<span style='margin-left:15px;color:#4CAF50;'>计算结果：</span>",
                    f"<span style='margin-left:25px;'>热量 = {calories_per_100} × {amount} ÷ 100 = {calc_calories:.1f} 千卡</span>",
                    f"<span style='margin-left:25px;'>蛋白质 = {protein_per_100} × {amount} ÷ 100 = {calc_protein:.1f} g</span>",
                    f"<span style='margin-left:25px;'>碳水 = {carbs_per_100} × {amount} ÷ 100 = {calc_carbs:.1f} g</span>",
                    f"<span style='margin-left:25px;'>脂肪 = {fat_per_100} × {amount} ÷ 100 = {calc_fat:.1f} g</span>",
                    f"<span style='margin-left:25px;'>糖类 = {sugar_per_100} × {amount} ÷ 100 = {calc_suger:.1f} g</span>",
                    f"<span style='margin-left:25px;'>膳食纤维 = {fiber_per_100} × {amount} ÷ 100 = {calc_fiber:.1f} g</span>"
                ])

                return "<br>".join(calc_lines)
            else:
                return f"📐 计算过程：{ing_data.get('热量', 0)}千卡 (基于菜品配比)"

        except Exception as e:
            return f"📐 计算过程：{ing_data.get('热量', 0)}千卡"

class ComboBoxDelegate(QStyledItemDelegate):
    """下拉框委托"""

    def __init__(self, parent=None, items=None):
        super().__init__(parent)
        self.items = items or []

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        for item in self.items:
            combo.addItem(item)
        combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #333;
                padding: 4px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #bbdefb;
            }
        """)
        return combo

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        if value:
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class DatabaseManagerWidget(QWidget):
    """数据库管理界面"""

    def __init__(self):
        super().__init__()
        self.current_table = None
        self.current_data = []
        self.current_headers = []
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        # 设置背景颜色
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #e8f4fc, stop:1 #d1e8f5);
                border-radius: 10px;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 标题
        title = QLabel("🗄️ 数据库管理")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        main_layout.addWidget(title)

        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #bdc3c7; max-height: 2px;")
        main_layout.addWidget(line)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addStretch()

        # 菜式表按钮
        self.recipes_btn = QPushButton("📖 菜式表")
        self.recipes_btn.setFixedSize(200, 50)
        self.recipes_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

        # 食材表按钮
        self.ingredients_btn = QPushButton("🥬 食材表")
        self.ingredients_btn.setFixedSize(200, 50)
        self.ingredients_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
        """)

        # 刷新图标按钮
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(50, 50)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 22px;
                font-weight: bold;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.refresh_btn.setToolTip("从食物数据库.xlsx重新导入数据")

        button_layout.addWidget(self.recipes_btn)
        button_layout.addWidget(self.ingredients_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # 表格显示区域
        self.table_scroll = QScrollArea()
        self.table_scroll.setWidgetResizable(True)
        self.table_scroll.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
            }
        """)

        # 表格容器
        self.table_container = QWidget()
        self.table_layout = QVBoxLayout(self.table_container)
        self.table_layout.setContentsMargins(10, 10, 10, 10)

        self.table_scroll.setWidget(self.table_container)
        main_layout.addWidget(self.table_scroll, stretch=1)

        # 底部信息栏
        self.info_label = QLabel("数据库详情")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("""
            font-size: 13px;
            color: #7f8c8d;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 8px;
        """)
        main_layout.addWidget(self.info_label)

    def setup_connections(self):
        """设置信号连接"""
        self.recipes_btn.clicked.connect(lambda: self.load_table_data('recipes'))
        self.ingredients_btn.clicked.connect(lambda: self.load_table_data('ingredients'))
        self.refresh_btn.clicked.connect(self.on_refresh_clicked)

    def on_refresh_clicked(self):
        """刷新按钮点击事件 - 从Excel重新导入数据"""
        # 创建确认对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(480, 380)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                color: #333;
            }
            QPushButton {
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
        """)

        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #2196F3; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(35, 30, 35, 35)

        # 图标
        icon_label = QLabel("🔄")
        icon_label.setStyleSheet("font-size: 52px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("从Excel导入数据")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2196F3;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e0e0e0; max-height: 1px;")
        content_layout.addWidget(line)

        # 文件路径显示
        current_dir = os.getcwd()
        excel_path = os.path.join(current_dir, "食物数据库.xlsx")

        path_label = QLabel(f"源文件：{excel_path}")
        path_label.setStyleSheet("""
            font-size: 13px;
            color: #555;
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 10px;
        """)
        path_label.setWordWrap(True)
        path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(path_label)

        # 警告信息
        warning_label = QLabel("⚠️ 导入将覆盖现有数据库中的所有数据！")
        warning_label.setStyleSheet("""
            font-size: 14px;
            color: #f44336;
            background: #ffebee;
            padding: 12px 20px;
            border-radius: 12px;
            font-weight: bold;
        """)
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warning_label.setWordWrap(True)
        content_layout.addWidget(warning_label)

        # 提示信息
        hint_label = QLabel("请确保「食物数据库.xlsx」文件存在于程序目录下")
        hint_label.setStyleSheet("""
            font-size: 12px;
            color: #7f8c8d;
            background: transparent;
        """)
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_label.setWordWrap(True)
        content_layout.addWidget(hint_label)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.addStretch()

        confirm_btn = QPushButton("确认导入")
        confirm_btn.setFixedSize(130, 44)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        confirm_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(confirm_btn)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(130, 44)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #666;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        if dialog.exec() == QDialog.Accepted:
            self.import_from_excel()

    def import_from_excel(self):
        """从Excel文件导入数据到数据库"""
        try:
            current_dir = os.getcwd()
            excel_path = os.path.join(current_dir, "食物数据库.xlsx")
            db_path = os.path.join(current_dir, "mydb.db")

            # 检查Excel文件是否存在
            if not os.path.exists(excel_path):
                QMessageBox.critical(self, "错误", f"找不到Excel文件：\n{excel_path}")
                return

            # 显示加载状态
            self.info_label.setText("⏳ 正在从Excel导入数据...")
            self.info_label.setStyleSheet("""
                font-size: 13px;
                color: #1565C0;
                padding: 8px;
                background-color: #e3f2fd;
                border-radius: 8px;
            """)
            QApplication.processEvents()

            # 连接数据库
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # 删除旧表
            cursor.execute("DROP TABLE IF EXISTS recipes")
            cursor.execute("DROP TABLE IF EXISTS ingredients")

            # 创建食材表
            cursor.execute("""
            CREATE TABLE ingredients (
                id INTEGER PRIMARY KEY,
                category TEXT,
                name TEXT,
                protein REAL,
                carbs REAL,
                fat REAL,
                fiber REAL,
                sugar REAL,
                calories REAL
            )
            """)

            # 读取食材表数据
            df_ingredients = pd.read_excel(excel_path, sheet_name="食材表")

            insert_ingredients = """
            INSERT INTO ingredients (id, category, name, protein, carbs, fat, fiber, sugar, calories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            ingredient_count = 0
            for _, row in df_ingredients.iterrows():
                if pd.isna(row.iloc[0]):
                    continue
                values = (
                    int(row.iloc[0]),
                    str(row.iloc[1]),
                    str(row.iloc[2]),
                    float(row.iloc[3]) if pd.notna(row.iloc[3]) else 0,
                    float(row.iloc[4]) if pd.notna(row.iloc[4]) else 0,
                    float(row.iloc[5]) if pd.notna(row.iloc[5]) else 0,
                    float(row.iloc[6]) if pd.notna(row.iloc[6]) else 0,
                    float(row.iloc[7]) if pd.notna(row.iloc[7]) else 0,
                    float(row.iloc[8]) if pd.notna(row.iloc[8]) else 0
                )
                cursor.execute(insert_ingredients, values)
                ingredient_count += 1

            # 创建食谱表
            cursor.execute("""
            CREATE TABLE recipes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                ingredients TEXT
            )
            """)

            # 读取食谱表数据
            df_recipes = pd.read_excel(excel_path, sheet_name="食谱表")

            insert_recipes = """
            INSERT INTO recipes (id, name, category, ingredients)
            VALUES (?, ?, ?, ?)
            """

            recipe_count = 0
            for _, row in df_recipes.iterrows():
                if pd.isna(row.iloc[0]):
                    continue

                recipe_id = int(row.iloc[0])
                name = str(row.iloc[1])
                category = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""
                ingredients = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""

                cursor.execute(insert_recipes, (recipe_id, name, category, ingredients))
                recipe_count += 1

            conn.commit()
            conn.close()

            # 显示成功信息
            self.info_label.setText(f"✅ 导入成功！食材 {ingredient_count} 条，食谱 {recipe_count} 条")
            self.info_label.setStyleSheet("""
                font-size: 13px;
                color: #2e7d32;
                padding: 8px;
                background-color: #e8f5e9;
                border-radius: 8px;
            """)

            # 清空当前显示的表格
            self.clear_table()
            self.current_table = None

            # 美化成功弹窗
            self.show_success_dialog(ingredient_count, recipe_count)

        except FileNotFoundError as e:
            self.info_label.setText("❌ 导入失败：找不到Excel文件")
            self.info_label.setStyleSheet("""
                font-size: 13px;
                color: #c62828;
                padding: 8px;
                background-color: #ffebee;
                border-radius: 8px;
            """)
            self.show_error_dialog(f"找不到Excel文件：\n{str(e)}")
        except Exception as e:
            self.info_label.setText(f"❌ 导入失败：{str(e)[:50]}")
            self.info_label.setStyleSheet("""
                font-size: 13px;
                color: #c62828;
                padding: 8px;
                background-color: #ffebee;
                border-radius: 8px;
            """)
            self.show_error_dialog(f"导入数据时发生错误：\n{str(e)}")
            traceback.print_exc()

    def show_success_dialog(self, ingredient_count, recipe_count):
        """显示美化成功弹窗"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(400, 320)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QPushButton {
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #4CAF50; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(40, 35, 40, 35)

        # 成功图标
        icon_label = QLabel("✅")
        icon_label.setStyleSheet("font-size: 64px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("导入成功！")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 提示信息
        hint_label = QLabel(f"已成功导入 {ingredient_count + recipe_count} 条数据")
        hint_label.setStyleSheet("""
            font-size: 15px;
            color: #555555;
        """)
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(hint_label)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("确 定")
        ok_btn.setFixedSize(160, 44)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        ok_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(ok_btn)

        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        dialog.exec()

    def show_error_dialog(self, message):
        """显示美化错误弹窗"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(400, 320)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QPushButton {
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(8)
        top_bar.setStyleSheet("background-color: #f44336; border-radius: 20px 20px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(40, 35, 40, 35)

        # 错误图标
        icon_label = QLabel("❌")
        icon_label.setStyleSheet("font-size: 64px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("导入失败")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #c62828;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 错误信息
        msg_label = QLabel(message)
        msg_label.setStyleSheet("""
            font-size: 14px;
            color: #555555;
        """)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        content_layout.addWidget(msg_label)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("确 定")
        ok_btn.setFixedSize(160, 44)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)
        ok_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(ok_btn)

        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        dialog.exec()

    def clear_table(self):
        """清空表格显示区域"""
        while self.table_layout.count():
            item = self.table_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_table_data(self, table_name):
        """加载表数据"""
        self.current_table = table_name
        self.clear_table()

        try:
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()

            if table_name == 'recipes':
                cursor.execute("SELECT id, name, category, ingredients FROM recipes ORDER BY id")
                rows = cursor.fetchall()
                self.current_headers = ["食谱名称", "类别", "食材及配量"]
                self.current_data = list(rows)

                # 类别直接使用数据库中的文本，不需要映射
                display_data = []
                for row in rows:
                    display_row = (row[1], row[2], row[3])  # name, category, ingredients
                    display_data.append(display_row)

            else:  # ingredients
                cursor.execute("""
                    SELECT id, category, name, protein, carbs, fat, fiber, sugar, calories
                    FROM ingredients
                    ORDER BY id
                """)
                rows = cursor.fetchall()
                self.current_headers = ["类别", "食材名称", "蛋白质(g/100g)", "碳水(g/100g)",
                                        "脂肪(g/100g)", "膳食纤维(g/100g)", "糖类(g/100g)", "热量(千卡/100g)"]
                self.current_data = list(rows)

                # 类别直接使用数据库中的文本
                display_data = []
                for row in rows:
                    display_row = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    display_data.append(display_row)

            conn.close()

            self.create_editable_table(self.current_headers, display_data)

            self.info_label.setText(
                f"{'📖 食谱表' if table_name == 'recipes' else '🥬 食材表'} - 共 {len(rows)} {'道菜式' if table_name == 'recipes' else '种食材'}"
            )
            self.info_label.setStyleSheet("""
                font-size: 13px;
                color: #2e7d32;
                padding: 8px;
                background-color: #e8f5e9;
                border-radius: 8px;
            """ if table_name == 'recipes' else """
                font-size: 13px;
                color: #e65100;
                padding: 8px;
                background-color: #fff3e0;
                border-radius: 8px;
            """)

        except sqlite3.Error as e:
            self.show_error_message(f"读取数据失败: {str(e)}")

    def create_editable_table(self, headers, data):
        """创建可编辑的表格组件"""
        if not data:
            empty_label = QLabel("📭 暂无数据")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("font-size: 16px; color: #999; padding: 40px;")
            self.table_layout.addWidget(empty_label)
            return

        rows = len(data)
        cols = len(headers) + 2  # 多两列：ID列和删除按钮列

        # 创建 QTableWidget
        table = QTableWidget(rows, cols)

        # 设置表头：ID + 数据headers + ""（删除列不设标题）
        display_headers = ["ID"] + list(headers) + [""]
        table.setHorizontalHeaderLabels(display_headers)

        # 设置样式
        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                font-size: 12px;
                alternate-background-color: #f8f9fa;
                selection-background-color: #bbdefb;
            }
            QTableWidget::item {
                padding: 8px 12px;
                color: #000000;
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #bbdefb;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                font-size: 13px;
                padding: 10px;
                border: none;
            }
        """)

        # 设置表格属性
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setWordWrap(True)
        table.setTextElideMode(Qt.ElideNone)

        # 存储原始数据ID的映射
        row_id_map = {}

        # 填充数据
        for row_idx, row_data in enumerate(data):
            original_id = self.current_data[row_idx][0]
            row_id_map[row_idx] = original_id

            # 第0列显示ID
            id_item = QTableWidgetItem(str(original_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setForeground(QColor(0, 0, 0))
            id_item.setBackground(QColor(255, 255, 255))
            table.setItem(row_idx, 0, id_item)

            # 第1列开始填充数据
            for col_idx, cell_data in enumerate(row_data):
                cell_text = str(cell_data) if cell_data is not None else ""
                item = QTableWidgetItem(cell_text)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setForeground(QColor(0, 0, 0))
                item.setBackground(QColor(255, 255, 255))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                table.setItem(row_idx, col_idx + 1, item)

            # 最后一列添加删除按钮
            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(40, 30)  # 增大按钮宽度到40
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
                QPushButton:pressed {
                    background-color: #c62828;
                }
            """)
            delete_btn.clicked.connect(lambda checked, r=row_idx, tid=original_id: self.delete_row(r, tid))
            table.setCellWidget(row_idx, cols - 1, delete_btn)

        # 设置列宽
        table.setColumnWidth(0, 60)  # ID列
        table.setColumnWidth(cols - 1, 60)  # 删除按钮列宽度设为60

        # 设置行高
        table.verticalHeader().setDefaultSectionSize(45)

        # 调整其他列宽
        for col_idx, header in enumerate(display_headers):
            if col_idx == 0 or col_idx == cols - 1:
                continue
            if "名称" in header or "食材" in header:
                table.setColumnWidth(col_idx, 180)
            elif "类别" in header:
                table.setColumnWidth(col_idx, 120)
            elif "蛋白质" in header or "碳水" in header or "脂肪" in header:
                table.setColumnWidth(col_idx, 100)
            else:
                table.setColumnWidth(col_idx, 120)

        table.resizeRowsToContents()

        # 设置编辑委托
        text_delegate = self.StyledItemDelegate()

        # 为类别列设置下拉框委托
        if self.current_table == 'recipes':
            recipe_categories = ["早餐主食", "早餐饮品", "午晚餐主食", "午晚餐鸡类",
                                 "午晚餐鸭类", "午晚餐牛类", "午晚餐猪类",
                                 "午晚餐鱼虾类", "午晚餐蔬菜类", "午晚餐蛋类"]
            category_col = 2
            combo_delegate = ComboBoxDelegate(table, recipe_categories)
            table.setItemDelegateForColumn(category_col, combo_delegate)
        elif self.current_table == 'ingredients':
            ingredient_categories = ["主食", "饮品", "辅料", "调料", "蔬菜", "鱼虾类", "肉类"]
            category_col = 1
            combo_delegate = ComboBoxDelegate(table, ingredient_categories)
            table.setItemDelegateForColumn(category_col, combo_delegate)

        # 为其他列设置文本委托
        for col in range(table.columnCount()):
            if col != 0 and col != cols - 1:
                if (self.current_table == 'recipes' and col == 2) or \
                        (self.current_table == 'ingredients' and col == 1):
                    continue
                table.setItemDelegateForColumn(col, text_delegate)

        # 连接单元格编辑完成信号
        table.itemChanged.connect(lambda item: self.on_cell_edited(item, table, row_id_map))

        table.blockSignals(False)

        self.table_layout.addWidget(table)

        # 添加底部的"添加"按钮
        add_btn = QPushButton("➕ 添加新记录")
        add_btn.setFixedSize(160, 40)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        add_btn.clicked.connect(self.show_add_dialog)

        add_layout = QHBoxLayout()
        add_layout.addStretch()
        add_layout.addWidget(add_btn)
        add_layout.addStretch()

        self.table_layout.addLayout(add_layout)

    class StyledItemDelegate(QStyledItemDelegate):
        """自定义委托，控制编辑时的样式"""

        def createEditor(self, parent, option, index):
            editor = super().createEditor(parent, option, index)
            if isinstance(editor, QLineEdit):
                editor.setStyleSheet("""
                    QLineEdit {
                        background-color: white;
                        color: #000000;
                        selection-background-color: #bbdefb;
                        border: 1px solid #2196F3;
                        border-radius: 3px;
                        padding: 4px;
                    }
                """)
            elif isinstance(editor, QTextEdit):
                editor.setStyleSheet("""
                    QTextEdit {
                        background-color: white;
                        color: #000000;
                        selection-background-color: #bbdefb;
                        border: 1px solid #2196F3;
                        border-radius: 3px;
                        padding: 4px;
                    }
                """)
            return editor

    def on_cell_edited(self, item, table, row_id_map):
        """单元格编辑完成时更新数据库"""
        row = item.row()
        col = item.column()

        if col == 0 or col == table.columnCount() - 1:
            return

        new_value = item.text()
        original_id = row_id_map.get(row)
        if original_id is None:
            return

        field_name = self.current_headers[col - 1]

        if self.current_table == 'recipes':
            field_map = {
                "食谱名称": "name",
                "类别": "category",
                "食材及配量": "ingredients"
            }
        else:
            field_map = {
                "类别": "category",
                "食材名称": "name",
                "蛋白质(g/100g)": "protein",
                "碳水(g/100g)": "carbs",
                "脂肪(g/100g)": "fat",
                "膳食纤维(g/100g)": "fiber",
                "糖类(g/100g)": "sugar",
                "热量(千卡/100g)": "calories"
            }

        db_field = field_map.get(field_name, field_name)
        try:
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()
            query = f"UPDATE {self.current_table} SET {db_field} = ? WHERE id = ?"
            cursor.execute(query, (new_value, original_id))
            conn.commit()
            conn.close()

            # 更新本地数据
            if self.current_table == 'recipes':
                field_index = {
                    "name": 1, "category": 2, "ingredients": 3
                }.get(db_field, col)
            else:
                field_index = {
                    "name": 2, "category": 1, "protein": 3, "carbs": 4,
                    "fat": 5, "fiber": 6, "sugar": 7, "calories": 8
                }.get(db_field, col)

            old_row = list(self.current_data[row])
            old_row[field_index] = new_value
            self.current_data[row] = tuple(old_row)

            self.info_label.setText("✅ 数据已更新")
            # 保存当前值到局部变量，避免 lambda 捕获问题
            current_table = self.current_table
            current_count = len(self.current_data)
            table_display = "📖 食谱表" if current_table == 'recipes' else "🥬 食材表"
            QTimer.singleShot(2000, lambda: self.info_label.setText(f"{table_display} - 共 {current_count} 条记录"))

        except sqlite3.Error as e:
            self.show_error_message(f"更新失败: {str(e)}")

    def delete_row(self, row, record_id):
        """删除行 - 美化确认对话框"""
        # 创建自定义确认对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(420, 350)  # 增加宽度和高度
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 16px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QPushButton {
                border: none;
                border-radius: 20px;
                font-weight: bold;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部装饰条
        top_bar = QWidget()
        top_bar.setFixedHeight(6)
        top_bar.setStyleSheet("background-color: #f44336; border-radius: 16px 16px 0 0;")
        main_layout.addWidget(top_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(35, 35, 35, 35)

        # 图标容器 - 确保图标完整显示
        icon_container = QWidget()
        icon_container.setFixedHeight(80)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel("🗑️")
        icon_label.setStyleSheet("font-size: 60px; background: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)
        content_layout.addWidget(icon_container)

        # 标题
        title_label = QLabel("确认删除")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333;
            background: transparent;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e0e0e0; max-height: 1px; margin: 10px 0;")
        content_layout.addWidget(line)

        # 提示信息
        msg_label = QLabel("确定要删除这条记录吗？")
        msg_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
            background: transparent;
        """)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(msg_label)

        # 警告信息
        warning_label = QLabel("此操作不可撤销！")
        warning_label.setStyleSheet("""
            font-size: 12px;
            color: #f44336;
            background: #ffebee;
            padding: 8px 16px;
            border-radius: 20px;
        """)
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(warning_label)

        content_layout.addStretch()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.addStretch()

        # 确认删除按钮
        confirm_btn = QPushButton("确认删除")
        confirm_btn.setFixedSize(130, 40)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        confirm_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(confirm_btn)

        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(130, 40)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #666;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

        main_layout.addWidget(content_widget)

        if dialog.exec() == QDialog.Accepted:
            try:
                conn = sqlite3.connect("mydb.db")
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {self.current_table} WHERE id = ?", (record_id,))
                conn.commit()
                conn.close()

                del self.current_data[row]
                self.load_table_data(self.current_table)

                self.info_label.setText("✅ 记录已删除")
                # 保存当前值到局部变量
                current_table = self.current_table
                current_count = len(self.current_data)
                table_display = "📖 食谱表" if current_table == 'recipes' else "🥬 食材表"
                QTimer.singleShot(2000, lambda: self.info_label.setText(f"{table_display} - 共 {current_count} 条记录"))
            except sqlite3.Error as e:
                self.show_error_message(f"删除失败: {str(e)}")

    def show_add_dialog(self):
        """显示添加记录的对话框"""
        if self.current_table == 'recipes':
            self.show_add_recipe_dialog()
        else:
            self.show_add_ingredient_dialog()

    def show_add_recipe_dialog(self):
        """添加菜式对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(550, 500)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 15px;
            }
            QLabel {
                color: #333;
                font-size: 14px;
                background: transparent;
                border: none;
                padding: 0px;
            }
            QLineEdit {
                background-color: #f8f9fa;
                color: #333;
                padding: 8px 12px;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 6px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                background-color: white;
            }
            QTextEdit {
                background-color: #f8f9fa;
                color: #333;
                padding: 8px 12px;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 6px;
            }
            QTextEdit:focus {
                border-color: #2196F3;
                background-color: white;
            }
            QComboBox {
                background-color: #f8f9fa;
                color: #333;
                padding: 6px 8px;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 6px;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #2196F3;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #e3f2fd;
                padding: 4px;
            }
            QPushButton {
                padding: 8px 20px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        # 标题
        title = QLabel("➕ 添加新菜式")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #2196F3; background: transparent; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 菜式名称
        name_label = QLabel("菜式名称：")
        layout.addWidget(name_label)
        name_input = QLineEdit()
        name_input.setPlaceholderText("请输入菜式名称")
        layout.addWidget(name_input)

        # 菜式类别
        category_label = QLabel("类别：")
        layout.addWidget(category_label)
        category_combo = QComboBox()
        # 食谱表类别列表
        recipe_categories = ["早餐主食", "早餐饮品", "午晚餐主食", "午晚餐鸡类",
                             "午晚餐鸭类", "午晚餐牛类", "午晚餐猪类",
                             "午晚餐鱼虾类", "午晚餐蔬菜类", "午晚餐蛋类"]
        for name in recipe_categories:
            category_combo.addItem(name)
        layout.addWidget(category_combo)

        # 食材及配量
        ingredients_label = QLabel("食材及配量：")
        layout.addWidget(ingredients_label)
        ingredients_input = QTextEdit()
        ingredients_input.setMaximumHeight(120)
        ingredients_input.setPlaceholderText("例如：鸡胸肉 120g + 洋葱 50g")
        layout.addWidget(ingredients_input)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("添加")
        ok_btn.setStyleSheet("background-color: #4CAF50; color: white; min-width: 100px;")
        ok_btn.clicked.connect(dialog.accept)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("background-color: #f0f0f0; color: #333; min-width: 100px;")
        cancel_btn.clicked.connect(dialog.reject)

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        if dialog.exec() == QDialog.Accepted:
            name = name_input.text().strip()
            category_text = category_combo.currentText()
            ingredients = ingredients_input.toPlainText().strip()

            if not name:
                self.show_error_message("请填写菜式名称！")
                return

            category = category_text

            try:
                conn = sqlite3.connect("mydb.db")
                cursor = conn.cursor()

                cursor.execute("SELECT MAX(id) FROM recipes")
                max_id = cursor.fetchone()[0]
                new_id = (max_id or 0) + 1

                cursor.execute("""
                    INSERT INTO recipes (id, name, category, ingredients)
                    VALUES (?, ?, ?, ?)
                """, (new_id, name, category, ingredients))
                conn.commit()
                conn.close()

                self.load_table_data('recipes')

                self.info_label.setText("✅ 新菜式已添加")
                QTimer.singleShot(2000, lambda: self.info_label.setText(
                    f"📖 食谱表 - 共 {len(self.current_data)} 道菜式"
                ))

            except sqlite3.Error as e:
                self.show_error_message(f"添加失败: {str(e)}")

    def show_add_ingredient_dialog(self):
        """添加食材对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setFixedSize(550, 650)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 15px;
            }
            QLabel {
                color: #333;
                font-size: 14px;
                background: transparent;
                border: none;
                padding: 0px;
            }
            QLineEdit {
                background-color: #f8f9fa;
                color: #333;
                padding: 8px 12px;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 6px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #FF9800;
                background-color: white;
            }
            QComboBox {
                background-color: #f8f9fa;
                color: #333;
                padding: 6px 8px;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 6px;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #FF9800;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #fff3e0;
                padding: 4px;
            }
            QPushButton {
                padding: 8px 20px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        # 标题
        title = QLabel("➕ 添加新食材")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #FF9800; background: transparent; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 食材名称
        name_label = QLabel("食材名称：")
        layout.addWidget(name_label)
        name_input = QLineEdit()
        name_input.setPlaceholderText("请输入食材名称")
        layout.addWidget(name_input)

        # 食材类别
        category_label = QLabel("类别：")
        layout.addWidget(category_label)
        category_combo = QComboBox()
        # 食材类别列表
        ingredient_categories = ["主食", "饮品", "辅料", "调料", "蔬菜", "鱼虾类", "肉类"]
        for name in ingredient_categories:
            category_combo.addItem(name)
        layout.addWidget(category_combo)

        # 营养成分
        nutrient_label = QLabel("营养成分 (每100g)：")
        nutrient_label.setStyleSheet("margin-top: 10px;")
        layout.addWidget(nutrient_label)

        # 创建网格布局用于营养成分
        nutrient_layout = QGridLayout()
        nutrient_layout.setSpacing(10)
        nutrient_layout.setContentsMargins(0, 5, 0, 5)

        protein_label = QLabel("蛋白质(g):")
        nutrient_layout.addWidget(protein_label, 0, 0)
        protein_input = QLineEdit()
        protein_input.setPlaceholderText("0")
        nutrient_layout.addWidget(protein_input, 0, 1)

        carbs_label = QLabel("碳水(g):")
        nutrient_layout.addWidget(carbs_label, 1, 0)
        carbs_input = QLineEdit()
        carbs_input.setPlaceholderText("0")
        nutrient_layout.addWidget(carbs_input, 1, 1)

        fat_label = QLabel("脂肪(g):")
        nutrient_layout.addWidget(fat_label, 2, 0)
        fat_input = QLineEdit()
        fat_input.setPlaceholderText("0")
        nutrient_layout.addWidget(fat_input, 2, 1)

        fiber_label = QLabel("膳食纤维(g):")
        nutrient_layout.addWidget(fiber_label, 3, 0)
        fiber_input = QLineEdit()
        fiber_input.setPlaceholderText("0")
        nutrient_layout.addWidget(fiber_input, 3, 1)

        sugar_label = QLabel("糖类(g):")
        nutrient_layout.addWidget(sugar_label, 4, 0)
        sugar_input = QLineEdit()
        sugar_input.setPlaceholderText("0")
        nutrient_layout.addWidget(sugar_input, 4, 1)

        calories_label = QLabel("热量(千卡):")
        nutrient_layout.addWidget(calories_label, 5, 0)
        calories_input = QLineEdit()
        calories_input.setPlaceholderText("0")
        nutrient_layout.addWidget(calories_input, 5, 1)

        layout.addLayout(nutrient_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("添加")
        ok_btn.setStyleSheet("background-color: #4CAF50; color: white; min-width: 100px;")
        ok_btn.clicked.connect(dialog.accept)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("background-color: #f0f0f0; color: #333; min-width: 100px;")
        cancel_btn.clicked.connect(dialog.reject)

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        if dialog.exec() == QDialog.Accepted:
            name = name_input.text().strip()
            category_text = category_combo.currentText()

            if not name:
                self.show_error_message("请填写食材名称！")
                return

            def get_float(value, default=0):
                try:
                    return float(value) if value else default
                except:
                    return default

            protein = get_float(protein_input.text())
            carbs = get_float(carbs_input.text())
            fat = get_float(fat_input.text())
            fiber = get_float(fiber_input.text())
            sugar = get_float(sugar_input.text())
            calories = get_float(calories_input.text())

            category = category_text

            try:
                conn = sqlite3.connect("mydb.db")
                cursor = conn.cursor()

                cursor.execute("SELECT MAX(id) FROM ingredients")
                max_id = cursor.fetchone()[0]
                new_id = (max_id or 0) + 1

                cursor.execute("""
                    INSERT INTO ingredients (id, category, name, protein, carbs, fat, fiber, sugar, calories)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (new_id, category, name, protein, carbs, fat, fiber, sugar, calories))
                conn.commit()
                conn.close()

                self.load_table_data('ingredients')

                self.info_label.setText("✅ 新食材已添加")
                QTimer.singleShot(2000, lambda: self.info_label.setText(
                    f"🥬 食材表 - 共 {len(self.current_data)} 种食材"
                ))

            except sqlite3.Error as e:
                self.show_error_message(f"添加失败: {str(e)}")

    def show_error_message(self, message):
        """显示错误消息"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("错误")
        msg_box.setText(str(message))
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI膳食搭配系统")
        self.setMinimumSize(1200, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)

        self.create_button_panel()
        self.create_initial_content()
        self.create_statusbar()

        self.setup_connections()

    def create_button_panel(self):
        button_panel = QWidget()
        button_panel.setFixedWidth(180)
        button_panel.setStyleSheet("""
            QWidget {
                background-color: #bbdefb;  /* 浅蓝色背景 */
                border-radius: 10px;
            }
        """)

        button_layout = QVBoxLayout(button_panel)
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(20, 30, 20, 30)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_ai_plan = QPushButton("🤖 AI搭配")
        self.btn_calc = QPushButton("🧮 营养计算")
        self.btn_db = QPushButton("🗄️ 数据库管理")

        button_size = QSize(140, 50)
        self.btn_ai_plan.setFixedSize(button_size)
        self.btn_calc.setFixedSize(button_size)
        self.btn_db.setFixedSize(button_size)

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """

        self.btn_ai_plan.setStyleSheet(button_style)
        self.btn_calc.setStyleSheet(button_style)
        self.btn_db.setStyleSheet(button_style)

        button_layout.addWidget(self.btn_ai_plan)
        button_layout.addWidget(self.btn_calc)
        button_layout.addWidget(self.btn_db)
        button_layout.addStretch()

        self.main_layout.addWidget(button_panel)

        self.btn_ai_plan.setStyleSheet(button_style)
        self.btn_calc.setStyleSheet(button_style)
        self.btn_db.setStyleSheet(button_style)

        button_layout.addWidget(self.btn_ai_plan)
        button_layout.addWidget(self.btn_calc)
        button_layout.addWidget(self.btn_db)
        button_layout.addStretch()

        self.main_layout.addWidget(button_panel)

    def create_initial_content(self):
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        welcome_label = QLabel("欢迎使用 AI 膳食搭配系统")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        layout.addWidget(welcome_label)

        info_label = QLabel("请从左侧选择功能")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 14px; color: #666;")
        layout.addWidget(info_label)

        layout.addStretch()

        self.main_layout.addWidget(self.content_widget, stretch=1)

    def create_statusbar(self):
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #f0f0f0;
                color: #333;
                padding: 5px;
            }
        """)
        self.statusBar().showMessage("就绪")

    def switch_content(self, new_widget, title):
        self.main_layout.removeWidget(self.content_widget)
        self.content_widget.deleteLater()
        self.content_widget = new_widget
        self.main_layout.addWidget(self.content_widget, stretch=1)
        self.statusBar().showMessage(f"当前：{title}")

    def setup_connections(self):
        self.btn_ai_plan.clicked.connect(self.on_ai_plan_clicked)
        self.btn_calc.clicked.connect(self.on_calc_clicked)
        self.btn_db.clicked.connect(self.on_db_clicked)

    def on_ai_plan_clicked(self):
        self.switch_content(AIPlannerWidget(), "AI搭配")

    def on_calc_clicked(self):
        self.switch_content(NutritionCalcWidget(), "营养计算")

    def on_db_clicked(self):
        self.switch_content(DatabaseManagerWidget(), "数据库管理")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())