from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
print(now.second)

class TaskScheduler():
    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)


class Task():
    def __init__(self, description, hour, minute):
        self.description = description
        self.time = datetime.time(hour=hour, minute=minute)
