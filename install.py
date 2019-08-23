import winreg


def add_context_menu():
    # 菜单名称
    menu_name = 'HashUtil'
    # 执行一个python脚本的命令, 用于打印命令行参数的第二个参数（即选中的文件路径）
    py_command = r'D:\applications\Python3.7.2\pythonw.exe "D:\su\workspace\GitHub\HashTool\main.py" "%1"'

    # 打开名称父键
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'*\\shell')
    # 为key创建一个名称为menu_name的sub_key, 并设置sub_key的值为menu_name加上快捷键, 数据类型为REG_SZ字符串类型
    winreg.SetValue(key, menu_name, winreg.REG_SZ, menu_name)

    # 打开刚刚创建的名为menu_name的sub_key
    sub_key = winreg.OpenKey(key, menu_name)
    # 为sub_key添加名为'command'的子键, 并设置其值为command, 数据类型为REG_SZ字符串类型
    winreg.SetValue(sub_key, 'command', winreg.REG_SZ, py_command)

    # 关闭sub_key和key
    winreg.CloseKey(sub_key)
    winreg.CloseKey(key)


def add_show_file_path_menu():
    """
    添加右键菜单, 可以在右键点击一个文件、目录、文件夹空白处或驱动器盘符后在命令行中打印出当前的绝对路径
    :return: None
    """

    # D:\su\workspace\GitHub\HashTool\resource\image\HashUtil.ico
    # 添加文件右键菜单
    # add_context_menu(menu_name, py_command, winreg.HKEY_CLASSES_ROOT, r'*\\shell')
    # 添加文件夹右键菜单
    # add_context_menu(menu_name, py_command, winreg.HKEY_CLASSES_ROOT, r'Directory\\shell', 'S')
    # 添加文件夹空白处右键菜单
    # add_context_menu(menu_name, py_command, winreg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', 'S')
    # 添加磁盘驱动器右键菜单
    # add_context_menu(menu_name, py_command, winreg.HKEY_CLASSES_ROOT, r'Drive\\shell', 'S')


def test():
    add_context_menu()


if __name__ == '__main__':
    test()
