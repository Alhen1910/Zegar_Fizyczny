import time

# Random będzie generował losowy czas
import random

# Threading będzie symulował współbieżne procesy
from threading import Thread, Lock

# Klasa Process dziedziczy po Thread, aby uruchmic każdy proces jako osobny wątek
class Process(Thread):
    def __init__(self, process_id, max_time_interval):
        super().__init__()
        self.process_id = process_id
        self.clock = 0
        self.max_time_interval = max_time_interval
        self.lock = Lock()

    # Symulowanie czasu pomiędzy zdarzeniami
    def run(self):
        while True:
            self.internal_event()
            time.sleep(random.uniform(0.5, 2))

    # Zwiększanie zegara o losowy przedział czasu
    def internal_event(self):
        time_interval = random.randint(1, self.max_time_interval)
        with self.lock:
            self.clock += time_interval
            print(f"Proces {self.process_id}: Zdarzenie wewnętrzne, czas = {self.clock}")

# Metody "send_message" i "receive_message" obsługują komunikację oraz synchronizują zegary między procesami
    def send_message(self, recipient):
        with self.lock:
            message_time = self.clock
            print(f"Proces {self.process_id}: Wysłano wiadomość, czas = {self.clock}")
        recipient.receive_message(message_time)

    def receive_message(self, message_time):
        with self.lock:
            self.clock = max(self.clock, message_time)
            print(f"Proces {self.process_id}: Otrzymano wiadomość, synchronizacja czasu = {self.clock}")

# Symulowanie procesów i komunikacji
def simulate_processes(num_processes, max_time_interval, num_messages):
    processes = [Process(process_id, max_time_interval) for process_id in range(num_processes)]

    for process in processes:
        process.start()

    for _ in range(num_messages):
        sender = random.choice(processes)
        recipient = random.choice(processes)
        if sender != recipient:
            sender.send_message(recipient)

            # Symulowanie czasu pomiędzy wiadomościami
            time.sleep(random.uniform(1, 3))

    for process in processes:
        process.join()


if __name__ == "__main__":
    simulate_processes(num_processes=5, max_time_interval=5, num_messages=10)