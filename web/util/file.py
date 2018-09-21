# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2018-01-08 17:26
"""
import os
from os import path


def package_import(package, excludes=None):
    """
    引用包内的所有py文件
    :param excludes: type(list) 需要排除文件名称
    :param package: type(str)包路径, 多级路径用 . 分隔, 例如 user.config.pkg
    :return:
    """
    if excludes is None:
        excludes = []
    try:
        package_path = package.replace(".", os.sep)
        root_path = get_abs_path()
        files = [x for x in get_dir_files_with_py(package_path) if x not in excludes]
        packages = []
        for file in files:
            file = file.replace(root_path + os.sep, "")
            file = file.replace(os.sep, ".")
            file = file.replace(".py", "")
            packages.append(file)
        for pkg in packages:
            __import__(pkg)
    except OSError:
        raise ValueError("package [%s] not exists, please checking!" % package)


def get_dir_files_with_py(dir_path):
    """
    获取当前路径下所有py文件
    :param dir_path: 相对项目根目录的路径
    :return:
    """
    abs_path = get_abs_path(dir_path)
    files = []
    paths = []
    for x in os.listdir(abs_path):
        file = os.path.join(abs_path, x)
        if os.path.isdir(file):
            paths.append(file)
        else:
            files.append(file)
    files = [x for x in files if "__" not in x and ".pyc" not in x]
    paths = [x for x in paths if not x.startswith("__")]

    for p in paths:
        files += get_dir_files_with_py(p)
    return files


def get_abs_path(*args):
    """
    根据args从根目录获取文件的绝对路径
    :param args: 例如 get_file_path("1","2","3.xml") -> ${root_dir}/1/2/3.xml
    :return: 文件的绝对路径
    """
    previous_path = "/../../"
    root_dir = path.abspath(__file__ + previous_path)
    for arg in args:
        if isinstance(arg, tuple):
            for a in arg:
                root_dir = path.join(root_dir, a)
        else:
            root_dir = path.join(root_dir, arg)
    return root_dir
