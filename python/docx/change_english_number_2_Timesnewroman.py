import re
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
import shutil


def set_run_font_to_times(run):
    """
    将单个run的字体设置为Times New Roman，保持原有大小和粗细
    """
    # 获取原有字体大小（如果没有则默认为None）
    original_size = run.font.size
    original_bold = run.font.bold
    original_italic = run.font.italic

    # 设置西文字体为Times New Roman
    run.font.name = 'Times New Roman'

    # 关键步骤：设置XML中的字体，确保英文生效
    r = run._element
    rPr = r.get_or_add_rPr()

    # 设置西文字体
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), '宋体')  # 中文字体保持宋体（可按需修改）
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')

    # 恢复原有大小和粗细（如果之前有设置的话）
    if original_size is not None:
        run.font.size = original_size
    if original_bold is not None:
        run.font.bold = original_bold
    if original_italic is not None:
        run.font.italic = original_italic


def is_english_or_digit(text):
    """
    判断文本是否包含英文或数字
    """
    return bool(re.search(r'[a-zA-Z0-9]', text))


def process_paragraph(paragraph):
    """
    处理单个段落，将其中英文和数字的run字体改为Times New Roman
    """
    # 如果段落没有run，直接返回
    if not paragraph.runs:
        return

    # 逐个处理run
    for run in paragraph.runs:
        text = run.text
        if text and is_english_or_digit(text):
            # 这个run包含英文或数字，改为Times New Roman
            set_run_font_to_times(run)


def process_document(doc_path):
    """
    处理整个docx文档，直接覆盖原文件
    """
    # 先创建一个临时备份，以防处理出错
    temp_backup = doc_path + ".temp_backup"
    try:
        # 复制原文件作为临时备份
        shutil.copy2(doc_path, temp_backup)

        # 打开文档
        doc = Document(doc_path)

        # 遍历所有段落
        for paragraph in doc.paragraphs:
            process_paragraph(paragraph)

        # 遍历所有表格中的段落
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        process_paragraph(paragraph)

        # 直接保存覆盖原文件
        doc.save(doc_path)
        print(f"✓ 处理完成并已覆盖：{doc_path}")

        # 删除临时备份
        if os.path.exists(temp_backup):
            os.remove(temp_backup)

    except Exception as e:
        # 如果出错，从临时备份恢复
        print(f"✗ 处理出错：{e}")
        if os.path.exists(temp_backup):
            shutil.copy2(temp_backup, doc_path)
            os.remove(temp_backup)
            print(f"已从备份恢复原文件")
        raise


def batch_process_folder(folder_path):
    """
    批量处理文件夹中的所有docx文件（直接覆盖）
    """
    docx_files = [f for f in os.listdir(folder_path) if f.endswith('.docx')]

    if not docx_files:
        print("该文件夹中没有找到docx文件")
        return

    print(f"找到 {len(docx_files)} 个docx文件")
    print("=" * 50)

    success_count = 0
    fail_count = 0

    for i, filename in enumerate(docx_files, 1):
        file_path = os.path.join(folder_path, filename)
        print(f"[{i}/{len(docx_files)}] 正在处理：{filename}...")
        try:
            process_document(file_path)
            success_count += 1
        except Exception as e:
            print(f"  ✗ 处理失败：{e}")
            fail_count += 1

    print("=" * 50)
    print(f"处理完成！成功：{success_count} 个，失败：{fail_count} 个")


def main():
    """
    主函数 - 提供交互式选择
    """
    print("=" * 50)
    print("Word文档英文转Times New Roman工具（直接覆盖原文件）")
    print("⚠️  警告：此操作将直接修改原文件，建议提前备份！")
    print("=" * 50)

    # 安全确认
    confirm = input("\n是否继续？(输入 yes 继续，其他任意键退出): ").strip().lower()
    if confirm != 'yes':
        print("已取消操作")
        return

    print("\n请选择模式：")
    print("1. 处理单个文件")
    print("2. 批量处理文件夹")
    print("3. 退出")

    choice = input("\n请输入数字选择 (1/2/3): ").strip()

    if choice == '1':
        file_path = input("请输入docx文件路径: ").strip()
        if not os.path.exists(file_path):
            print("文件不存在！")
            return
        # 再次确认
        confirm2 = input(f"确认要覆盖 {file_path} 吗？(y/n): ").strip().lower()
        if confirm2 != 'y':
            print("已取消操作")
            return
        process_document(file_path)

    elif choice == '2':
        folder_path = input("请输入文件夹路径: ").strip()
        if not os.path.exists(folder_path):
            print("文件夹不存在！")
            return
        # 列出将处理的文件
        docx_files = [f for f in os.listdir(folder_path) if f.endswith('.docx')]
        if not docx_files:
            print("该文件夹中没有docx文件")
            return
        print(f"\n将处理以下 {len(docx_files)} 个文件：")
        for f in docx_files:
            print(f"  - {f}")
        confirm2 = input(f"\n确认要覆盖这些文件吗？(y/n): ").strip().lower()
        if confirm2 != 'y':
            print("已取消操作")
            return
        batch_process_folder(folder_path)

    elif choice == '3':
        print("退出程序")
        return

    else:
        print("无效输入")


if __name__ == "__main__":
    main()