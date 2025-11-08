import os
import shutil

def move_files_without_suffix():
    # 指定要遍历的路径，这里替换成你实际要遍历的文件夹路径
    source_path = r"H:"  # 替换为你的源路径
    # 桌面路径获取
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    # 目标文件夹路径（桌面的‘重复文件夹’）
    target_folder = os.path.join(desktop_path, "重复文件夹")
    # 如果目标文件夹不存在，则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    # 遍历指定路径下的所有文件
    for root, dirs, files in os.walk(source_path):
        for file in files:
            # 检查文件名是否包含后缀以“(1)”结尾的情况，这里假设后缀是指文件扩展名
            # 分离文件名和扩展名
            file_name, file_extension = os.path.splitext(file)
            # 如果文件名不包含后缀以“(1)”结尾，则移动该文件
            if file_name.endswith("(1)"):
                file_path = os.path.join(root, file)
                # 构造目标文件路径
                target_file_path = os.path.join(target_folder, file)
                # 移动文件
                shutil.move(file_path, target_file_path)
                print(f"Moved: {file_path} to {target_folder}")

if __name__ == "__main__":
    move_files_without_suffix()