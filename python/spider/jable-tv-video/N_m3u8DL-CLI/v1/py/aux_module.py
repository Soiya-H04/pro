# 导入库
import json # noqa
import os # noqa
import time # noqa
import requests # noqa
from bs4 import BeautifulSoup # noqa
import subprocess # noqa
import sys # noqa
from concurrent.futures import ThreadPoolExecutor, as_completed # noqa
from lxml import html # noqa
import shutil # noqa
import re # noqa

cursor = 1

# functions
# 1. CLI
# output
def write_out(message: str = "", row: int = None):
    if row:
        sys.stdout.write(f"\033[{row}H\033[K")
        sys.stdout.write(f"{message}")
    else:
        sys.stdout.write(f"{message}")
    sys.stdout.flush()

# input
def read_in():
    message = sys.stdin.readline().rstrip("\n")
    return message

# cls
def clean_cmd():
    global cursor
    cursor = 1
    os.system("cls")

# 2. File/Folder
# exist
def exist_folder(folder_path):
        return os.path.isdir(folder_path) if os.path.exists(folder_path) else False

def exist_file(file_path):
        return os.path.isfile(file_path) if os.path.exists(file_path) else False

# create
def create_folder(folder_path):
    os.makedirs(folder_path,exist_ok=True)

def create_file(file_path):
        with open(file_path,"w",encoding="utf-8"):pass

# move
def move_file(title, config):
    try:
        save_folder_path = config["path"]["save_folder_path"]
        video_folder_path = os.path.join(save_folder_path, title)
        video_extensions = config["download"]["video_extensions"]

        video_files = []

        for root, dirs, files in os.walk(video_folder_path): # noqa
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    video_files.append(os.path.join(root, file))

        if not video_files:
            return False

        base_video_name = f"{title}.mp4"
        destination = os.path.join(save_folder_path, base_video_name)

        counter = 1
        while exist_file(destination):
            base_video_name = f"{title}_{counter}.mp4"
            destination = os.path.join(save_folder_path, base_video_name)
            counter += 1

        shutil.move(video_files[0], destination) # noqa

        if exist_folder(video_folder_path):
            shutil.rmtree(video_folder_path)
        return True
    except Exception as e: # noqa
        return False

# delete
def del_folder(folder_path):
        shutil.rmtree(folder_path)

def del_file(file_path):
    os.remove(file_path)

# 3.cursor（好用）
def move_cursor(add_step:int):
    global cursor
    now = cursor
    cursor += add_step
    return now

def set_cursor(row:int):
    global cursor
    cursor = row
    sys.stdout.write(f"\033[{row}H")
    sys.stdout.flush()


# 4.interface
def return_count(n:int):
    if n > 0:
        while n:
            n -= 1
            time.sleep(1)
            write_out(f"return at {n} seconds.", move_cursor(0))
    else:
        return False

def choice_interface():
    write_out("options:", move_cursor(1))
    write_out("add \t check \t sdl(start download) \t exit", move_cursor(1)) # 添加 txt 文件的视频
    write_out("choice: ", move_cursor(2))
    option = read_in()
    return option

def check_interface():
    write_out("options:", move_cursor(1))
    write_out("config \t video \t new_video \t exit", move_cursor(1))
    write_out("choice: ", move_cursor(2))
    option = read_in()
    return option

def print_config(config):
    for category in config:
        for info in config[category]:
            write_out(f"{info} : \t {config[category][info]}", move_cursor(1))

def print_video(video):
    for category in video:
        write_out(f"{category}", move_cursor(1))
        if not video[category]:
            write_out("(empty)", move_cursor(1))
            move_cursor(1)
            continue

        for key, details in video[category].items():
            write_out(f"{key}", move_cursor(1))
            write_out(f"Title: {details[0]}", move_cursor(1))
            write_out(f"URL: {details[1]}", move_cursor(1))
            write_out(f"M3U8: {details[2]}",move_cursor(1))
            move_cursor(1)

def print_new_video(new_video):
    for info in new_video:
        write_out(f"{info}", move_cursor(1))
        move_cursor(1)

