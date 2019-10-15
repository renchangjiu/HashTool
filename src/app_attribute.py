import os
import sys


class AppAttribute(object):
    # 应用名称
    app_name = "HashUtil"

    # 应用根目录
    root = os.path.split(sys.argv[0])[0]
