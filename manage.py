# 管理文件
import logging

from flask import render_template, current_app
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

from cars import create_app, db

app = create_app('dev')

manager = Manager(app=app)
manager.add_command('db_command', MigrateCommand)

Migrate(app=app, db=db)

# from werkzeug.routing import BaseConverter
#
#
# class HtmlConverter(BaseConverter):
#     def __init__(self, param, *args):
#         super().__init__(param)
#
#         self.regex = args[0]
#
#
# app.url_map.converters['re'] = HtmlConverter

#
# @app.route('/<re(".*\.html$"):html>')
# def index(html):
#     # logging.info("进入index页面")
#     # logging.log(logging.DEBUG, "debug的模式")
#     # logging.log(logging.INFO, "info的模式")
#     return render_template(html)


if __name__ == '__main__':
    manager.run()
