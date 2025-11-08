import os
import zlib
import shutil

def get_file_crc32(file_path, chunk_size=65536):
    """计算文件的 CRC32 校验值"""
    crc_value = 0
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            crc_value = zlib.crc32(chunk, crc_value)
    return format(crc_value & 0xFFFFFFFF, '08x')

def scan_folder(folder_path):
    """遍历文件夹，返回文件字典（文件名: 文件路径）"""
    file_dict = {}
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_dict[file_name] = file_path
    return file_dict

def replace_files_if_different(a_folder, b_folder):
    """
    遍历 B 文件夹中的所有文件，如果 A 文件夹中有同名文件且 CRC32 不同，
    则删除 B 文件夹中的文件并用 A 文件夹中的文件替换
    """
    # 获取 A 和 B 文件夹的文件字典
    a_files = scan_folder(a_folder)
    b_files = scan_folder(b_folder)
    
    replaced_files = 0
    skipped_files = 0
    
    # 遍历 B 文件夹中的每个文件
    for file_name, b_file_path in b_files.items():
        # 检查 A 文件夹中是否有同名文件
        if file_name in a_files:
            a_file_path = a_files[file_name]
            
            # 计算两个文件的 CRC32 校验值
            a_crc = get_file_crc32(a_file_path)
            b_crc = get_file_crc32(b_file_path)
            
            print(f"比较文件: {file_name}")
            print(f"A 文件路径: {a_file_path} (CRC32: {a_crc})")
            print(f"B 文件路径: {b_file_path} (CRC32: {b_crc})")
            
            # 如果 CRC32 值不同，则替换 B 中的文件
            if a_crc != b_crc:
                print(f"文件 {file_name} 的 CRC32 值不同，将用 A 中的文件替换 B 中的文件")
                
                # 先删除 B 中的文件
                os.remove(b_file_path)
                print(f"已删除文件: {b_file_path}")
                
                # 用 A 中的文件替换 B 中的文件
                shutil.copy2(a_file_path, b_file_path)
                print(f"已复制文件: {a_file_path} -> {b_file_path}\n")
                replaced_files += 1
            else:
                # CRC32 相同，跳过
                print(f"文件 {file_name} 的 CRC32 值相同，无需替换\n")
                skipped_files += 1
        else:
            # A 中没有同名文件，跳过
            print(f"B 中的文件 {file_name} 在 A 中没有找到同名文件，跳过\n")
            skipped_files += 1
    
    # 输出统计信息
    print(f"处理完成！")
    print(f"共替换 {replaced_files} 个文件")
    print(f"共跳过 {skipped_files} 个文件")

if __name__ == "__main__":
    # 设置文件夹路径
    # a_folder = input("请输入原始文件夹(A)的路径: ")
    # b_folder = input("请输入被替换文件夹(B)的路径: ")
    
    a_folder = r"E:\WBFS"
    b_folder = r"J:\wbfs"
    
    # 检查文件夹是否存在
    if not os.path.exists(a_folder):
        print(f"错误: 原始文件夹 {a_folder} 不存在")
        exit(1)
    
    if not os.path.exists(b_folder):
        print(f"错误: 被替换文件夹 {b_folder} 不存在")
        exit(1)
    
    # 执行文件替换操作
    replace_files_if_different(a_folder, b_folder)