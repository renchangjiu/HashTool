import win32clipboard as clipboard
import win32con

null = None


class ClipboardUtil(object):
    @staticmethod
    def get_text():
        """  读取剪切板  """
        clipboard.OpenClipboard()
        d = clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        clipboard.CloseClipboard()
        return d

    @staticmethod
    def set_text(string: str):
        if str is null:
            return
        """ 写入剪切板  """
        clipboard.OpenClipboard()
        clipboard.EmptyClipboard()
        clipboard.SetClipboardData(win32con.CF_UNICODETEXT, string)
        clipboard.CloseClipboard()


def test():
    ClipboardUtil.set_text("adb中文qwe!@#$%123")
    print(ClipboardUtil.get_text())


if __name__ == "__main__":
    test()
