import PySimpleGUI as sg
import os
import shutil
import win32file

# sg.theme_previewer()
sg.theme('DarkGray')  # Add a little color to your windows
sg.set_options(font=("微软雅黑", 10))

APP_TITLE = 'E5一键开卡工具'
APP_VERSION = '1.0.0'
HOW_TO_USE = """
1.把TF卡用读卡器插在电脑上
2.点击刷新盘符，左侧选择你的TF卡的盘符
3.点击一键开卡，会卡10分钟左右，10分钟后自动弹窗显示开卡完成
4.把其他网站上下载好的游戏复制到TF卡对应的文件夹中，文件夹对应关系看软件界面
5.点击生成游戏列表
6.弹出TF卡，插入游戏机，开机即可
"""

def get_usb_drives():
    drives = []
    if os.name == 'nt':  # Windows系统
        drive_types = {
            win32file.DRIVE_REMOVABLE: '可移动磁盘',
            win32file.DRIVE_FIXED: '本地磁盘',
            win32file.DRIVE_REMOTE: '网络磁盘',
            win32file.DRIVE_CDROM: '光盘驱动器',
            win32file.DRIVE_RAMDISK: 'RAM磁盘'
        }

        for drive_letter in range(ord('A'), ord('Z')+1):
            drive = chr(drive_letter) + ':\\'
            if os.path.exists(drive):
                # 获取驱动器类型
                drive_type = win32file.GetDriveType(drive)
                if drive_type == win32file.DRIVE_REMOVABLE:
                    drives.append(drive)

    else:  # 其他系统（如Linux）
        # 在Linux系统上，通常可以通过挂载点来识别U盘，但具体实现可能更复杂
        # 这里提供一个简化的版本，实际应用中可能需要更复杂的逻辑
        pass

    return drives

# 复制文件到U盘（修改版）


def copy_to_usb(source_folder, destination_folder):
    try:
        # 检查源文件夹是否存在
        if not os.path.exists(source_folder):
            sg.popup('源文件夹不存在', '请检查路径：', source_folder, title='错误')
            return

        # 检查目标文件夹是否存在
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # 获取源文件夹中的所有文件和文件夹
        items = os.listdir(source_folder)
        total_items = len(items)
        copied_items = 0

        # 遍历所有文件和文件夹
        for item in items:
            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)

            # 如果是文件，直接复制并覆盖
            if os.path.isfile(source_path):
                # 先删除目标文件（如果存在）
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                shutil.copy2(source_path, destination_path)
            # 如果是文件夹，递归复制内容并覆盖
            elif os.path.isdir(source_path):
                # 先删除目标文件夹（如果存在）
                if os.path.exists(destination_path):
                    shutil.rmtree(destination_path)
                shutil.copytree(source_path, destination_path)

            copied_items += 1
            # 更新进度条
            window['-PROGRESS-'].update(copied_items / total_items * 100)

        sg.popup(
            '开卡完成', f"已成功复制 {copied_items} 个项目到 {destination_folder}", title='成功')

    except Exception as e:
        sg.popup('开卡失败', '错误:', str(e), title='错误')

# 生成游戏列表的函数（对应提供的JavaScript脚本逻辑）


def create_game_list(directory_path):
    try:
        # 删除旧的filelist.txt
        filelist_path = os.path.join(directory_path, 'filelist.txt')
        if os.path.exists(filelist_path):
            os.remove(filelist_path)
            print(f"原始文件删除成功: {filelist_path}")
        else:
            print(f"原始目录不存在filelist.txt，忽略")

        # 重新创建filelist.txt
        with open(filelist_path, 'w', encoding='utf-8') as f:
            pass  # 创建空文件，后续会写入数据

        files = os.listdir(directory_path)
        game_list = []

        for file in files:
            file_parts = file.split('.')
            if len(file_parts) > 1:
                file_type = file_parts[-1]
                # 过滤掉js和txt文件
                if file_type.lower() not in ['js', 'txt']:
                    file_name = file_parts[0]  # 获取文件名（不含扩展名）
                    # 如果文件名超过20字符，截取前20个字符
                    truncated_name = file_name[:20] if len(
                        file_name) > 20 else file_name
                    game_list.append(
                        f"{file};{file_name}.png;{truncated_name}")

        # 将游戏列表写入txt文件
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for item in game_list:
                f.write(f"{item}\n")

        # print(f"-------------成功为 {directory_path} 生成游戏列表，请手动关闭-------------")
        print(f"为 {directory_path} 生成游戏列表成功")
        return True

    except Exception as e:
        sg.popup(f'为目录生成游戏列表时出错：{str(e)}', title='错误')
        return False

# 实现为选中类型生成游戏列表的逻辑


