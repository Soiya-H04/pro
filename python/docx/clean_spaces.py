import re
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
import shutil


def is_chinese(char):
    """
    判断一个字符是否为中文字符
    """
    return '\u4e00' <= char <= '\u9fff'


def is_english_or_digit(char):
    """
    判断一个字符是否为英文字母或数字
    """
    return char.isalpha() and char.isascii() or char.isdigit()


def clean_spaces_in_text(text):
    """
    清理文本中的多余空格
    规则：
    1. 段首空两格保留（由单独的缩进功能处理）
    2. 两个英文单词之间的空格保留
    3. 英文单词与中文之间的空格删除
    4. 中文与中文之间的空格删除
    5. 中文与数字之间的空格删除
    6. 连续多个空格合并为一个（英文单词之间除外）
    """
    if not text:
        return text

    # 先处理特殊情况：如果文本全是空格，直接返回
    if text.strip() == '':
        return text

    result = []
    i = 0
    length = len(text)

    while i < length:
        char = text[i]

        # 如果当前字符不是空格，直接添加
        if char != ' ':
            result.append(char)
            i += 1
            continue

        # 当前字符是空格，需要判断是否保留
        # 检查空格前后的字符
        prev_char = text[i - 1] if i > 0 else None
        next_char = text[i + 1] if i < length - 1 else None

        # 跳过开头和结尾的空格（段首和段尾由专门的函数处理）
        if i == 0:
            i += 1
            continue

        # 如果后面没有字符了（段尾），删除
        if next_char is None:
            i += 1
            continue

        # 判断前后字符类型
        prev_is_chinese = is_chinese(prev_char) if prev_char else False
        prev_is_english = is_english_or_digit(prev_char) if prev_char else False
        next_is_chinese = is_chinese(next_char) if next_char else False
        next_is_english = is_english_or_digit(next_char) if next_char else False

        # 判断是否保留空格
        keep_space = False

        # 规则：两个英文单词之间保留空格（前后都是英文字母或数字）
        if prev_is_english and next_is_english:
            keep_space = True

        # 规则：英文单词与中文之间删除空格（无论英文在前还是中文在前）
        # 这里已经包含了：英文+空格+中文 和 中文+空格+英文 的情况
        # 因为前后不是英文+英文的情况，所以删除

        # 规则：数字与中文之间删除空格（数字被包含在英文判断中）
        # 规则：中文与中文之间删除空格

        if keep_space:
            result.append(char)
        # 否则删除空格，不添加到结果中

        i += 1

    # 处理连续多个空格的情况（在英文之间保留一个）
    final_result = []
    prev_char = None
    for char in result:
        if char == ' ' and prev_char == ' ':
            # 如果前一个字符也是空格，跳过（合并连续空格）
            continue
        final_result.append(char)
        prev_char = char

    return ''.join(final_result)


def clean_paragraph_spacing(paragraph):
    """
    清理段落中的多余空格，同时保留段首空两格
    """
    # 如果段落没有run，直接返回
    if not paragraph.runs:
        return

    # 获取段落的完整文本
    full_text = ''.join(run.text for run in paragraph.runs)

    # 检查段首是否有空格（用于判断是否保留了首行缩进）
    # 如果段首有两个空格，记录下来
    has_indent = full_text.startswith('  ') or full_text.startswith('　　')
    indent_spaces = ''
    if full_text.startswith('  '):
        indent_spaces = '  '
    elif full_text.startswith('　　'):
        indent_spaces = '　　'

    # 清理段首空格后的文本（保留首行缩进的空格）
    if has_indent:
        text_to_clean = full_text[2:]
    else:
        text_to_clean = full_text

    # 清理多余空格
    cleaned_text = clean_spaces_in_text(text_to_clean)

    # 重新组合（加上段首缩进）
    if has_indent:
        cleaned_text = indent_spaces + cleaned_text

    # 如果文本没有变化，跳过
    if cleaned_text == full_text:
        return

    # 将清理后的文本写回段落
    # 先清空所有run
    for run in paragraph.runs:
        run.text = ''

    # 在第一个run中设置新文本（保持原有格式）
    if paragraph.runs:
        paragraph.runs[0].text = cleaned_text
        # 复制其他run的属性到第一个run（保留格式）
        # 但为了简单起见，我们清空其他run，只保留第一个
        for run in paragraph.runs[1:]:
            run.text = ''
    else:
        # 如果没有run，创建一个
        paragraph.add_run(cleaned_text)


