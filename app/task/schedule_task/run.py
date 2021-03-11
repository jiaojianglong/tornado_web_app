#!usr/bin/env python
# -*- coding:utf-8 -*-

import schedule
import time
import threading
from app.task.models.task import Task
from app.task.schedule_task.manage import Manage

def job():
    task = Task.query.filter(
        Task.status == "unexecute"
    ).order_by(Task.updatetime.asc()).first()
    if task:
        print("执行任务：", task.template.name)
        Manage(task).run()



def thread_job():
    threading.Thread(target=job).start()

def run():
    print("开始循环执行任务")
    schedule.every(3).seconds.do(thread_job)
    while True:
        schedule.run_pending()
        time.sleep(0.1)

threading.Thread(target=run).start()


