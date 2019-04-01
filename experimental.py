import io
from threading import Thread
import time
import requests
from CloseableQueue import CloseableQueue, Closed


class ReaderWorker(Thread):

    def __init__(self, queue, url):
        super(ReaderWorker, self).__init__()
        self.url = url
        self.queue = queue

    def run(self):
        print("ReaderWorker: starting")
        def deq():
            while True:
                try:
                    b = self.queue.get()
                    print("ReaderWorker: got bytes: {}".format(b))
                    yield b
                except Closed:
                    print("ReaderWorker: Queue closed.")
                    return

        requests.post(self.url, data=deq())
        print("ReaderWorker: finished")


class QueueWriter:

    def __init__(self, queue):
        self.queue = queue

    def write(self, b):
        self.queue.put(b)


class RemoteFileUploader():
    """A class that allows parallel file uploading.  Open with the with
    statement.  Provides a writable object where bytes are supposed to
    be written to."""

    def __init__(self, host, port, filename):
        self.url = "http://{}:{}/".format(host, port)
        self.filename = filename
        self.queue = CloseableQueue()
        self.rw = ReaderWorker(self.queue, self.url)
        self.queue_writer = QueueWriter(self.queue)

    def __enter__(self):
        self.rw.start()
        return self.queue_writer

    def __exit__(self, type, value, tb):
        self.queue.close()
        self.rw.join()
        print('Data sent to server.')


def main():
    print("Main started")

    with RemoteFileUploader("localhost", 5000, "filename.txt") as f:
        for c in b"Hello World!":
            print("Main: {}".format(c))
            f.write(c)
            time.sleep(0.5)


if __name__ == "__main__":
    main()
