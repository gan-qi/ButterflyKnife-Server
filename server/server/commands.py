# -*- coding: utf-8 -*-
import click
from datetime import datetime

from server import app, db
from server.models import DEP, USER, TASK

from random import randint


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def user():
    """插入用户数据"""
    try:
        # 先插入部门数据
        depExample = DEP(name="研发")
        db.session.add(depExample)
        # 再插入用户数据
        userInfo = USER(name="tom", role=0, password="adminadmin", dep_id=1)
        userInfo2 = USER(name="jerry", role=1, password="adminadmin", dep_id=1)
        db.session.add(userInfo)
        db.session.add(userInfo2)
        db.session.commit()
        click.echo('灌入用户数据成功!')
    except Exception as e:
        click.echo('灌入用户数据失败：')
        click.echo(e)

@app.cli.command()
def task():
    """插入任务数据"""
    for i in range(1, 10):
        taskExample = TASK(title='task%s'%(i), desc='heihei',
                ctime=datetime.now().strftime("%Y%m%d"),
                wtime=datetime.now().strftime("%Y%m%d"),
                etime=datetime.now().strftime("%Y%m%d"),
                status=randint(0, 2),
                color="black", user_id=1)
        db.session.add(taskExample)
    db.session.commit()
