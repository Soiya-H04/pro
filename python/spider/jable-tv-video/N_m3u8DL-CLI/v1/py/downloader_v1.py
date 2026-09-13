"""
version: v.1

change:
- 改用 json 进行 video 记录与下载（但还是使用 txt 进行交互）
- 将构架文件单独存放进 build_struct.py
- 完善输出显示逻辑
- 将与类服务于类的基本函数存放进 aux_module.py
- 增加任务流

Describe：
基于 v0 改进

"""


from aux_module import *

class DownLoader:
    # 初始化
    def __init__(self, paths):
        write_out("initialize program...", move_cursor(1))
        self.config = self.load_config(paths) # noqa
        self.video = self.load_video()
        self.new_video = self.load_new_video()
        self.save_video_data()

        write_out("program has initialized", move_cursor(1))

    # 获取 config.json 文件
    @staticmethod
    def load_config(paths):
        try:
            write_out("get config.json...", move_cursor(1))

            config_path = paths[3]
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            write_out("done")
            return config
        except Exception as e: # noqa
            return {}

    # 获取 video.json 文件
    def load_video(self):
        try:
            write_out("get video.json...", move_cursor(1))

            video_path = self.config["path"]["video_path"]
            with open(video_path, "r", encoding="utf-8") as f:
                video = json.load(f)

            write_out("done")
            return video
        except Exception as e: # noqa
            return {}

    # 获取 new_video.txt 文件
    def load_new_video(self):
        try:
            write_out("get new_video.txt...", move_cursor(1))

            new_video_path = self.config["path"]["new_video_path"]
            with open(new_video_path, "r", encoding="utf-8") as f:
                new_video = [line.strip() for line in f if line.strip()]

            write_out("done")
            return new_video
        except Exception as e: # noqa
            return []

    # 将 new_video.txt 文件内的 video 添加进 video.json 的 crawl_video
    def add_video(self):
        if not self.new_video:
            write_out("not video to add.", move_cursor(1))
            write_out("please write the url in new_video.txt.", move_cursor(1))

        else:
            write_out(f"{len(self.new_video)} videos have been added.", move_cursor(1))
            self.parse_crawl_details()

    # 解析 video.txt 细节（标题、m3u8_url）
    def parse_crawl_details(self):
        try:
            headers = self.config["download"]["headers"]
            
            for i, web_url in enumerate(self.new_video, 1):
                write_out(f"parse: {i}/{len(self.new_video)}", move_cursor(1))
                illegal_chars = r'[<>:"/\\|?*\x00-\x1f.-]'

                name = re.sub(illegal_chars, "", web_url)

                response = requests.get(url=web_url, headers=headers, timeout=10).content

                soup = BeautifulSoup(response, 'html.parser')
                title = soup.find('title').text.split(' - J')[0]
                title = re.sub(illegal_chars, '_', title)
                title = title.strip('. ')
                if len(title) > 200:
                    title = title[200:]

                tree = html.fromstring(response)
                xpath = "//section[1]/script[2]"
                script_text = tree.xpath(xpath)[0].text
                m3u8_url = re.findall(r"var\s+hlsUrl\s*=\s*['\"](.*?)['\"]", script_text, re.DOTALL)[0]

                self.video["crawl_video"][name] = [title, web_url, m3u8_url]

                write_out(f"\t {title} done")

            self.new_video.clear()
            success = self.save_all_data()

            if success:
                write_out("new_video.txt updated successfully.", move_cursor(1))
            else:
                write_out("new_video.txt updated failed.", move_cursor(1))

        except Exception as e: # noqa
            write_out("videos add failed", move_cursor(1))

    # 查看 config.json
    def config_info(self):
        while True:
            write_out("base", move_cursor(1))
            write_out("path", move_cursor(1))
            write_out("download", move_cursor(1))
            write_out("exit", move_cursor(2))
            write_out("choice:",move_cursor(2))

            option = read_in()

            if option == "base":
                write_out(self.config["base"],move_cursor(5))
            elif option == "path":
                write_out(self.config["path"], move_cursor(5))
            elif option == "download":
                write_out(self.config["download"], move_cursor(5))
            elif option == "exit":
                break
            else:
                write_out("there is no such option available", move_cursor(2))

    # 查看 video.json
    def video_info(self):
        while True:
            write_out("crawl_video", move_cursor(1))
            write_out("crawled_video", move_cursor(1))
            write_out("exit", move_cursor(2))
            write_out("choice:", move_cursor(2))

            option = read_in()
            if option == "crawl_video":
                write_out(self.video["crawl_video"],move_cursor(len(self.video["crawl_video"])*2))
            elif option == "crawled_video":
                write_out(self.video["crawled_video"], move_cursor(len(self.video["crawled_video"])*2))
            elif option == "exit":
                break
            else:
                write_out("there is no such option available", move_cursor(2))

    # 查看 new_video.txt
    def new_video_info(self):
        write_out(f"{self.new_video}", move_cursor(len(self.new_video)*2))

    # 保存 video.json
    def save_video_data(self):
        try:
            video_path = self.config["path"]["video_path"]
            with open(video_path, "w", encoding="utf-8") as f:
                json.dump(self.video, f, ensure_ascii=False, indent=4) # noqa
            return True
        except Exception as e:
            write_out(f"保存视频数据失败: {str(e)}", move_cursor(1))
            return False

    # 保存 new_video.txt
    def save_new_video_data(self):
        try:
            new_video_path = self.config["path"]["new_video_path"]

            with open(new_video_path, "w", encoding="utf-8") as f:
                f.write("")

            self.new_video.clear()
            return True
        except Exception as e: # noqa
            write_out(f"new_video save failed", move_cursor(1))
            return False

    def save_all_data(self):
        video_success = self.save_video_data()
        new_video_success = self.save_new_video_data()
        return video_success and new_video_success

    # 下载任务
    def download_task(self, task, i, retry = 0):
        title  = task[0]
        video_url = task[1]
        m3u8_url = task[2]

        base_row = 3 + (i-1) * 3
        write_out(f"mission {i}--{title}", base_row)
        write_out("", base_row + 1)
        write_out("", base_row + 2)

        save_dir = os.path.join(self.config["path"]["save_folder_path"], title)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        cmd = [
            self.config["download"]["cli_path"],
            m3u8_url,
            "--saveName", title,
            "--workDir", save_dir,
            f"--{self.config["download"]["afterDownload"]}",
            "--maxThreads", f"{self.config["download"]["maxThreads"]}",
            "--minThreads", f"{self.config["download"]["minThreads"]}",
            "--timeOut", f"{self.config["download"]["timeOut"]}",
        ]

        if self.config["download"]["headers"]:
            headers_list = []
            for key, value in self.config["download"]["headers"].items():
                headers_list.append(f"{key}:{value}")
            headers_str = "|".join(headers_list)
            cmd.extend(["--headers", headers_str])

        try:
            process = subprocess.Popen(
                cmd,
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT,
                text = True,
                encoding = "utf-8",
                errors = "ignore",
                bufsize = 1,
                universal_newlines = True
            )

            last_update = time.time()
            update_interval = 0.5  # 0.5秒更新一次

            last_line = ""

            while True:
                line = process.stdout.readline().rstrip("\n")
                if line and line != last_line and not line.startswith('['):
                    current_time = time.time()
                    if current_time - last_update >= update_interval:
                        write_out(f"{line}", base_row + 1)

                        last_update = current_time
                    last_line = line


                returncode = process.poll()  # noqa
                if returncode is not None:
                    break

            if returncode == 0:
                for video, detail in self.video["crawl_video"].items():
                    if detail[0] == title:
                        self.video["crawled_video"][video] = [title, video_url, m3u8_url]
                        del self.video["crawl_video"][video]

                        self.save_video_data()

                        success = move_file(title, self.config)
                        if success:
                            write_out(f"mission {i}--{title} done.", base_row + 1)
                        else:
                            write_out(f"mission {i}--{title} move failed.", base_row + 1)
                            return False

                        break

            else:
                write_out(f"mission {i}--{title} download failed", base_row)
                if retry < self.config["download"]["retry_count"]:
                    write_out(f"retrying mission {i}--{title} {retry + 1}/{self.config['download']['retry_count']}", base_row)
                    time.sleep(2)

                    return self.download_task(task, i, retry + 1)
                else:
                    write_out(f"mission {i}--{title} retry failed.", base_row)

        except Exception as e: # noqa
            write_out("conduct failed.", base_row)
            return False

    def start_download(self):
        if not self.video["crawl_video"]:
            write_out("not video to download.", move_cursor(1))
            return False

        write_out("start download...", move_cursor(1))
        time.sleep(2)

        clean_cmd()

        total_tasks = len(self.video["crawl_video"])
        write_out(f"Total tasks: {total_tasks}", move_cursor(2))

        for i in range(total_tasks):
            write_out("", move_cursor(1))

        set_cursor(3)

        tasks = self.video["crawl_video"].values()
        max_concurrent = self.config["download"]["max_concurrent"]

        with (ThreadPoolExecutor(max_workers=max_concurrent) as executor):
            future_to_task = {}
            for i, task in enumerate(tasks, 1):
                future = executor.submit(self.download_task, task, i) # noqa
                future_to_task[future] = task

            for future in as_completed(future_to_task):
                try:
                    future.result(timeout=3600)
                except Exception as e:
                    write_out(f"Task failed with exception: {str(e)}", move_cursor(1))

        time.sleep(1)
        clean_cmd()

        if self.save_video_data():
            write_out("data save successfully.", move_cursor(1))
        else:
            write_out("data save failed.", move_cursor(1))