def should_skip_paragraph(paragraph):
    """
    判断是否应该跳过某些特殊段落
    """
    # 跳过空段落
    if not paragraph.text.strip():
        return True

    # 可以添加更多跳过条件，比如表格中的特殊内容

    return False


def process_document_spaces(doc_path):
    """
    处理文档中的多余空格
    """
    # 创建临时备份
    temp_backup = doc_path + ".temp_backup"
    try:
        shutil.copy2(doc_path, temp_backup)

        doc = Document(doc_path)
        modified_count = 0

        # 处理所有段落
        for paragraph in doc.paragraphs:
            if should_skip_paragraph(paragraph):
                continue

            # 保存原始文本用于比较
            original_text = paragraph.text
            clean_paragraph_spacing(paragraph)

            # 检查是否发生了变化
            if paragraph.text != original_text:
                modified_count += 1

        # 处理所有表格中的段落
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if should_skip_paragraph(paragraph):
                            continue
                        original_text = paragraph.text
                        clean_paragraph_spacing(paragraph)
                        if paragraph.text != original_text:
                            modified_count += 1

        # 保存文档
        doc.save(doc_path)
        print(f"✓ 处理完成：{doc_path} (修改了 {modified_count} 个段落)")

        # 删除临时备份
        if os.path.exists(temp_backup):
            os.remove(temp_backup)

        return modified_count

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
    批量处理文件夹中的所有docx文件
    """
    docx_files = [f for f in os.listdir(folder_path) if f.endswith('.docx')]

    if not docx_files:
        print("该文件夹中没有找到docx文件")
        return

    print(f"找到 {len(docx_files)} 个docx文件")
    print("=" * 50)

    success_count = 0
    fail_count = 0
    total_modified = 0

    for i, filename in enumerate(docx_files, 1):
        file_path = os.path.join(folder_path, filename)
        print(f"[{i}/{len(docx_files)}] 正在处理：{filename}...")
        try:
            modified = process_document_spaces(file_path)
            success_count += 1
            total_modified += modified
        except Exception as e:
            print(f"  ✗ 处理失败：{e}")
            fail_count += 1

    print("=" * 50)
    print(f"处理完成！成功：{success_count} 个，失败：{fail_count} 个")
    print(f"总共修改了 {total_modified} 个段落")


def main():
    """
    主函数
    """
    print("=" * 60)
    print("Word文档多余空格清理工具")
    print("规则说明：")
    print("  ✓ 保留段首空两格")
    print("  ✓ 保留英文单词之间的空格")
    print("  ✓ 删除英文与中文之间的空格")
    print("  ✓ 删除中文之间的空格")
    print("  ✓ 删除中文与数字之间的空格")
    print("  ✓ 合并连续多个空格为一个（英文之间除外）")
    print("=" * 60)
    print("⚠️  警告：此操作将直接修改原文件，建议提前备份！")
    print("=" * 60)

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
        confirm2 = input(f"确认要修改 {file_path} 吗？(y/n): ").strip().lower()
        if confirm2 != 'y':
            print("已取消操作")
            return
        process_document_spaces(file_path)

    elif choice == '2':
        folder_path = input("请输入文件夹路径: ").strip()
        if not os.path.exists(folder_path):
            print("文件夹不存在！")
            return
        docx_files = [f for f in os.listdir(folder_path) if f.endswith('.docx')]
        if not docx_files:
            print("该文件夹中没有docx文件")
            return
        print(f"\n将处理以下 {len(docx_files)} 个文件：")
        for f in docx_files:
            print(f"  - {f}")
        confirm2 = input(f"\n确认要修改这些文件吗？(y/n): ").strip().lower()
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