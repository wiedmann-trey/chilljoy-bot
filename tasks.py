import datetime

now = datetime.datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
print(now.second)

def difference(time1, time2):
    date = datetime.date(1, 1, 1)
    datetime1 = datetime.datetime.combine(date, time1)
    datetime2 = datetime.datetime.combine(date, time2)
    time_elapsed = datetime1 - datetime2
    return time_elapsed

class TaskScheduler():
    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)


class Task():
    def __init__(self, description, hour, minute):
        self.description = description
        self.time = datetime.time(hour=hour, minute=minute)
        self.done = False

    def time_until(self):
        return difference(self.time,datetime.datetime.now().time())
t = Task("Finish Math problems", 20, 30)