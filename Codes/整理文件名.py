import os

def rename_files_without_colon_prefix():
    # 指定要遍历的文件夹路径，这里替换成你实际要操作的文件夹路径
    folder_path = r"F:\ROMS"  # 替换为你的文件夹路径

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 构造完整的文件路径
        try:
            file_path = os.path.join(folder_path, filename)
            # 如果是文件，而非文件夹
            if os.path.isfile(file_path):
                # 查找文件名中第一个“：”的位置
                colon_index = filename.find("：")
                if colon_index != -1:
                    # 删除“：”前的内容，保留“：”后的部分
                    new_filename = filename[colon_index + 1:]
                    # 构造新的文件路径
                    new_file_path = os.path.join(folder_path, new_filename)
                    # 重命名文件
                    os.rename(file_path, new_file_path)
                    print(f"Renamed: {filename} to {new_filename}")
                else:
                    print(f"No colon found in filename: {filename}")
        except Exception as e:
            print(f"Error renaming file: {filename}. Error: {e}")

if __name__ == "__main__":
    rename_files_without_colon_prefix()