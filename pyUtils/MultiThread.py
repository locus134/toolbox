import threading
from queue import Queue

class SequenceThread(threading.Thread):
    """
    队列执行线程
    """
    def __init__(self, queue, task, args):
        threading.Thread.__init__(self)

        self.queue = queue
        self.task = task
        self.args = args

    def run(self):
        while True:
            q_id = self.queue.get()
            # 如果队列已满，则继续等待
            if q_id is not None:
                self.task(*self.args)
                self.queue.task_done()
                self.queue.put(q_id)
                break


class MultiThread:
    """
    多线程执行封装， 使用方法：
        mt = MultiThread(50)
        for i in range(100):
            mt.addTask(testFunc, i, i)
        mt.run()
    """
    def __init__(self, max_running=-1):
        """
        多线程执行任务
        :param max_running: 最大同时执行数, 默认-1为不做限制
        """
        self.queue = None
        self.task_list = []
        self.max_running = max_running

    def addTask(self, task, *args):
        """
        添加任务到列表
        :param task: 执行函数
        :param *args: 函数参数列表
        :return: None
        """
        self.task_list.append([task, args])

    def run(self):
        if len(self.task_list) > 0:
            self.queue = Queue(self.max_running)
            queue_num = self.max_running if self.max_running != -1 else len(self.task_list)
            for i in range(queue_num):
                self.queue.put('name' + str(i))

            thread_list = []
            for task_info in self.task_list:
                thread = SequenceThread(self.queue, task_info[0], task_info[1])
                thread.start()
                thread_list.append(thread)

            for thread in thread_list:
                thread.join()

