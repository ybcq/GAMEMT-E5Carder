import os
import shutil
import argparse
from pathlib import Path

def get_file_list(directory):
    """获取指定目录下所有文件的路径列表，包括子目录中的文件"""
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 计算相对路径，方便后续操作
            relative_path = os.path.relpath(file_path, directory)
            file_list.append(relative_path)
    return file_list

def sync_directories(src_dir, dest_dir, check_content=False, verbose=False):
    """
    同步两个目录，将源目录中存在的文件（目标目录中不存在的）复制到目标目录
    保持原始目录结构
    
    参数:
    src_dir -- 源目录路径
    dest_dir -- 目标目录路径
    check_content -- 是否检查文件内容相同 (默认: False)
    verbose -- 是否显示详细操作信息 (默认: False)
    """
    # 确保源目录存在
    if not os.path.exists(src_dir):
        print(f"源目录 '{src_dir}' 不存在！")
        return
    
    # 确保目标目录存在，如果不存在则创建
    if not os.path.exists(dest_dir):
        print(f"目标目录 '{dest_dir}' 不存在，正在创建...")
        os.makedirs(dest_dir)
    
    # 获取源目录和目标目录的文件列表
    src_files = get_file_list(src_dir)
    dest_files = get_file_list(dest_dir)
    
    # 计算需要复制的文件
    files_to_copy = []
    
    for file in src_files:
        src_file_path = os.path.join(src_dir, file)
        dest_file_path = os.path.join(dest_dir, file)
        
        # 如果目标文件不存在
        if not os.path.exists(dest_file_path):
            print(f"目标文件 '{dest_file_path}' 不存在，需要复制...")
            files_to_copy.append((src_file_path, dest_file_path))
        else:
            # 如果需要检查文件内容是否相同
            if check_content:
                # 检查文件内容是否相同
                with open(src_file_path, 'rb') as f1, open(dest_file_path, 'rb') as f2:
                    if f1.read() != f2.read():
                        print(f"文件 '{dest_file_path}' 的内容不同，需要复制...")
                        files_to_copy.append((src_file_path, dest_file_path))
    
    # 复制文件
    for src_file, dest_file in files_to_copy:
        # 确保目标目录存在
        dest_dir_part = os.path.dirname(dest_file)
        if not os.path.exists(dest_dir_part):
            os.makedirs(dest_dir_part)
        
        # 复制文件
        try:
            shutil.copy2(src_file, dest_file)
            if verbose:
                print(f"已复制: {os.path.relpath(src_file, src_dir)}")
        except Exception as e:
            print(f"复制文件 {src_file} 到 {dest_file} 时出错: {e}")
    
    if verbose:
        print("\n同步完成！")
        if not files_to_copy:
            print("没有需要复制的文件。")
        else:
            print(f"共复制 {len(files_to_copy)} 个文件。")

if __name__ == "__main__":
    
    # parser = argparse.ArgumentParser(description="同步两个目录，将源目录中存在的文件复制到目标目录。")
    # parser.add_argument("src_dir", help="源目录路径")
    # parser.add_argument("dest_dir", help="目标目录路径")
    # parser.add_argument("-c", "--check-content", action="store_true",
    #                     help="检查文件内容是否相同（默认只比较文件名）")
    # parser.add_argument("-v", "--verbose", action="store_true",
    #                     help="显示详细操作信息")
    
    # args = parser.parse_args()
    
    # sync_directories(args.src_dir, args.dest_dir, args.check_content, args.verbose)
    
    
    # 原始文件路径
    src_dir = r"F:\wbfs"
    # 目标文件路径
    dest_dir = r"J:\wbfs"
    # 调用函数进行同步
    sync_directories(src_dir, dest_dir, check_content=False, verbose=True)