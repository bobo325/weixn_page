#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2018/1/9 9:42
"""
import os

from PIL import Image
from flask import request

from config import web
from const import msg
from flask_app import app
from service.base.media import add_media, list_media, delete_media, detail_media, \
    modify_media_type, list_media_type, modify_media
from util.common import build_ret, get_uuid, to_list, get_g, build_ret_one


@app.route("/mediaType/list", methods=["GET"])
def media_type_list():
    result = list_media_type()
    return build_ret(msg.SYS_SUCCESS, data=result)


@app.route("/mediaType/update", methods=["POST"])
def media_type_modify():
    current_user = get_g().user
    params = request.get_json()
    modify_media_type(data=params, updator=current_user.id)
    return build_ret(msg.SYS_SUCCESS)


@app.route("/media/list", methods=["GET"])
def media_list():
    params = request.args.to_dict()
    total, result = list_media(params)
    return build_ret(msg.SYS_SUCCESS, data=result, total=total)


@app.route("/media/thumbnail", methods=["POST"])
def media_thumbnail():
    params = request.get_json()
    result = detail_media(params["id"])
    url = result["url"]
    # 生成缩略图
    result["url"], result["size"] = resize_image(filein=url, long=params["long"], wide=params["wide"])
    result["resolution"] = str(params["long"]) + "X" + str(params["wide"])
    result.pop("id")
    current_user = get_g().user
    if not add_media(result, creator=current_user.id):
        return build_ret(msg.SYS_FAIL)
    if result:
        return build_ret(msg.SYS_SUCCESS)
    return build_ret(msg.SYS_RECORD_NOT_FOUND)


@app.route("/media/update", methods=["POST"])
def media_modify():
    current_user = get_g().user
    params = request.get_json()
    modify_media(params, updator=current_user.id)
    return build_ret(msg.SYS_SUCCESS)


@app.route("/media/detail", methods=["GET"])
def media_detail():
    params = request.args.to_dict()
    result = detail_media(params["id"])
    if result:
        return build_ret(msg.SYS_SUCCESS, data=result)
    return build_ret(msg.SYS_RECORD_NOT_FOUND)


@app.route("/media/delete", methods=["POST"])
def media_delete():
    current_user = get_g().user
    params = request.get_json()
    delete_media(to_list(params["ids"]), oid=current_user.id)
    return build_ret(msg.SYS_SUCCESS)


@app.route("/media/upload", methods=["POST"])
def media_upload():
    if request.method == 'POST':
        current_user = get_g().user
        files = request.files.getlist('file')
        file_urls = []
        for each_file in files:
            media = MediaUpload(each_file).upload()
            if not media:
                return build_ret(msg.FILE_FORMAT_ERR)
            file_urls.append(media.show_url)
            file_info = {
                "name": each_file.filename.rsplit('.', 1)[0],
                "type": media.type,
                "uploader": current_user.id,
                "size": len(media.content),
                "url": media.show_url
            }
            if media.type == "image":
                with open(media.file_dir, "rb") as f:
                    img = Image.open(f)
                    file_info["resolution"] = str(img.size[0]) + "X" + str(img.size[1])
            # elif allow_result == "audio":
            #     # TO DO 获取音频长度
            #     pass
            # elif allow_result == "video":
            #     # TO DO 获取视频长度
            #     pass
            add_media(file_info, creator=current_user.id)

        result = {
            'file_url': file_urls
        }
        return build_ret_one(msg.SYS_SUCCESS, data=result)


def check_file_path(file_path, file_type):
    """
    检查文件路径
    :param file_path: 基础文件路径
    :param file_type: 文件类型
    :return:
    """

    if file_path[0] == ".":
        cwd = os.getcwd()
        re_file_path = os.path.abspath(file_path)
        file_dir = os.path.join(re_file_path, file_type)
        # 判断存储路径是否存在
        if os.path.isdir(file_dir):
            return file_dir
        else:
            os.chdir(file_path)
            os.mkdir(file_type)
            os.chdir(cwd)
            return file_dir
    else:
        file_dir = os.path.join(file_path, file_type)
        # 判断存储路径是否存在
        if os.path.isdir(file_dir):
            return file_dir
        else:
            os.chdir(file_path)
            os.mkdir(file_type)
            return file_dir


def resize_image(filein, long, wide):
    """
    修改图片大小
    :param filein: 打开的文件路径
    :param long: 长
    :param wide: 宽
    :return:
    """
    img = Image.open(web["pic_read"] + filein)
    out = img.resize((long, wide), Image.ANTIALIAS)  # resize image with high-quality
    filename = get_uuid() + '.png'
    files_path = check_file_path("%s%s/upload" % (web['pic_read'], web['pic_pix']), "image")
    out.save(os.path.join(files_path, filename))
    file_url = web['pic_pix'] + "upload/" + "image" + "/" + filename
    # 本机测试
    # file_url = "\\static_file\\upload\\" + "image" + "\\" + filename
    file_size = os.path.getsize(web["pic_read"] + file_url)
    return file_url, file_size


class MediaUpload:
    def __init__(self, raw):
        self.raw = raw
        self.file_type = raw.filename.rsplit('.', 1)[1]
        self.path = "%s%s/upload" % (web['pic_read'], web['pic_pix'])
        self.content = self.raw.read()
        self.filename = "{}.{}".format(get_uuid(), self.file_type)
        self.file_dir = ''
        self.type = self.is_allowed_file()
        self.show_url = os.path.join(web['pic_pix'], "upload", os.path.join(self.type, self.filename))\
            .replace(os.sep, "/")

    def upload(self):
        if isinstance(self.type, str):
            self.file_dir = os.path.join(self.path, os.path.join(self.type, self.filename)).replace('/', os.sep)
            with open(self.file_dir, "wb") as f:
                f.write(self.content)
            return self
        return False

    def is_allowed_file(self):
        allow_media_types = list_media_type()
        for value in allow_media_types:
            if self.file_type and self.file_type in value['format'] and len(self.content) < value['limit_size']:
                return value["type_name"]
        return False
