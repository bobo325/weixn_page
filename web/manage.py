#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/4/16 15:25
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# 主文件中导入app初始化manage
from flask_app.app import app
from flask_app.app import db

# business model
from util.file import package_import

package_import("model")


# 让python支持命令行工作
manager = Manager(app)

# 使用migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


# 初始化  python manage.py db init
# 创建迁移脚本  python manage.py db migrate
# 更新数据库  python hello.py db upgrade




