import os
import re
import sys
from pathlib import Path


def extract_chinese_prefix_and_number(filename):
    """从文件名中提取汉字前缀和数字
    例如: '照片1.jpg' -> ('照片', 1)
          '慰001.jpg' -> ('慰', 1)
          '文件100.jpg' -> ('文件', 100)
    """
    # 匹配开头的汉字和后面的数字
    match = re.match(r'^([\u4e00-\u9fa5]+)(\d+)', filename)
    if match:
        prefix = match.group(1)  # 汉字前缀
        number = int(match.group(2))  # 数字
        return prefix, number
    return None, None


def clean_path(path):
    """清理路径，去除首尾的双引号、单引号和多余空格"""
    path = path.strip()
    # 去除首尾的双引号
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    # 去除首尾的单引号
    elif path.startswith("'") and path.endswith("'"):
        path = path[1:-1]
    return path


def get_files_in_folder(folder_path):
    """获取文件夹中所有以汉字开头+数字的文件"""
    files = []
    for file in os.listdir(folder_path):
        prefix, number = extract_chinese_prefix_and_number(file)
        if prefix and number is not None:
            files.append((file, prefix, number))

    # 按汉字前缀分组，然后按数字排序
    files.sort(key=lambda x: (x[1], x[2]))
    return files


def analyze_file_numbers(files_data):
    """分析文件数字的连续性

    Returns:
        dict: 包含每个前缀的数字列表、缺失数字等信息
    """
    prefix_info = {}
    for file, prefix, number in files_data:
        if prefix not in prefix_info:
            prefix_info[prefix] = {
                'numbers': [],
                'files': []
            }
        prefix_info[prefix]['numbers'].append(number)
        prefix_info[prefix]['files'].append((file, number))

    # 分析每个前缀的连续性
    for prefix, info in prefix_info.items():
        numbers = info['numbers']
        if numbers:
            min_num = min(numbers)
            max_num = max(numbers)
            expected = list(range(min_num, max_num + 1))
            missing = [n for n in expected if n not in numbers]
            info['min'] = min_num
            info['max'] = max_num
            info['missing'] = missing
            info['is_continuous'] = len(missing) == 0

    return prefix_info


def rename_files(folder_path, digits=None, start_number=1):
    """重命名文件

    Args:
        folder_path: 文件夹路径
        digits: 自定义位数
        start_number: 起始数字
    """
    files_data = get_files_in_folder(folder_path)

    if not files_data:
        print("未找到以'汉字开头+数字'命名的文件！")
        return False

    # 分析文件数字情况
    prefix_info = analyze_file_numbers(files_data)

    print(f"找到 {len(files_data)} 个文件")
    print("\n文件分析：")
    print("-" * 70)

    for prefix, info in prefix_info.items():
        print(f"\n【{prefix}】组:")
        print(f"  文件数量: {len(info['numbers'])} 个")
        print(f"  数字范围: {info['min']} - {info['max']}")

        if info['missing']:
            missing_str = str(info['missing'][:10])
            if len(info['missing']) > 10:
                missing_str += '...'
            print(f"  ⚠️  缺失数字: {missing_str}")
            print(f"  连续性: ❌ 不连续（缺少 {len(info['missing'])} 个数字）")
            print(f"  建议: 将重新排序为 {start_number} - {start_number + len(info['numbers']) - 1}")
        else:
            print(f"  连续性: ✓ 连续")

    print("\n" + "-" * 70)

    # 确定使用的位数
    if digits is None:
        # 自动计算：根据文件总数和起始数字
        total_files = len(files_data)
        max_num = start_number + total_files - 1
        digits = len(str(max_num))

    print(f"\n将使用 {digits} 位数字格式")
    print(f"起始数字: {start_number}")

    # 显示将要进行的重命名
    print("\n" + "=" * 70)
    print("重命名预览：")
    print("=" * 70)

    rename_list = []
    # 按前缀分组处理
    current_num = start_number

    for prefix, info in prefix_info.items():
        print(f"\n【{prefix}】组:")
        # 获取该组的所有文件（已排序）
        group_files = [f for f in files_data if f[1] == prefix]

        for item in group_files:
            old_name = item[0]
            old_num = item[2]

            # 计算新的数字
            new_num = current_num
            current_num += 1

            # 获取文件扩展名
            file_path = Path(folder_path) / old_name
            extension = file_path.suffix

            # 构造新文件名
            new_name = f"{prefix}{str(new_num).zfill(digits)}{extension}"
            new_path = Path(folder_path) / new_name

            # 检查新文件名是否已存在
            if new_path.exists() and new_path != file_path:
                print(f"  ⚠️  跳过: {old_name:30} -> {new_name} (目标文件已存在)")
                continue

            rename_list.append((old_name, new_name, old_num, new_num))
            print(f"  {old_name:30} -> {new_name}  (原数字: {old_num})")

    print("\n" + "=" * 70)
    print(f"共 {len(rename_list)} 个文件需要重命名")

    if not rename_list:
        print("没有文件需要重命名")
        return False

    # 显示统计信息
    has_missing = any(info.get('missing') for info in prefix_info.values())
    if has_missing:
        print("\n📊 检测到数字不连续，将按顺序重新编号")
        missing_info = []
        for p, info in prefix_info.items():
            if info.get('missing'):
                missing_info.append(f"{p}: {info['min']}-{info['max']}")
        print(f"   将从不连续的: {missing_info}")
        print(f"   重新编号为: 连续从 {start_number} 开始")

    # 询问是否执行重命名
    print("\n请选择操作：")
    print("1. 执行重命名")
    print("2. 取消操作")

    while True:
        choice = input("请选择 (1/2): ").strip()
        if choice == '1':
            break
        elif choice == '2':
            print("操作已取消")
            return False
        else:
            print("请输入 1 或 2")

    # 执行重命名
    print("\n开始重命名...")
    print("-" * 70)

    success_count = 0
    fail_count = 0

    # 按原数字排序，确保重命名顺序正确（从大到小重命名避免冲突）
    rename_list.sort(key=lambda x: x[2], reverse=True)  # 按原数字从大到小排序

    for old_name, new_name, old_num, new_num in rename_list:
        old_path = Path(folder_path) / old_name
        new_path = Path(folder_path) / new_name

        try:
            os.rename(old_path, new_path)
            print(f"✓ {old_name:30} -> {new_name}  (原数字: {old_num} -> 新数字: {new_num})")
            success_count += 1
        except Exception as e:
            print(f"✗ 重命名 {old_name} 失败: {e}")
            fail_count += 1

    print("-" * 70)
    print(f"\n重命名完成！")
    print(f"成功: {success_count} 个文件")
    if fail_count > 0:
        print(f"失败: {fail_count} 个文件")

    return True


