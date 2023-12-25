import queue

class Process:
    def __init__(self, pid, burst_time, priority):
        self.pid = pid
        self.burst_time = burst_time
        self.priority = priority
        self.wait_time = 0

class MLQ:
    def __init__(self, num_queues):
        self.queues = [queue.Queue() for _ in range(num_queues)]

    def add_process(self, process):
        if process.priority < len(self.queues):
            self.queues[process.priority].put(process)
        else:
            print(f"Process {process.pid} has invalid priority {process.priority}. Skipping.")

    def execute(self):
        while any(not q.empty() for q in self.queues):
            for i, q in enumerate(self.queues):
                if not q.empty():
                    process = q.get()
                    print(f"Executing process {process.pid} from queue {i}")
                    process.burst_time -= 1
                    if process.burst_time > 0:
                        process.wait_time += 1
                        if process.wait_time > len(self.queues) - 1:
                            process.wait_time = 0
                            process.priority += 1
                            if process.priority >= len(self.queues):
                                process.priority = len(self.queues) - 1
                        self.queues[process.priority].put(process)


def test_mlq():
    mlq = MLQ(3)

    p1 = Process(1, 5, 0)
    p2 = Process(2, 3, 1)
    p3 = Process(3, 4, 2)

    mlq.add_process(p1)
    mlq.add_process(p2)
    mlq.add_process(p3)

    mlq.execute()

    assert p1.burst_time == 0
    assert p2.burst_time == 0
    assert p3.burst_time == 0

test_mlq()
