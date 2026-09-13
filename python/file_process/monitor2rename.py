import os
import time
import re
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileRenameHandler(FileSystemEventHandler):
    def __init__(self, target_folder, base_name, start_num, extensions=None, debug=False):
        """
        初始化文件重命名处理器

        :param target_folder: 要监控的文件夹路径
        :param base_name: 文件名基础部分（如"慰"）
        :param start_num: 起始数字
        :param extensions: 要处理的文件扩展名列表
        :param debug: 是否开启调试模式
        """
        self.target_folder = Path(target_folder)
        self.base_name = base_name
        self.current_num = start_num
        self.extensions = extensions
        self.debug = debug
        self.processing_files = set()  # 正在处理的文件路径
        self.processed_files = set()  # 已处理完成的文件路径
        self.file_tracking = {}  # 跟踪文件下载状态 {路径: {'last_size': 0, 'stable_count': 0, 'first_seen': time}}

        # 初始化时扫描现有文件，找到最大的编号
        self._init_current_num()

    def _init_current_num(self):
        """扫描文件夹，将当前编号设置为已有文件的最大编号+1"""
        max_num = self.current_num - 1
        pattern = re.compile(rf'^{re.escape(self.base_name)}(\d+)(?:\..+)?$')

        for file in self.target_folder.iterdir():
            if file.is_file():
                # 跳过临时文件
                if self._is_temp_file(file.name):
                    continue
                # 检查是否符合命名规则
                match = pattern.match(file.name)
                if match:
                    num = int(match.group(1))
                    if num > max_num:
                        max_num = num

        self.current_num = max_num + 1
        print(f"当前起始编号: {self.current_num}")

    def _is_temp_file(self, filename):
        """判断是否为临时文件"""
        # 常见的临时文件扩展名
        temp_extensions = ['.part', '.tmp', '.crdownload', '.download']
        for ext in temp_extensions:
            if filename.endswith(ext):
                return True
        return False

    def _should_process_file(self, file_path):
        """判断是否应该处理该文件"""
        file_path_str = str(file_path)
        file_name = file_path.name

        # 如果文件正在处理或已经处理过，跳过
        if file_path_str in self.processing_files:
            if self.debug:
                print(f"   ⏭️ 文件正在处理中，跳过")
            return False

        if file_path_str in self.processed_files:
            if self.debug:
                print(f"   ⏭️ 文件已处理过，跳过")
            return False

        if self.debug:
            print(f"🔍 检查文件: {file_name}")
            print(f"   是否为文件: {file_path.is_file()}")

        if not file_path.is_file():
            return False

        # 跳过临时文件
        if self._is_temp_file(file_name):
            if self.debug:
                print(f"   ⏭️ 临时文件，跳过")
            return False

        # 检查扩展名
        if self.extensions is not None:
            file_ext = file_path.suffix.lower()
            if file_ext not in self.extensions:
                if self.debug:
                    print(f"   ❌ 扩展名不匹配（只处理: {', '.join(self.extensions)}），跳过")
                return False

        if self.debug:
            print(f"   ✅ 文件将被处理")
        return True

    def _is_file_downloading(self, file_path):
        """判断文件是否正在下载（通过大小变化）"""
        file_path_str = str(file_path)

        if not file_path.exists():
            return False

        try:
            current_size = file_path.stat().st_size

            # 如果文件大小为0，可能还在创建
            if current_size == 0:
                return True

            # 检查跟踪记录
            if file_path_str in self.file_tracking:
                tracking = self.file_tracking[file_path_str]
                last_size = tracking.get('last_size', 0)

                # 如果文件大小变化，说明正在下载
                if current_size != last_size:
                    # 更新跟踪信息
                    tracking['last_size'] = current_size
                    tracking['stable_count'] = 0
                    tracking['first_seen'] = time.time()
                    return True
                else:
                    # 大小稳定，增加稳定计数
                    tracking['stable_count'] = tracking.get('stable_count', 0) + 1
                    # 需要连续稳定3次（每次检查间隔1秒）才认为下载完成
                    if tracking['stable_count'] >= 3:
                        return False
                    else:
                        return True
            else:
                # 首次看到这个文件，记录初始状态
                self.file_tracking[file_path_str] = {
                    'last_size': current_size,
                    'stable_count': 0,
                    'first_seen': time.time()
                }
                return True

        except Exception as e:
            if self.debug:
                print(f"   ⚠️ 检查文件大小时出错: {e}")
            return True  # 保守处理，认为还在下载

    def on_created(self, event):
        """当文件被创建时触发"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        file_name = file_path.name

        # 如果是临时文件，忽略
        if self._is_temp_file(file_name):
            if self.debug:
                print(f"\n📂 检测到临时文件创建: {file_name} (忽略)")
            return

        # 如果是目标视频文件
        if self.debug:
            print(f"\n📂 检测到文件创建: {file_name}")

        # 检查是否应该处理
        if not self._should_process_file(file_path):
            return

        # 标记为正在处理
        file_path_str = str(file_path)
        self.processing_files.add(file_path_str)

        # 异步处理下载完成
        self._process_download_complete(file_path)

    def on_modified(self, event):
        """当文件被修改时触发 - 用于检测下载进度"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        file_name = file_path.name

        # 如果是临时文件，忽略
        if self._is_temp_file(file_name):
            return

        # 如果是目标视频文件
        if self.extensions is not None:
            file_ext = file_path.suffix.lower()
            if file_ext not in self.extensions:
                return

        if self.debug:
            print(f"\n📂 检测到文件修改: {file_name}")

        # 检查是否应该处理
        if not self._should_process_file(file_path):
            return

        # 检查是否下载完成
        if not self._is_file_downloading(file_path):
            # 下载完成，可以重命名
            file_path_str = str(file_path)
            if file_path_str not in self.processing_files:
                self.processing_files.add(file_path_str)
                self._rename_file(file_path)
                self.processing_files.discard(file_path_str)

    def on_moved(self, event):
        """当文件被移动/重命名时触发 - 处理下载完成后的重命名"""
        if event.is_directory:
            return

        src_path = Path(event.src_path)
        dest_path = Path(event.dest_path)
        src_name = src_path.name
        dest_name = dest_path.name

        # 如果是从临时文件变为目标文件
        if self._is_temp_file(src_name) and not self._is_temp_file(dest_name):
            if self.debug:
                print(f"\n📂 检测到文件完成: {src_name} -> {dest_name}")

            # 检查目标文件是否应该处理
            if self._should_process_file(dest_path):
                file_path_str = str(dest_path)
                self.processing_files.add(file_path_str)

                # 延迟一下，确保文件完全写入
                time.sleep(1)
                self._rename_file(dest_path)
                self.processing_files.discard(file_path_str)

    def _process_download_complete(self, file_path):
        """处理下载完成的文件"""
        try:
            # 等待下载完成
            wait_count = 0
            max_wait = 30  # 最多等待30秒

            while wait_count < max_wait:
                if self._is_file_downloading(file_path):
                    if self.debug:
                        print(f"   ⏳ 文件正在下载中... (等待 {wait_count + 1}s)")
                    time.sleep(1)
                    wait_count += 1
                else:
                    # 下载完成
                    if self.debug:
                        print(f"   ✅ 文件下载完成")
                    break

            # 如果超时，仍然尝试处理
            if wait_count >= max_wait and self.debug:
                print(f"   ⚠️ 等待超时，尝试处理文件")

            # 再次检查文件是否应该被处理
            if self._should_process_file(file_path):
                self._rename_file(file_path)

        finally:
            # 从正在处理列表中移除
            self.processing_files.discard(str(file_path))

    def _rename_file(self, file_path):
        """重命名文件"""
        # 再次检查文件是否存在
        if not file_path.exists():
            if self.debug:
                print(f"   ❌ 文件已不存在")
            return

        # 再次确认文件下载完成
        time.sleep(0.5)

        try:
            # 获取文件大小，确保不是0
            file_size = file_path.stat().st_size
            if file_size == 0:
                if self.debug:
                    print(f"   ⚠️ 文件大小为0，可能还未完成")
                # 等待一下再尝试
                time.sleep(1)
                if file_path.stat().st_size == 0:
                    if self.debug:
                        print(f"   ❌ 文件大小为0，放弃处理")
                    return
        except Exception as e:
            if self.debug:
                print(f"   ⚠️ 检查文件大小时出错: {e}")

        # 获取文件扩展名
        suffix = file_path.suffix

        # 构建新文件名
        new_name = f"{self.base_name}{self.current_num}{suffix}"
        new_path = self.target_folder / new_name

        # 如果目标文件已存在，增加编号直到不冲突
        while new_path.exists():
            if self.debug:
                print(f"   ⚠️ 目标文件已存在: {new_name}，尝试下一个编号")
            self.current_num += 1
            new_name = f"{self.base_name}{self.current_num}{suffix}"
            new_path = self.target_folder / new_name

        try:
            # 再次等待确保文件可操作
            time.sleep(0.3)
            file_path.rename(new_path)
            print(f"✅ 重命名: {file_path.name} -> {new_name} (大小: {file_size} bytes)")

            # 记录已处理的文件
            self.processed_files.add(str(new_path))
            self.current_num += 1

            # 清理跟踪记录
            file_path_str = str(file_path)
            if file_path_str in self.file_tracking:
                del self.file_tracking[file_path_str]

        except Exception as e:
            print(f"❌ 重命名失败: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()


def get_user_input():
    """获取用户输入的配置信息"""
    print("=" * 60)
    print("文件自动重命名监控程序 (支持浏览器下载)")
    print("=" * 60)

    # 获取文件夹路径
    while True:
        folder_input = input("\n请输入要监控的文件夹路径（支持拖拽或直接输入）: ").strip()
        folder_input = folder_input.strip('"').strip("'")

        if not folder_input:
            print("❌ 文件夹路径不能为空！")
            continue

        folder_path = Path(folder_input)
        if not folder_path.exists():
            print(f"❌ 文件夹不存在: {folder_input}")
            continue

        if not folder_path.is_dir():
            print(f"❌ 路径不是文件夹: {folder_input}")
            continue

        break

    # 获取文件名基础部分
    while True:
        base_name = input("\n请输入文件名基础文字（如：慰、视频、下载等）: ").strip()
        if not base_name:
            print("❌ 文件名基础文字不能为空！")
            continue
        break

    # 获取起始数字
    while True:
        start_input = input("\n请输入起始数字（默认为1）: ").strip()
        if not start_input:
            start_num = 1
            break
        try:
            start_num = int(start_input)
            if start_num < 0:
                print("❌ 数字不能为负数！")
                continue
            break
        except ValueError:
            print("❌ 请输入有效的数字！")

    # 获取文件扩展名（默认为.mp4）
    print("\n请输入要处理的文件扩展名（多个扩展名用逗号分隔，如：.mp4,.avi,.mkv）")
    print("直接按回车则默认处理 .mp4 文件")
    ext_input = input("扩展名（默认.mp4）: ").strip()

    if ext_input:
        extensions = []
        for ext in ext_input.split(','):
            ext = ext.strip()
            if ext:
                if not ext.startswith('.'):
                    ext = '.' + ext
                extensions.append(ext.lower())
        print(f"将只处理以下扩展名的文件: {', '.join(extensions)}")
    else:
        extensions = ['.mp4']  # 默认只处理MP4
        print("将只处理 .mp4 文件")

    # 是否开启调试
    debug_input = input("\n是否开启调试模式？(y/n，直接回车默认n): ").strip().lower()
    debug = debug_input == 'y'

    # 显示配置信息
    print("\n" + "=" * 60)
    print("📋 配置信息确认:")
    print(f"  监控文件夹: {folder_path}")
    print(f"  文件名格式: {base_name}[数字]")
    print(f"  起始数字: {start_num}")
    print(f"  处理扩展名: {', '.join(extensions)}")
    print(f"  调试模式: {'开启' if debug else '关闭'}")
    print("=" * 60)

    confirm = input("\n确认以上配置？(y/n，直接回车默认y): ").strip().lower()
    if confirm and confirm != 'y':
        print("已取消配置")
        return None

    return folder_path, base_name, start_num, extensions, debug


def monitor_folder(folder_path, base_name, start_num, extensions=None, debug=False):
    """监控文件夹并自动重命名新增文件"""
    folder = Path(folder_path)

    # 创建事件处理器
    event_handler = FileRenameHandler(folder_path, base_name, start_num, extensions, debug)

    # 创建观察者
    observer = Observer()
    observer.schedule(event_handler, str(folder), recursive=False)
    observer.start()

    print("\n" + "=" * 60)
    print("✅ 监控已启动！")
    print(f"📁 监控文件夹: {folder_path}")
    print(f"📝 文件命名格式: {base_name}[数字]")
    print(f"🔢 当前编号从: {event_handler.current_num} 开始")
    if extensions:
        print(f"📄 只处理扩展名: {', '.join(extensions)}")
    print("=" * 60)
    print("💡 提示:")
    print("   - 自动识别浏览器下载的临时文件 (.part, .tmp 等)")
    print("   - 监控目标文件的大小变化，等待下载完成")
    print("   - 下载完成后自动重命名")
    print("   - 不管原文件名是什么，都会按照规则重新编号")
    print("按 Ctrl+C 停止监控...\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n" + "=" * 60)
        print("🛑 监控已停止")
        print("=" * 60)

    observer.join()


def main():
    """主函数"""
    try:
        config = get_user_input()
        if config is None:
            return

        folder_path, base_name, start_num, extensions, debug = config

        monitor_folder(folder_path, base_name, start_num, extensions, debug)

    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")


if __name__ == "__main__":
    main()