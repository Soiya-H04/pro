import os
from pathlib import Path


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


def create_test_files(folder_path=None, prefix="测试", start=1, end=100, extensions=None):
    """创建测试文件

    Args:
        folder_path: 文件夹路径，None表示当前目录
        prefix: 文件前缀（汉字）
        start: 起始数字
        end: 结束数字
        extensions: 文件扩展名列表，默认['.txt']
    """
    if folder_path is None:
        folder_path = os.getcwd()

    if extensions is None:
        extensions = ['.txt']

    # 创建文件夹（如果不存在）
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    print(f"正在创建测试文件...")
    print(f"文件夹: {folder_path}")
    print(f"前缀: {prefix}")
    print(f"数字范围: {start} - {end}")
    print(f"扩展名: {', '.join(extensions)}")
    print("-" * 60)

    created_count = 0
    skipped_count = 0

    for i in range(start, end + 1):
        for ext in extensions:
            # 使用数字格式（不带补零）
            filename = f"{prefix}{i}{ext}"
            filepath = Path(folder_path) / filename

            # 检查文件是否已存在
            if filepath.exists():
                print(f"⚠️  跳过: {filename} (文件已存在)")
                skipped_count += 1
                continue

            # 创建文件并写入内容
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"这是测试文件 {filename}\n")
                    f.write(f"创建时间: {Path(filepath).stat().st_ctime if filepath.exists() else '新文件'}\n")
                    f.write(f"这是第 {i} 个测试文件\n")
                    f.write(f"前缀: {prefix}\n")
                    f.write(f"数字: {i}\n")

                print(f"✓ 创建: {filename}")
                created_count += 1
            except Exception as e:
                print(f"✗ 创建失败: {filename} - {e}")

    print("-" * 60)
    print(f"\n创建完成！")
    print(f"成功创建: {created_count} 个文件")
    if skipped_count > 0:
        print(f"跳过（已存在）: {skipped_count} 个文件")
    print(f"总计: {created_count + skipped_count} 个文件")


def main():
    """主函数"""
    print("=" * 60)
    print("测试文件创建工具")
    print("=" * 60)
    print("\n💡 提示：可以直接粘贴带双引号的文件夹路径")
    print("   例如：\"D:\\my文件夹\" 或 'D:\\my文件夹'")
    print()

    # 获取文件夹路径
    while True:
        folder_input = input("请输入文件夹路径（直接回车使用当前目录的 'test_files' 文件夹）: ").strip()

        if not folder_input:
            folder_path = os.path.join(os.getcwd(), "test_files")
            print(f"将使用: {folder_path}")
            break

        # 清理路径（去除引号）
        folder_path = clean_path(folder_input)

        # 检查路径是否有效（如果不是绝对路径，创建相对路径）
        if os.path.exists(folder_path):
            if os.path.isdir(folder_path):
                break
            else:
                print(f"❌ 路径存在但不是文件夹: {folder_path}")
                print(f"   您输入的路径: {folder_input}")
                continue
        else:
            # 路径不存在，询问是否创建
            print(f"⚠️  路径不存在: {folder_path}")
            create_choice = input("是否创建该文件夹？(y/n): ").strip().lower()
            if create_choice == 'y':
                try:
                    Path(folder_path).mkdir(parents=True, exist_ok=True)
                    print(f"✓ 文件夹已创建: {folder_path}")
                    break
                except Exception as e:
                    print(f"❌ 创建文件夹失败: {e}")
                    continue
            else:
                print("请重新输入路径")
                continue

    # 选择文件前缀
    prefix = input("请输入文件前缀（汉字，如'测试'、'文件'、'慰'，直接回车使用'测试'）: ").strip()
    if not prefix:
        prefix = "测试"
        print(f"将使用: {prefix}")

    # 选择数字范围
    print("\n请设置数字范围：")
    try:
        start_input = input("请输入起始数字（直接回车从1开始）: ").strip()
        start = int(start_input) if start_input else 1

        end_input = input("请输入结束数字（直接回车到100）: ").strip()
        end = int(end_input) if end_input else 100

        if start > end:
            print("❌ 起始数字不能大于结束数字！")
            return

        print(f"数字范围: {start} - {end}")
    except ValueError:
        print("❌ 请输入有效的数字！")
        return

    # 选择文件扩展名
    print("\n请选择文件扩展名：")
    print("1. 仅 .txt")
    print("2. .txt 和 .jpg")
    print("3. .txt, .jpg, .png")
    print("4. 自定义")

    choice = input("请选择 (1-4): ").strip()

    if choice == '1':
        extensions = ['.txt']
    elif choice == '2':
        extensions = ['.txt', '.jpg']
    elif choice == '3':
        extensions = ['.txt', '.jpg', '.png']
    elif choice == '4':
        ext_input = input("请输入扩展名（用逗号分隔，如 .txt,.jpg）: ").strip()
        extensions = [ext.strip() for ext in ext_input.split(',') if ext.strip()]
        if not extensions:
            extensions = ['.txt']
            print("未输入扩展名，使用默认 .txt")
    else:
        extensions = ['.txt']
        print("无效选择，使用默认 .txt")

    print(f"将创建: {', '.join(extensions)} 格式文件")

    # 确认创建
    print("\n" + "=" * 60)
    print("创建配置确认：")
    print(f"  文件夹: {folder_path}")
    print(f"  前缀: {prefix}")
    print(f"  数字范围: {start} - {end} (共 {end - start + 1} 个数字)")
    print(f"  扩展名: {', '.join(extensions)}")
    print(f"  预计创建文件数: {(end - start + 1) * len(extensions)} 个")
    print("=" * 60)

    confirm = input("\n是否继续创建？(y/n): ").strip().lower()
    if confirm != 'y':
        print("操作已取消")
        input("\n按回车键退出...")
        return

    # 创建文件
    create_test_files(folder_path, prefix, start, end, extensions)

    print("\n" + "=" * 60)
    print("文件创建完成！")
    print(f"你可以将 {folder_path} 中的文件用于测试重命名工具")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
        input("\n按回车键退出...")
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n发生错误: {e}")
        input("\n按回车键退出...")