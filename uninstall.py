import winreg

from src.app_attribute import AppAttribute as app


def delete_reg_key():
    try:
        parent_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\\shell")
        menu_key = winreg.OpenKey(parent_key, app.app_name)
        # 删除子项
        winreg.DeleteKey(menu_key, 'command')
        # 删除父项
        winreg.DeleteKey(parent_key, app.app_name)
        winreg.CloseKey(parent_key)
    except Exception as msg:
        print(msg)


def main():
    delete_reg_key()


if __name__ == '__main__':
    main()
