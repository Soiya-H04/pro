# build_exe.py
import os
import sys
import shutil
import subprocess


# 清理之前的构建
def clean_build():
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除: {dir_name}")

    spec_file = 'AI膳食搭配系统.spec'
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"已删除: {spec_file}")


# 执行打包
def build_exe():
    print("开始打包...")

    # Anaconda 环境路径
    conda_dlls = r"D:\Download\Anaconda\envs\Py_study\DLLs"
    conda_bin = r"D:\Download\Anaconda\envs\Py_study\Library\bin"

    # 使用文件夹模式
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=AI膳食搭配系统',
        '--windowed',  # 不显示控制台
        '--noconfirm',
        '--clean',  # 清理临时文件
    ]

    # 添加数据文件
    if os.path.exists('mydb.db'):
        cmd.append('--add-data=mydb.db;.')
        print("✓ 包含数据库文件: mydb.db")

    if os.path.exists('食物数据库.xlsx'):
        cmd.append('--add-data=食物数据库.xlsx;.')
        print("✓ 包含数据文件: 食物数据库.xlsx")

    # 添加 Anaconda 的 DLL 文件
    pyexpat_path = os.path.join(conda_dlls, 'pyexpat.pyd')
    if os.path.exists(pyexpat_path):
        cmd.append(f'--add-data={pyexpat_path};.')
        print("✓ 包含 pyexpat.pyd")

    # 添加 libexpat.dll（如果存在）
    libexpat_path = os.path.join(conda_bin, 'libexpat.dll')
    if os.path.exists(libexpat_path):
        cmd.append(f'--add-data={libexpat_path};.')
        print("✓ 包含 libexpat.dll")

    # 添加 python3.dll
    python3_dll = os.path.join(conda_dlls, 'python3.dll')
    if os.path.exists(python3_dll):
        cmd.append(f'--add-data={python3_dll};.')
        print("✓ 包含 python3.dll")

    # 添加 vcruntime140.dll
    vcruntime = os.path.join(conda_dlls, 'vcruntime140.dll')
    if os.path.exists(vcruntime):
        cmd.append(f'--add-data={vcruntime};.')
        print("✓ 包含 vcruntime140.dll")

    # 隐藏导入
    hidden_imports = [
        '--hidden-import=openpyxl',
        '--hidden-import=pandas',
        '--hidden-import=sqlite3',
        '--hidden-import=openai',
        '--hidden-import=PySide6',
        '--hidden-import=xml.parsers.expat',
        '--hidden-import=pyexpat',
        '--collect-all=openpyxl',
        '--collect-all=pandas',
    ]
    cmd.extend(hidden_imports)

    # 排除不必要的模块（减小体积，避免冲突）
    excludes = [
        '--exclude-module=pandas.tests',
        '--exclude-module=pandas._testing',
        '--exclude-module=pandas.conftest',
        '--exclude-module=numpy.distutils',
        '--exclude-module=numpy.tests',
        '--exclude-module=PIL.ImageQt',
        '--exclude-module=PIL.ImageTk',
    ]
    cmd.extend(excludes)

    # 添加 Anaconda 的 DLL 路径到搜索路径
    cmd.append(f'--paths={conda_dlls}')
    cmd.append(f'--paths={conda_bin}')

    # 主文件
    cmd.append('main_guifan.py')

    print(f"\n执行命令:\n{' '.join(cmd)}\n")

    # 执行打包
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("✅ 打包成功！")
        print("=" * 50)

        # 复制额外的 DLL 到输出目录
        dist_dir = os.path.abspath('dist/AI膳食搭配系统')
        if os.path.exists(dist_dir):
            print("\n正在复制额外的 DLL 文件...")

            # 复制所有必要的 DLL 到程序目录
            dll_files = ['pyexpat.pyd', 'python3.dll', 'vcruntime140.dll', 'libexpat.dll']
            for dll in dll_files:
                src = os.path.join(conda_dlls, dll)
                if not os.path.exists(src):
                    src = os.path.join(conda_bin, dll)
                if os.path.exists(src):
                    dst = os.path.join(dist_dir, dll)
                    shutil.copy2(src, dst)
                    print(f"  ✓ 复制 {dll}")

            # 复制数据文件
            if os.path.exists('mydb.db'):
                shutil.copy2('mydb.db', dist_dir)
                print("  ✓ 复制 mydb.db")
            if os.path.exists('食物数据库.xlsx'):
                shutil.copy2('食物数据库.xlsx', dist_dir)
                print("  ✓ 复制 食物数据库.xlsx")

            exe_path = os.path.join(dist_dir, 'AI膳食搭配系统.exe')
            print(f"\n📁 程序位置: {exe_path}")

            # 创建启动脚本
            create_launcher(dist_dir)

        # 也创建单文件版本的说明
        single_exe = os.path.abspath('dist/AI膳食搭配系统.exe')
        if os.path.exists(single_exe):
            size = os.path.getsize(single_exe) / (1024 * 1024)
            print(f"\n📁 单文件版本: {single_exe}")
            print(f"📊 文件大小: {size:.2f} MB")
    else:
        print("\n" + "=" * 50)
        print("❌ 打包失败，请检查错误信息")
        print("=" * 50)


def create_launcher(dist_dir):
    """创建启动脚本"""
    launcher_content = f'''@echo off
chcp 65001 >nul
title AI膳食搭配系统
echo 正在启动 AI膳食搭配系统...
cd /d "{dist_dir}"
start AI膳食搭配系统.exe
exit
'''
    launcher_path = os.path.join(dist_dir, '启动.bat')
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    print(f"\n📄 已创建启动脚本: {launcher_path}")


if __name__ == "__main__":
    clean_build()
    build_exe()