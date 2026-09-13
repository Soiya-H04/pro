import subprocess
import re
import sys
import threading
import time


def fast_ffmpeg_download_with_progress():
    """FFmpeg加速下载方案 - 修复进度显示"""

    m3u8_url = "https://fuaf-uying.mushroomtrack.com/hls/f0_pzQBSopCVmSGOQ6rVyw/1770200765/28000/28175/28175.m3u8"
    referer = "https://jable.tv/videos/dvaj-445/"
    output = "video.mp4"

    sys.stdout.write("🚀 FFmpeg高速下载模式")
    sys.stdout.write("-" * 60)

    # 完整请求头
    headers = (
        f'Referer: {referer}\r\n'
        'User-Agent: Mozilla/5.0\r\n'
        'Accept: */*\r\n'
        'Origin: https://jable.tv'
    )

    # 关键加速参数：
    cmd = [
        'ffmpeg',
        '-headers', headers,
        '-i', m3u8_url,
        '-c', 'copy',  # 不重新编码
        '-threads', '8',  # 使用8个线程
        '-reconnect', '1',  # 自动重连
        '-reconnect_streamed', '1',  # 流式重连
        '-reconnect_delay_max', '5',  # 最大重连延迟
        '-rw_timeout', '5000000',  # 读写超时5秒
        '-timeout', '30000000',  # 总超时30秒
        '-max_muxing_queue_size', '9999',  # 增加混合队列大小
        '-stats',  # 显示统计信息
        '-loglevel', 'info',  # 信息级别
        '-y',  # 覆盖输出
        output
    ]

    sys.stdout.write(f"使用 8 线程下载")
    sys.stdout.write("开始下载...")
    sys.stdout.write("-" * 60)

    # 记录开始时间
    start_time = time.time()

    # 启动下载进程
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # 合并stderr到stdout
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # 显示进度
    def show_progress():
        last_time = None
        last_update = time.time()

        while True:
            # 检查进程是否结束
            if process.poll() is not None:
                break

            # 显示简单进度点
            current_time = time.time()
            if current_time - last_update >= 1:  # 每秒更新一次
                elapsed = current_time - start_time
                sys.stdout.write(f'\r⏱️ 已下载: {elapsed:.0f}秒 | ')

                # 显示文件大小（如果文件已存在）
                import os
                if os.path.exists(output):
                    size = os.path.getsize(output) / 1024 / 1024
                    sys.stdout.write(f'📁 大小: {size:.1f}MB | ')
                    if elapsed > 0:
                        speed = size / elapsed
                        sys.stdout.write(f'🚀 速度: {speed:.2f}MB/s')

                sys.stdout.flush()
                last_update = current_time

            time.sleep(0.1)

    # 启动进度显示线程
    progress_thread = threading.Thread(target=show_progress)
    progress_thread.daemon = True
    progress_thread.start()

    # 同时读取输出信息（显示FFmpeg统计信息）
    def read_output():
        for line in process.stdout:
            line = line.strip()

            # 显示关键统计信息
            if 'time=' in line or 'speed=' in line or 'frame=' in line:
                # 提取时间
                time_match = re.search(r'time=(\d+:\d+:\d+\.\d+)', line)
                if time_match:
                    sys.stdout.write(f'\n📊 当前时间: {time_match.group(1)}')

                # 提取速度
                speed_match = re.search(r'speed=([\d.]+)x', line)
                if speed_match:
                    speed = float(speed_match.group(1))
                    if speed > 10:
                        sys.stdout.write(f'   🚀 速度: {speed:.1f}x')
                    else:
                        sys.stdout.write(f'   ⏩ 速度: {speed:.1f}x')

                # 提取帧数
                frame_match = re.search(r'frame=\s*(\d+)', line)
                if frame_match:
                    sys.stdout.write(f'   🎞️  帧数: {frame_match.group(1)}')

            # 显示其他重要信息
            elif 'HTTP error' in line or '403' in line or '404' in line:
                sys.stdout.write(f'\n⚠️  警告: {line}')
            elif 'Opening' in line or 'Stream mapping' in line:
                sys.stdout.write(f'\nℹ️  信息: {line}')

    # 启动输出读取线程
    output_thread = threading.Thread(target=read_output)
    output_thread.daemon = True
    output_thread.start()

    # 等待进程完成
    process.wait()

    # 计算总耗时
    end_time = time.time()
    total_time = end_time - start_time

    sys.stdout.write(f"\n{'=' * 60}")

    if process.returncode == 0:
        import os
        if os.path.exists(output):
            size_mb = os.path.getsize(output) / 1024 / 1024
            speed_mb_s = size_mb / total_time if total_time > 0 else 0

            sys.stdout.write(f"✅ 下载完成!")
            sys.stdout.write(f"📁 文件: {output}")
            sys.stdout.write(f"📊 大小: {size_mb:.2f} MB")
            sys.stdout.write(f"⏱️  耗时: {total_time:.1f} 秒")
            sys.stdout.write(f"🚀 平均速度: {speed_mb_s:.2f} MB/s")

            # 显示视频时长
            try:
                duration_cmd = [
                    'ffprobe',
                    '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=nosys.stdout.write_wrappers=1:nokey=1',
                    output
                ]
                result = subprocess.run(duration_cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    duration = float(result.stdout.strip())
                    minutes = int(duration // 60)
                    seconds = int(duration % 60)
                    sys.stdout.write(f"🎬 视频时长: {minutes}分{seconds}秒")
            except:
                pass
        else:
            sys.stdout.write(f"❌ 下载完成但文件不存在")
    else:
        sys.stdout.write(f"❌ 下载失败 (错误码: {process.returncode})")

        # 显示错误信息
        try:
            error_output = process.stdout.read()
            if error_output:
                sys.stdout.write("\n错误详情:")
                sys.stdout.write(error_output[-500:])  # 显示最后500字符
        except:
            pass

# 运行
fast_ffmpeg_download_with_progress()