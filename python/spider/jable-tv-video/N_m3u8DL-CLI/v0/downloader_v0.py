"""
Name: downloader
version: v0

- 使用 txt 进行 url 记录与下载
- 使用 config.json 进行下载配置
- 多任务同步下载


Describe：
粗糙版本，主要用于初步技术探索与可行性研究

"""

from import_modules import *

class DownLoader:
    # 更新输出内容
    def stdout_write(self, message, row=None):
        if row:
            sys.stdout.write(f"\033[{row}H\033[K")
            sys.stdout.write(f"{message}")
        else:
            sys.stdout.write(f"{message}")
        sys.stdout.flush()

    # 命令行清屏
    def clean_cmd(self):
        os.system("cls")

    # 初始化
    def __init__(self):
        self.clean_cmd()
        self.stdout_write(message="正在读取配置文件...", row=1)
        self.config = self.load_config()

        if self.config:
            self.stdout_write(message="\t成功")
            self.stdout_write(message="正在读取视频 url 文件...", row=2)
            self.video_url = self.get_video_url()
            if self.video_url:
                self.video_details = self.get_video_details()
            else:
                self.stdout_write(message="\t失败")
        else:
            self.stdout_write(message="\t失败")

    # 读取配置文件
    def load_config(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            return {}

    # 读取视频网页的 url 的 txt 文件
    def get_video_url(self):
        if os.path.exists(self.config["video_url_path"]):
            with open(self.config["video_url_path"], "r", encoding='utf-8') as file:
                video_url = [line.strip() for line in file if line.strip()]
            self.stdout_write("\t成功")
        else:
            self.stdout_write("\t无视频 url 文件，已创建！")
            video_url = []
            with open(self.config["video_url_path"], "w", encoding='utf-8') as file:
                pass

        self.stdout_write(message="正在读取已缓存视频 url 文件...", row=3)
        if os.path.exists(self.config["crawled_video_url_path"]):
            with open(self.config["crawled_video_url_path"], "r") as file:
                crawled_video_url = set(line.strip() for line in file if line.strip())
            self.stdout_write("\t成功")
        else:
            self.stdout_write("\t无已缓存视频 url 文件，已创建！", row=3)
            crawled_video_url = set()
            with open(self.config["crawled_video_url_path"], "w", encoding='utf-8') as file:
                pass

        video_url = [url for url in video_url if url not in crawled_video_url]

        with open(self.config["video_url_path"], "w") as file:
            for url in video_url:
                file.write(f"{url}\n")

        self.stdout_write(f"找到 {len(video_url)} 个待下载视频", row=4)
        return video_url

    def get_video_details(self):
        self.stdout_write("开始解析视频信息...", row=5)
        video_details = []
        if not self.video_url:
            return video_details

        for i, url in enumerate(self.video_url, 1):
            try:
                response = requests.get(url=url, headers=self.config["headers"], timeout=10)
                respon = response.content

                soup = BeautifulSoup(respon, 'html.parser')
                title = soup.find('title').text.split(' - J')[0]
                illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
                title = re.sub(illegal_chars, '_', title)
                title = title.strip('. ')
                if len(title) > 200:
                    title = title[200:]

                tree = html.fromstring(respon)
                xpath = "//section[1]/script[2]"
                script_text = tree.xpath(xpath)[0].text
                m3u8_url = re.findall(r"var\s+hlsUrl\s*=\s*['\"](.*?)['\"]", script_text, re.DOTALL)[0]

                video_details.append({
                    "web_url": url,
                    "title": title,
                    "m3u8_url": m3u8_url
                })

                self.stdout_write(f"解析进度: {i}/{len(self.video_url)}", row=6)

            except Exception as e:
                self.stdout_write(f"解析失败: {url}", row=7)
                continue

        self.stdout_write("视频信息解析完成...", row=8)
        return video_details

    # 移动视频位置
    def move_video(self, title, save_dir):
        try:
            video_extensions = self.config["video_extensions"]
            video_files = []

            for root, dirs, files in os.walk(save_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        video_files.append(os.path.join(root, file))

            if not video_files:
                return False

            base_video_name = f"{title}.mp4"
            destination = os.path.join(self.config["default_save_dir"], base_video_name)

            counter = 1
            while os.path.exists(destination):
                base_video_name = f"{title}_{counter}.mp4"
                destination = os.path.join(self.config["default_save_dir"], base_video_name)
                counter += 1

            shutil.move(video_files[0], destination)

            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
            return True
        except Exception as e:
            return False

    # 下载
    def download_task(self, task, row, retry=0):
        title = task["title"]
        m3u8_url = task["m3u8_url"]
        web_url = task["web_url"]

        base_row = (row - 1) * 3 + 1

        self.stdout_write(f"[{row}] {title}", base_row)
        self.stdout_write("", base_row + 1)
        self.stdout_write("", base_row + 2)

        save_dir = os.path.join(self.config["default_save_dir"], title)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        cmd = [
            self.config["cli_path"],
            m3u8_url,
            "--saveName", title,
            "--workDir", save_dir,
            "--enableDelAfterDone",
            "--maxThreads", "32",
            "--minThreads", "16",
            "--timeOut", "30",
        ]

        if self.config["headers"]:
            headers_list = []
            for key, value in self.config["headers"].items():
                headers_list.append(f"{key}:{value}")
            headers_str = "|".join(headers_list)
            cmd.extend(["--headers", headers_str])

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='ignore',
                bufsize=1,
                universal_newlines=True
            )

            last_line = ""
            while True:
                line = process.stdout.readline().rstrip("\n")
                if line and line != last_line and not line.startswith('['):
                    self.stdout_write(f"状态: {line}", base_row + 1)
                    last_line = line

                returncode = process.poll() # noqa
                if returncode is not None:
                    break

            if returncode == 0:
                success = self.move_video(title, save_dir)
                if success:
                    self.stdout_write(f"[{row}] {title}下载完成", base_row)
                    self.del_work(web_url)
                    return True
                else:
                    self.stdout_write(f"[{row}] {title} 文件移动失败", base_row)
                    return False
            else:
                self.stdout_write(f"[{row}] {title}下载失败", base_row)
                if retry < self.config['retry_count']:
                    self.stdout_write(f"正在重试 ({retry + 1}/{self.config['retry_count']})...", base_row + 1)
                    time.sleep(0.5)
                    return self.download_task(task, row, retry + 1)
                else:
                    self.stdout_write("重试已达上限", base_row + 1)
                    return False

        except Exception as e:
            self.stdout_write(f"执行异常: {str(e)}", base_row + 1)
            return False

    # 开始下载
    def start_download(self):
        if not self.video_details:
            self.stdout_write("没有可下载的视频", row=9)
            return

        self.stdout_write("开始下载...", row=9)
        time.sleep(2)
        self.clean_cmd()

        tasks = self.video_details

        with (ThreadPoolExecutor(max_workers=self.config['max_concurrent']) as executor):
            future_to_task = {}
            for i, task in enumerate(tasks, 1):
                future = executor.submit(self.download_task, task, i)
                future_to_task[future] = task

            completed = 0
            for future in as_completed(future_to_task):
                completed += 1
                task = future_to_task[future]
                try:
                    success = future.result()
                    if not success:
                        self.stdout_write(f"任务失败: {task['title']}", row=20)
                except Exception as e:
                    self.stdout_write(f"任务异常: {task['title']} - {str(e)}", row=20)

                time.sleep(1)
                self.clean_cmd()
                self.stdout_write("下载任务完成",row=1)

    def del_work(self, web_url):
        with open(self.config['crawled_video_url_path'], "a") as file:
            file.write(f"{web_url}\n")

        if web_url in self.video_url:
            self.video_url.remove(web_url)
            with open(self.config['video_url_path'], "w") as file:
                for new_url in self.video_url:
                    file.write(f"{new_url}\n")

        for i, detail in enumerate(self.video_details):
            if detail['web_url'] == web_url:
                self.video_details.pop(i)
                break


if __name__ == '__main__':
    MyDownLoader = DownLoader()
    try:
        MyDownLoader.start_download()
    except KeyboardInterrupt:
        print("\n\n中断下载")
    except Exception as e:
        print(f"\n\n程序异常: {str(e)}")