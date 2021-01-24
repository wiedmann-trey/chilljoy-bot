import heapq 
import asyncio
import datetime

class Scheduler:
    def __init__(self,poll_rate):
        self.pq = []
        self.poll_rate = poll_rate

    async def loop(self):
        while True:
            while len(self.pq) > 0 and self.pq[0][0] < datetime.datetime.now(): 
                ev = heapq.heappop(self.pq)
                await ev[2](ev[1])
            await asyncio.sleep(self.poll_rate)

    def addEvent(self, dt, user, call):
        heapq.heappush(self.pq, Scheduler.event(dt, user, call))

    def event(dt, user, call):
        return (datetime.datetime.now() + dt, user, call)

