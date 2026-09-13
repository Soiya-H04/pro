"""

构建完整的项目结构

"""

from aux_module import *

# 创建
def create_all():
    py_folder_path = os.path.dirname(__file__)

    pro_folder_path = os.path.dirname(py_folder_path)

    refer_folder_path = os.path.join(pro_folder_path, "refer")
    if not exist_folder(refer_folder_path):
        create_folder(refer_folder_path)

    save_folder_path = os.path.join(pro_folder_path, "video")
    if not exist_folder(save_folder_path):
        create_folder(save_folder_path)

    video_path = os.path.join(refer_folder_path, "video.json")
    if not exist_file(video_path):
        create_file(video_path)
        build_url(video_path)

    new_video_path = os.path.join(refer_folder_path, "new_video.txt")
    if not exist_file(new_video_path):
        create_file(new_video_path)

    config_path = os.path.join(refer_folder_path, "config.json")
    paths = [pro_folder_path, py_folder_path, refer_folder_path, config_path, video_path, new_video_path, save_folder_path] # noqa
    if not exist_file(config_path):
        create_file(config_path)
        build_config(paths)
    return paths

def build_url(video_path):
    video_data = {
        "crawl_video":{

        },
        "crawled_video":{

        }
    }
    with open(video_path,"w", encoding="utf-8") as f:
        json.dump(video_data, f, ensure_ascii=False, indent=4)  # noqa

def build_config(paths): # noqa
    pro_folder_path, py_folder_path, refer_folder_path, config_path, video_path, new_video_path, save_folder_path = paths
    config_data = {
            "base": {
                "name":"m3u8_downloader",
                "version": "v1",
                "encoding": "utf-8"
            },

            "path": {
                "pro_folder_path": f"{pro_folder_path}",
                "py_folder_path": f"{py_folder_path}",
                "refer_folder_path": f"{refer_folder_path}",
                "video_path": f"{video_path}",
                "config_path": f"{config_path}",
                "new_video_path": f"{new_video_path}",
                "save_folder_path": f"{save_folder_path}"
            },

            "download": {
                "cli_path": "D:/Download/N_m3u8DL-CLI/N_m3u8DL-CLI_v3.0.2.exe",
                "retry_count": 3,
                "max_concurrent": 5,
                "maxThreads": 32,
                "minThreads": 16,
                "timeOut": 30,
                "afterDownload": "enableDelAfterDone",
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
                    "Referer": "https://jable.tv/"
                },
                "video_extensions": [
                    ".mp4",
                    ".mkv",
                    ".avi",
                    ".mov",
                    ".wmv",
                    ".flv",
                    ".ts",
                    ".m3u8"
                ]
            }
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)  # noqa