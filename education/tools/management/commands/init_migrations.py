# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.makemigrations import Command as makemigrations_Command
from django_extensions.management.commands.clean_pyc import Command as clean_pyc_Command
from connection import Connection
from posixpath import join as path_join

global select
global execute
global commit

SQL_check_migrations_SELECT = 'SELECT * FROM django_migrations WHERE app=? AND name=?'
SQL_insert_db_migrations_INSERT = 'INSERT INTO "django_migrations" (app,name,applied) VALUES (?, ?, ?)'

def init_go(db_path, project_path):
    global select
    global execute
    global commit
    db = Connection(db_path)
    select = db.select
    execute = db.execute
    commit = db.commit
    execute('delete from django_migrations')
    delete_migrations(project_path)

    makemigrations_Command().run_from_argv(['./manage.py', 'makemigrations'])
    clean_pyc_Command().run_from_argv(['./manage.py', 'clean_pyc'])

    init_migrations(project_path)

def delete_migrations(path, app=None):
    try:
        list = os.listdir(path)
    except OSError:
        return

    if 'migrations' in list:
        delete_migrations_list(path_join(path, 'migrations'), app)
    for i in list:
        delete_migrations(path_join(path, i), i)

def delete_migrations_list(path, app):
    migrations_list = os.listdir(path)
    if '0001_initial.py' not in migrations_list:
        return
    migrations_list.pop(migrations_list.index('__init__.py'))
    for migration in migrations_list:
        os.remove(path_join(path, migration))



def init_migrations(path, app=None):
    try:
        list = os.listdir(path)
    except OSError:
        return

    if 'migrations' in list:
        inser_db(path_join(path, 'migrations'), app)
    for i in list:
        init_migrations(path_join(path, i), i)

def inser_db(path, app):
    migrations_list = os.listdir(path)
    if '0001_initial.py' not in migrations_list:
        return
    migrations_list.pop(migrations_list.index('__init__.py'))
    for migration in migrations_list:
        if select(SQL_check_migrations_SELECT, (app, migration.split('.py')[0])):
            raise CommandError('err')
        execute(SQL_insert_db_migrations_INSERT, (app, migration.split('.py')[0], '2018-08-29 20:35:55.909400'))


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_go(path_join(settings.BASE_DIR, 'var', 'db.sqlite3'), path_join(settings.BASE_DIR))
        commit()

# init_go('/home/shaojiajun314/Desktop/yt131/var/db.sqlite3', '/home/shaojiajun314/Desktop/yt131')
