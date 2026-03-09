import logging

from queue import Queue
from threading import Thread
from logging.handlers import RotatingFileHandler, QueueHandler

from settings import config_loader


class AsyncLogWriter:
    def __init__(self):
        self.queue = Queue(maxsize=10_000)
        self.handler = RotatingFileHandler(
            config_loader('LOG_FILE'),
            maxBytes=50_000_000,
            backupCount=10,
            encoding='utf-8',
        )
        self.handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        ))
        self.thread = Thread(target=self._write_loop, daemon=True)
        self.thread.start()

    def _write_loop(self):
        while True:
            record = self.queue.get()
            self.handler.emit(record)
            self.queue.task_done()


log_writer = AsyncLogWriter()

logger = logging.getLogger('play_pulse')
logger.handlers.clear()
logger.addHandler(QueueHandler(log_writer.queue))
logger.setLevel(logging.DEBUG)
logger.propagate = False
