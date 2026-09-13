import os
import subprocess
import shutil
import re

# 支持的视频格式
video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')


def get_video_duration(file_path):
    """获取视频时长（秒）"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def trim_video_ffmpeg(file_path, temp_folder, start_time, end_time=None):
    """使用 FFmpeg 裁剪视频"""
    try:
        filename = os.path.basename(file_path)
        duration = get_video_duration(file_path)

        if start_time >= duration:
            print(f"  跳过: 开始时间 {start_time}s 超过视频时长 {duration:.1f}s")
            return False

        if end_time is None or end_time > duration:
            end_time = duration

        clip_duration = end_time - start_time
        if clip_duration < 0.5:
            print(f"  跳过: 裁剪后时长 {clip_duration:.1f}s 太短")
            return False

        print(f"  视频时长 {duration:.1f}s，裁剪 [{start_time:.1f}s -> {end_time:.1f}s]，时长 {clip_duration:.1f}s")

        os.makedirs(temp_folder, exist_ok=True)
        temp_path = os.path.join(temp_folder, f"temp_{os.getpid()}_{filename}")

        # ===== 根据裁剪时长选择模式 =====
        if clip_duration <= 5:
            print(f"  使用精确模式（裁剪时长 {clip_duration:.1f}s ≤ 5s）")
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(start_time),
                '-to', str(end_time),
                '-i', file_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'veryfast',
                '-crf', '23',
                '-avoid_negative_ts', '1',
                temp_path
            ]
        else:
            print(f"  使用快速模式（裁剪时长 {clip_duration:.1f}s > 5s）")
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(start_time),
                '-to', str(end_time),
                '-i', file_path,
                '-c', 'copy',
                '-avoid_negative_ts', '1',
                temp_path
            ]

        subprocess.run(cmd, capture_output=True, check=True)

        os.remove(file_path)
        shutil.move(temp_path, file_path)

        print(f"  完成: {filename}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"  FFmpeg 错误: {e.stderr.decode() if e.stderr else '未知错误'}")
        temp_path = os.path.join(temp_folder, f"temp_{os.getpid()}_{filename}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False
    except Exception as e:
        print(f"  错误: {e}")
        return False


def parse_time_input(time_str):
    """解析时间输入"""
    time_str = time_str.strip()

    try:
        return float(time_str)
    except ValueError:
        pass

    if ':' in time_str:
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

    pattern = r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?'
    match = re.match(pattern, time_str.lower())
    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        return hours * 3600 + minutes * 60 + seconds

    raise ValueError(f"无法解析时间格式: {time_str}")


def parse_pattern(pattern, video_files):
    """
    解析通配符模式，返回匹配的视频列表
    支持格式（适配重命名后的带前导零文件名）：
      - 慰[1-20]          -> 匹配 慰00001.mp4 到 慰00020.mp4
      - 慰[1-20,25-88]    -> 匹配 慰1-20 和 慰25-88
      - 慰[1,3,5]         -> 匹配 慰1, 慰3, 慰5
      - 视频[1-5]         -> 匹配 视频00001.mp4 到 视频00005.mp4
    """
    matched = []

    # 解析模式：提取前缀、数字范围和后缀
    pattern_pattern = r'^(.*?)\[(.*?)\](.*?)$'
    match = re.match(pattern_pattern, pattern)

    if not match:
        # 如果不是 [范围] 格式，当作普通字符串匹配
        return [f for f in video_files if pattern in f]

    prefix = match.group(1)
    range_str = match.group(2)
    suffix = match.group(3)

    # 解析范围字符串
    numbers = set()
    for part in range_str.split(','):
        part = part.strip()
        if '-' in part:
            parts = part.split('-')
            try:
                start = int(parts[0])
                end = int(parts[1])
                numbers.update(range(start, end + 1))
            except ValueError:
                print(f"警告: 忽略无效范围 '{part}'")
        else:
            try:
                numbers.add(int(part))
            except ValueError:
                print(f"警告: 忽略无效数字 '{part}'")

    # ===== 关键改动：匹配时忽略前导零 =====
    for num in numbers:
        # 先尝试精确匹配：前缀 + 数字 + 后缀
        target_name = f"{prefix}{num}{suffix}"
        # 再尝试匹配带前导零的版本（任意位数）
        # 例如：慰1 匹配 慰00001, 慰001, 慰1
        for f in video_files:
            name_without_ext = os.path.splitext(f)[0]

            # 精确匹配
            if name_without_ext == target_name:
                matched.append(f)
                break

            # 模糊匹配：提取文件名中的数字部分，忽略前导零
            # 匹配格式：前缀 + 数字（可能有前导零） + 后缀
            # 例如：慰00001 -> 前缀=慰，数字=1，后缀=''
            pattern_match = re.match(rf'^{re.escape(prefix)}(\d+){re.escape(suffix)}$', name_without_ext)
            if pattern_match:
                file_num = int(pattern_match.group(1))  # 转成数字去掉前导零
                if file_num == num:
                    matched.append(f)
                    break

    return matched


def select_videos(video_folder, video_files):
    """让用户选择要处理的视频"""
    print("\n" + "=" * 60)
    print("选择要处理的视频")
    print("=" * 60)
    print("\n支持的选择方式：")
    print("  1. 处理所有视频")
    print("  2. 通配符模式，例如：")
    print("     慰[1-20]          ")
    print("     慰[1-20,25-88]    ")
    print("     慰[1,3,5,7]       ")
    print("  3. 输入视频编号（用逗号或空格分隔）")
    print("  4. 输入编号范围（如 1-5）")
    print("-" * 60)

    # 显示所有视频（简化显示，去掉前导零）
    print("\n视频列表：")
    for i, f in enumerate(video_files, 1):
        # 提取文件名中的数字部分，显示更简洁
        name_without_ext = os.path.splitext(f)[0]
        num_match = re.search(r'\d+$', name_without_ext)
        if num_match:
            display_num = int(num_match.group())
            display_name = f"{name_without_ext[:-len(num_match.group())]}{display_num}"
        else:
            display_name = name_without_ext
        print(f"  {i:3d}. {display_name} -> {f}")

    choice = input("\n请选择处理方式 (1/2/3/4，直接回车默认 1): ").strip()

    if choice == "" or choice == "1":
        return video_files

    if choice == "2":
        pattern = input("请输入通配符模式（如: 慰[1-20] 或 慰[1-20,25-88]）: ").strip()
        matched = parse_pattern(pattern, video_files)
        if matched:
            print(f"\n匹配到 {len(matched)} 个视频：")
            for f in matched:
                print(f"  - {f}")
            return matched
        else:
            print("没有匹配到任何视频，将处理所有视频")
            return video_files

    if choice == "3":
        nums = input("请输入视频编号（用逗号或空格分隔，如: 1,3,5 或 1 3 5）: ").strip()
        indices = re.split(r'[,\s]+', nums)
        selected = []
        for idx in indices:
            try:
                i = int(idx) - 1
                if 0 <= i < len(video_files):
                    selected.append(video_files[i])
                else:
                    print(f"警告: 编号 {idx} 超出范围")
            except ValueError:
                print(f"警告: 忽略无效编号 '{idx}'")
        return selected if selected else video_files

    if choice == "4":
        range_input = input("请输入范围（如: 1-5）: ").strip()
        try:
            parts = range_input.split('-')
            start = int(parts[0]) - 1
            end = int(parts[1])
            if start < 0:
                start = 0
            if end > len(video_files):
                end = len(video_files)
            return video_files[start:end]
        except:
            print("输入无效，将处理所有视频")
            return video_files

    return video_files


def mode_trim_start():
    """模式1：裁剪片头指定秒数"""
    print("\n" + "=" * 60)
    print("模式1：裁剪片头")
    print("=" * 60)

    trim_seconds = input("\n请输入要裁剪的片头秒数（例如: 20）: ").strip()
    try:
        trim_seconds = float(trim_seconds)
    except ValueError:
        print("输入无效，请使用数字")
        return None, None

    print(f"\n将裁剪每个视频的前 {trim_seconds} 秒")
    print("提示：如果裁剪时长 ≤ 5秒，将使用精确模式（重新编码）")
    print("      如果裁剪时长 > 5秒，将使用快速模式（直接复制）")

    return trim_seconds, None


def mode_trim_specific():
    """模式2：在指定时间点裁剪指定秒数"""
    print("\n" + "=" * 60)
    print("模式2：在指定时间点裁剪")
    print("=" * 60)
    print("\n支持的时间格式：")
    print("  - 秒数: 120")
    print("  - 分:秒: 2:30")
    print("  - 时:分:秒: 1:30:45")
    print("  - 带单位: 1h30m45s")
    print("-" * 60)

    while True:
        start_input = input("\n请输入裁剪开始时间: ").strip()
        try:
            start_time = parse_time_input(start_input)
            break
        except ValueError as e:
            print(f"错误: {e}，请重新输入")

    while True:
        duration_input = input("请输入要裁剪的时长（秒数）: ").strip()
        try:
            duration = float(duration_input)
            if duration <= 0:
                print("时长必须大于0")
                continue
            break
        except ValueError:
            print("输入无效，请使用数字")

    end_time = start_time + duration
    print(f"\n将在 {start_time:.1f}s 处裁剪 {duration:.1f}s，结束于 {end_time:.1f}s")
    print(f"提示：裁剪时长 {duration:.1f}s")
    if duration <= 5:
        print("      将使用精确模式（重新编码），保证精确到帧")
    else:
        print("      将使用快速模式（直接复制）")

    return start_time, end_time


def get_folder_path():
    while True:
        folder_input = input("\n请输入文件夹路径: ").strip()

        if folder_input == "":
            folder_input = "."

        folder_input = folder_input.strip('"').strip("'")

        if os.path.exists(folder_input):
            return folder_input
        else:
            print(f"错误：路径 '{folder_input}' 不存在，请重新输入")
            print(f"当前工作目录: {os.getcwd()}")


# ========== 主程序 ==========
if __name__ == "__main__":
    # 检查 FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误：未找到 FFmpeg！")
        print("请先安装 FFmpeg：https://ffmpeg.org/download.html")
        exit(1)

    # 获取文件夹
    video_folder = get_folder_path()
    print(f"\n目标文件夹: {video_folder}")

    # 获取视频列表
    video_files = [
        f for f in os.listdir(video_folder)
        if f.lower().endswith(video_extensions)
    ]

    if not video_files:
        print(f"\n在 '{video_folder}' 中没有找到视频文件")
        print(f"支持的格式: {', '.join(video_extensions)}")
        exit(0)

    # 选择处理模式
    print("\n" + "=" * 60)
    print("请选择裁剪模式：")
    print("=" * 60)
    print("  1. 裁剪片头指定秒数（如：前20秒）")
    print("  2. 在指定时间点裁剪指定秒数（如：从 2分30秒 处裁剪 15秒）")
    print("-" * 60)

    while True:
        mode_choice = input("\n请输入选项 (1 或 2): ").strip()
        if mode_choice == "1":
            start_time, end_time = mode_trim_start()
            if start_time is None:
                exit(0)
            break
        elif mode_choice == "2":
            start_time, end_time = mode_trim_specific()
            break
        else:
            print("无效选项，请输入 1 或 2")

    # 选择要处理的视频
    selected_videos = select_videos(video_folder, video_files)

    if not selected_videos:
        print("没有选择任何视频，退出")
        exit(0)

    print(f"\n将处理 {len(selected_videos)} 个视频")
    print(f"临时文件目录: {os.path.join(video_folder, 'temp')}")
    print("=" * 60)

    # 确认
    confirm = input("\n是否继续处理？(y/n，直接回车默认 y): ").strip().lower()
    if confirm and confirm != 'y':
        print("已取消操作")
        exit(0)

    # 处理
    temp_folder = os.path.join(video_folder, "temp")
    print("\n开始处理...\n")

    processed_count = 0
    for filename in selected_videos:
        file_path = os.path.join(video_folder, filename)
        if trim_video_ffmpeg(file_path, temp_folder, start_time, end_time):
            processed_count += 1

    # 清理 temp 文件夹
    try:
        os.rmdir(temp_folder)
        print(f"\n已删除临时文件夹: {temp_folder}")
    except OSError:
        pass

    print("=" * 60)
    print(f"处理完成！已裁剪: {processed_count} 个，跳过: {len(selected_videos) - processed_count} 个")
    print("=" * 60)