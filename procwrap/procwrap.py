import time
from io import StringIO
from subprocess import PIPE, Popen
from threading import Thread
from queue import Queue

class Observer:
    def __init__(self, command=[], user_inputs=[]):
        self.process = Popen(
            command,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            bufsize=0
        )
        self.user_inputs = user_inputs
        self.lines = Queue()
        self.cur_line = StringIO()
        self.cur_output_last_time = time.time()
        self.outputting = False
        self.stop_flag = False

        self.read_output_thread = Thread(target=self._read_output)
        self.clock_thread = Thread(target=self._clock)

        self.read_output_thread.start()
        self.clock_thread.start()

        self.stdout = ""

    def _read_output(self):
        self.outputting = True
        while not self.stop_flag:
            char = self.process.stdout.read(1)
            if not char or self.process.poll() is not None:
                return
            self.cur_line.write(char)
            self.cur_output_last_time = time.time()

    def _clock(self):
        while not self.stop_flag:
            time.sleep(0.1)
            cur_line_interval = self.cur_line.getvalue()
            if time.time() - self.cur_output_last_time > 0.3 or '\n' in cur_line_interval:
                if len(cur_line_interval) > 0:
                    self.lines.put(cur_line_interval.rstrip('\n'))
                    self.cur_line.seek(0)
                    self.cur_line.truncate(0)
                    self.outputting = False
            else:
                self.outputting = True

    def get(self):
        while self.outputting:
            time.sleep(0.01)
        return self.lines.get()

    def write(self, data: str):
        while self.outputting:
            time.sleep(0.01)
        self.process.stdin.write(data)
        self.process.stdin.flush()

    def exit(self):
        self.stop_flag = True
        self.process.terminate()
        self.process.wait()

    def start(self):
        for user_input in self.user_inputs:
            self.stdout += self.get()
            self.write(user_input)
            self.stdout += user_input

        self.stdout += self.get()
        self.exit()

    def save(self, filename: str):
        with open(filename, 'w') as f:
            f.write(self.stdout)