import os

def generate_path_list(root_drive, exclude_dirs, exclude_file):
    # 创建一个列表，用于存储符合条件的文件路径
    path_list = []

    # 遍历指定盘符下的所有文件夹和文件
    for root, dirs, files in os.walk(root_drive):
        # 过滤掉要排除的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        # 获取当前目录下的一级文件（不包含子文件夹中的文件）
        for file in files:
            # 如果文件不是要排除的文件，且路径中不包含Images，则添加其完整路径到列表中，
            if file != exclude_file and "Images" not in root:
                file_path = os.path.join(root, file)
                path_list.append(file_path)

    # 将路径列表导出到 txt 文件
    output_file = "游戏列表.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for path in path_list:
            f.write(f"{path}\n")

    print(f"路径列表已导出到 {output_file}")

if __name__ == "__main__":
    # 指定要遍历的盘符（例如 C 盘）
    root_drive = "F:\\"
    # 指定要排除的目录
    exclude_dirs = ["retro", "bios"]
    # 指定要排除的文件
    exclude_file = "filelist.txt"
    # 生成路径列表
    generate_path_list(root_drive, exclude_dirs, exclude_file)