def main():
    """主函数"""
    print("=" * 70)
    print("文件批量重命名工具 - 汉字开头+数字 格式")
    print("=" * 70)
    print("\n💡 提示：可以直接粘贴带双引号的文件夹路径")
    print("   例如：\"D:\\my文件夹\" 或 'D:\\my文件夹'")
    print()

    # 获取文件夹路径
    while True:
        folder_input = input("请输入文件夹路径（直接回车使用当前目录）: ").strip()

        if not folder_input:
            folder_path = os.getcwd()
            break

        # 清理路径（去除引号）
        folder_path = clean_path(folder_input)

        # 检查路径是否存在
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            break
        else:
            print("❌ 路径不存在或不是文件夹，请重新输入")
            print(f"   您输入的路径: {folder_input}")
            print(f"   清理后的路径: {folder_path}")

    print(f"当前文件夹: {folder_path}")

    # 扫描文件
    files_data = get_files_in_folder(folder_path)

    if not files_data:
        print("\n⚠️  未找到以'汉字开头+数字'命名的文件！")
        input("\n按回车键退出...")
        return

    # 显示文件列表（只显示前10个和后10个）
    print(f"\n找到 {len(files_data)} 个文件")
    print("\n当前文件命名示例：")
    display_files = [f[0] for f in files_data]
    if len(display_files) <= 20:
        for f in display_files:
            print(f"  {f}")
    else:
        for f in display_files[:10]:
            print(f"  {f}")
        print("  ...")
        for f in display_files[-10:]:
            print(f"  {f}")

    # 选择配置
    print("\n" + "-" * 70)
    print("请选择配置方式：")
    print("1. 自动配置（推荐）")
    print("2. 自定义配置")

    choice = input("请选择 (1/2): ").strip()

    digits = None
    start_number = 1

    if choice == '2':
        # 自定义位数
        while True:
            try:
                digits_input = input("请输入数字位数（如3表示001，4表示0001，直接回车自动计算）: ").strip()
                if not digits_input:
                    digits = None
                    break
                digits = int(digits_input)
                if digits >= 1:
                    break
                print("位数必须大于0")
            except ValueError:
                print("请输入有效的数字")

        # 自定义起始数字
        while True:
            try:
                start_input = input("请输入起始数字（如 5，直接回车从1开始）: ").strip()
                if not start_input:
                    start_number = 1
                    break
                start_number = int(start_input)
                if start_number >= 0:
                    break
                print("起始数字必须大于等于0")
            except ValueError:
                print("请输入有效的数字")
    else:
        print("将自动计算位数，起始数字为1")
        start_number = 1

    # 执行重命名（包含预览和确认）
    print("\n" + "=" * 70)
    rename_files(folder_path, digits, start_number)

    print("\n" + "=" * 70)
    input("按回车键退出...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {e}")
        input("\n按回车键退出...")
        sys.exit(1)