def generate_game_lists_for_selected():
    selected_drive = values['-DRIVE-']
    if not selected_drive:
        sg.popup('请先选择一个TF卡', title='错误')
        return

    # 获取选中的复选框
    selected_folders = []
    if values['000-MAME']:
        selected_folders.append('000')
    if values['001-MD']:
        selected_folders.append('001')
    if values['002-SFC']:
        selected_folders.append('002')
    if values['003-FC']:
        selected_folders.append('003')
    if values['004-GBA']:
        selected_folders.append('004')
    if values['005-GBC']:
        selected_folders.append('005')
    if values['006-GB']:
        selected_folders.append('006')
    if values['007-PS']:
        selected_folders.append('007')
    if values['008-CPS1']:
        selected_folders.append('008')
    if values['009-CPS2']:
        selected_folders.append('009')
    if values['010-IGS']:
        selected_folders.append('010')
    if values['011-NEOGEO']:
        selected_folders.append('011')
    # if values['ROMS-OTHER']:
        # selected_folders.append('ROMS')

    if not selected_folders:
        sg.popup('错误', '请至少选择一个目录类型来生成游戏列表')
        return

    # 遍历选中的目录并生成游戏列表
    for folder in selected_folders:
        target_dir = os.path.join(selected_drive, folder)
        if not os.path.exists(target_dir):
            print(f"目录不存在: {target_dir}, 即将创建")
            # 　创建文件夹
            os.makedirs(target_dir, exist_ok=True)
            # 创建Images子文件夹
            os.makedirs(os.path.join(target_dir, 'Images'), exist_ok=True)

        create_game_list(target_dir)

    sg.popup('已为选中的目录生成游戏列表', title='成功')


# 初始化界面布局
layout = [
    [sg.Frame('第一步：选择TF卡', [
        [sg.Combo(get_usb_drives(), key='-DRIVE-', size=(15, 1), enable_events=True, readonly=True, default_value=get_usb_drives()[0] if get_usb_drives() else None),
         sg.Button('刷新盘符'), sg.Button('一键开卡')],
        [sg.ProgressBar(max_value=100, orientation='h', size=(
            20, 3), key='-PROGRESS-', expand_x=True, bar_color=('Green', 'White'))],
    ], expand_x=True)],
    [sg.Frame('第二步：复制游戏ROM', [
        [sg.Text('请手动把游戏ROM复制到TF卡中对应的目录')],
    ], expand_x=True)],

    [sg.Frame('第三步：选择要重建的目录', [
        [sg.Checkbox('000-MAME', default=True, key='000-MAME', size=(12, 1)),
         sg.Checkbox('001-MD', default=True, key='001-MD', size=(12, 1)),
         sg.Checkbox('002-SFC', default=True, key='002-SFC', size=(12, 1)),
         sg.Checkbox('003-FC', default=True, key='003-FC', size=(12, 1))],
        [sg.Checkbox('004-GBA', default=True, key='004-GBA', size=(12, 1)),
         sg.Checkbox('005-GBC', default=True, key='005-GBC', size=(12, 1)),
         sg.Checkbox('006-GB', default=True, key='006-GB', size=(12, 1)),
         sg.Checkbox('007-PS', default=True, key='007-PS', size=(12, 1))],
        [sg.Checkbox('008-CPS1', default=True, key='008-CPS1', size=(12, 1)),
         sg.Checkbox('009-CPS2', default=True, key='009-CPS2', size=(12, 1)),
         sg.Checkbox('010-IGS', default=True, key='010-IGS', size=(12, 1)),
         sg.Checkbox('011-NEOGEO', default=True, key='011-NEOGEO', size=(12, 1))],
        # [sg.Checkbox('ROMS-OTHER', default=True, key='ROMS-OTHER', size=(12, 1))],
        [sg.Button('为选中的类型生成游戏列表', size=(25, 1))]
    ])],
    [sg.Button('关于', size=(10, 1))]
]

# 创建窗口
window = sg.Window(f'{APP_TITLE} {APP_VERSION}', layout, finalize=True)

# 事件循环
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == '刷新盘符':
        window['-DRIVE-'].update(values=get_usb_drives())
        # 手动设置组合框的大小
        window['-DRIVE-'].set_size((15, 5))  # 设置宽度为15个字符，高度为1行
        # 显示为最后一个选项
        window['-DRIVE-'].update(set_to_index=0)
        sg.popup('刷新盘符成功，请重新选择TF卡', title='成功')
    elif event == '一键开卡':
        selected_drive = values['-DRIVE-']
        if selected_drive:
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            source_folder = os.path.join(
                current_dir, 'data')  # 假设源文件夹在当前目录下的data文件夹中
            destination_folder = selected_drive  # 直接复制到选中的U盘根目录

            copy_to_usb(source_folder, destination_folder)
            # 创建一个线程来执行复制操作，这样不会阻塞UI

        else:
            sg.popup('没有选择TF卡', '请先选择一张TF卡')
    elif event == '为选中的类型生成游戏列表':
        # 这里可以添加生成游戏列表的逻辑
        generate_game_lists_for_selected()
    elif event == '关于':
        sg.popup(f'{APP_TITLE} {APP_VERSION}\n作者: 御坂初琴工作室\n\n这是一个用于E5闭源游戏机的开卡工具，可以一键开卡并生成游戏列表\n\n使用方法：{HOW_TO_USE}',
                 title='关于', font=('Arial', 11))

window.close()
