#! /usr/bin/env python3
from web_client import RemoteFile


def main():
    data = b"Hello World!"
    print ("Client data: {}".format(data))

    with RemoteFile("localhost", 5000, "hello.txt") as f:
        print("Opened remote file.")
        f.write(data)
        print("Data written.")


if __name__ == "__main__":
    main()
