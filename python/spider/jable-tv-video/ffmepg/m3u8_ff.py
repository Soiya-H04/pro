import subprocess
import sys
import threading
import time
import os
import Video_details


def ffmpeg_download():
    details = Video_details.read_url("URLs.txt")

    if not details:
        print("没有找到视频信息")
        return

    print(f"找到 {len(details)} 个视频")
    print("=" * 50)

    os.makedirs("videos", exist_ok=True)

    for i, (title, info) in enumerate(details.items(), 1):
        print(f"\n[{i}/{len(details)}] {title[:60]}...")  # 限制标题长度
        print("-" * 40)

        m3u8_url = info["m3u8_url"]
        referer = info["web_url"]

        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
        output = os.path.join("videos", clean_title + ".mp4")

        if os.path.exists(output):
            size = os.path.getsize(output) / 1024 / 1024
            print(f"文件已存在: {size:.1f}MB")
            continue

        headers = f'Referer: {referer}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\nOrigin: https://jable.tv'

        print(f"URL: {m3u8_url[:80]}..." if len(m3u8_url) > 80 else f"URL: {m3u8_url}")

        if not test_m3u8_access(m3u8_url, referer):
            print("m3u8链接无法访问，跳过")
            continue

        cmd = [
            'ffmpeg',
            '-headers', headers,
            '-i', m3u8_url,
            '-c', 'copy',
            '-threads', '8',
            '-reconnect', '1',
            '-reconnect_delay_max', '2',
            '-timeout', '30000000',
            '-max_muxing_queue_size', '1024',
            '-loglevel', 'warning',  # 改为warning级别
            '-y',
            output
        ]

        # 启动下载进程
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        except Exception as e:
            print(f"无法启动FFmpeg: {e}")
            continue

        stop_event = threading.Event()
        start_time = time.time()

        def show_progress():
            last_update = time.time()

            while not stop_event.is_set():
                current_time = time.time()

                if int(current_time - last_update) >= 1:
                    elapsed = current_time - start_time
                    sys.stdout.write(f'\rtime: {elapsed:.0f}s | ')
                    if os.path.exists(output):
                        size = os.path.getsize(output) / 1024 / 1024
                        sys.stdout.write(f'size: {size:.1f}MB | ')
                        if elapsed > 0:
                            speed = size / elapsed
                            sys.stdout.write(f'speed: {speed:.2f}MB/s')
                    sys.stdout.flush()
                    last_update = current_time
                time.sleep(0.5)

        # 启动进度显示线程
        progress_thread = threading.Thread(target=show_progress)
        progress_thread.daemon = True
        progress_thread.start()

        try:
            # 等待进程完成
            return_code = process.wait()

            # 通知进度线程停止
            stop_event.set()
            progress_thread.join(timeout=1)

            # 检查结果
            if return_code == 0:
                if os.path.exists(output):
                    size_mb = os.path.getsize(output) / 1024 / 1024
                    total_time = time.time() - start_time

                    # 清除进度行，显示完成信息
                    sys.stdout.write('\r\033[K')
                    print(f"下载完成! | 大小: {size_mb:.2f} MB | 耗时: {total_time:.1f}s")
                else:
                    sys.stdout.write('\r\033[K')
                    print(f"下载完成但文件不存在")
            else:
                sys.stdout.write('\r\033[K')
                print(f"下载失败 (错误码: {return_code})")

                # 读取并显示错误信息
                try:
                    output_lines = []
                    for line in process.stdout:
                        line = line.strip()
                        if line:
                            output_lines.append(line)

                    if output_lines:
                        print("错误详情:")
                        for line in output_lines[-5:]:  # 显示最后5行
                            if len(line) > 200:
                                print(f"  {line[:200]}...")
                            else:
                                print(f"  {line}")
                except:
                    pass

        except KeyboardInterrupt:
            sys.stdout.write('\r\033[K')
            print(f"\n用户中断")
            process.terminate()
            stop_event.set()
            break

        except Exception as e:
            sys.stdout.write('\r\033[K')
            print(f"下载出错: {e}")
            process.terminate()
            stop_event.set()

        finally:
            # 确保进程被终止
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except:
                    pass

        # 两个视频之间添加间隔
        if i < len(details):
            time.sleep(2)  # 增加间隔时间

    print("\n" + "=" * 50)
    print("批量下载完成！")


def test_m3u8_access(m3u8_url, referer):
    try:
        import requests

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': referer,
            'Accept': '*/*',
        }

        # 发送HEAD请求测试
        response = requests.head(m3u8_url, headers=headers, timeout=5)

        if response.status_code == 200:
            return True
        else:
            print(f"  HTTP状态码: {response.status_code}")
            return False

    except Exception as e:
        print(f"  链接测试失败: {e}")
        return False


# 运行
if __name__ == '__main__':
    ffmpeg_download()