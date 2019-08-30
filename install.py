import os
import sys
import winreg
from src.app_attribute import AppAttribute as app


def add_context_menu():
    root = os.path.split(os.path.abspath(sys.argv[0]))[0]
    root = root.replace("\\", "/")
    pythonw_path = os.path.split(sys.executable)[0] + "/pythonw.exe"
    run_file_path = root + "/main.py"
    # C:\\Applications\\Python37/pythonw.exe "C:\\Users\\13595\\PycharmProjects\\HashTool/main.py" "%1"
    py_command = r'%s "%s" ' % (pythonw_path, run_file_path) + '"%1"'
    # 打开名称父键
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'*\\shell')
    # 为key创建一个名称为menu_name的sub_key, 并设置sub_key的值为menu_name加上快捷键, 数据类型为REG_SZ字符串类型
    winreg.SetValue(key, app.app_name, winreg.REG_SZ, app.app_name)

    # 打开刚刚创建的名为menu_name的sub_key
    ex_sub_key = winreg.OpenKeyEx(key, app.app_name, 0, winreg.KEY_SET_VALUE)
    # 添加项, 为sub_key添加名为'command'的子键, 并设置其值为command, 数据类型为REG_SZ字符串类型
    winreg.SetValue(ex_sub_key, 'command', winreg.REG_SZ, py_command)
    # 添加值
    winreg.SetValueEx(ex_sub_key, "icon", 0, winreg.REG_SZ, root + "/resource/image/app.ico")

    # 关闭sub_key和key
    winreg.CloseKey(ex_sub_key)
    winreg.CloseKey(key)


def test():
    add_context_menu()


if __name__ == '__main__':
    test()
