# 使用 N_m3u8DL-CLI 下载 https://jable.tv 网站视频

## 一、N_m3u8DL-CLI 直接下载

### usage

在 cmd 中运行

```bash
N_m3u8DL-CLI "m3u8_url" --workDir "保存目录" --saveName "视频名称"
```

>   m3u8_url：视频的 m3u8 地址
>
>   workDir：保存视频的文件夹
>
>   saveName：视频名（不含拓展，为 mp4 格式）

### 结果

-   速度快
-   需要手动抓包找到视频的 m3u8 地址
-   一次下载一个视频

## 二、Python + N_m3u8DL-CLI 下载：

### usage

切换到 spider 环境

```bash
conda activate spider
```

>   不同环境操作不一样（只要环境包含所要用的库即可）

切换到 py 文件所在目录

```bash
cd "文件目录"
```

在video_urls.txt 中每行输入想要下载视频的网页地址

```txt
# video_urls.txt
视频网址1
视频网址2
...
```

在终端运行

```bash
python downloader.py
```

### 情况

速度很快，不用手动抓包，下载视频存放在一起，但同时下载多个视频速度会降，相关配置需要调整 config.json
config 中相关参数：
cli_path：N_m3u8DL-CLI 的 exe 文件位置
video_url_path：需要下载视频的网址
crawled_video_url_path：已下载视频的网址
default_save_dir：默认存储视频的地址
retry_count：可重试次数
max_concurrent：可同时下载视频数
headers：下载配置参数