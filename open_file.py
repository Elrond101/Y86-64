import subprocess
import platform
import os
def open_file(file_path):
    """
    跨平台打开文件
    会根据操作系统使用相应的命令
    """
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return

    system = platform.system()

    try:
        if system == "Windows":
            os.startfile(file_path)  # 或者使用 subprocess.run(['start', file_path], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.run(['open', file_path])
        else:  # Linux 和其他Unix-like系统
            subprocess.run(['xdg-open', file_path])
    except Exception as e:
        print(f"打开文件时出错: {e}")