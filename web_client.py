import io
import requests


class RemoteFile():

    def __init__(self, host, port, filename):
        self.url = "http://{}:{}/".format(host, port)
        self.filename = filename
        self.bytesIO = None

    def __enter__(self):
        self.bytesIO = io.BytesIO()
        return self.bytesIO

    def __exit__(self, type, value, tb):
        self.bytesIO.seek(0)
        files = {'file': self.bytesIO}
        requests.post(self.url, files=files,
                      data={'filename': self.filename})
        print('Data sent to server.')
