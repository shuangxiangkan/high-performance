import threading
from socket import *
import time


# 总结点个数
amount=3


# 端口号
PORT=8888
# 接收的最大字节数
BUFSIZE=1024

def send_code(HOST):
    ADDR=(HOST,PORT)
    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(ADDR)

    while True:
        clientSocket.send("control".encode("utf-8"))
        data=clientSocket.recv(BUFSIZE).decode("utf-8")
        if data=="receive ready":
            content=get_code()
            # 发送代码文件
            for line in content:
                clientSocket.send((line+"$").encode("utf-8"))
            # 最后一句发送"###"，表示发送结束
            clientSocket.send("###".encode("utf-8"))
            result=clientSocket.recv(BUFSIZE).decode("utf-8")
            print(result)
            break






# 获得所有主机号
def get_hosts():
    with open("hosts.txt","r") as f:
        hosts=f.readlines()
    return hosts

def get_code():
    with open("20185227018.py","r") as f:
        contents=f.readlines()
    return contents


def main():

    # 开始时间
    start=time.time()

    # 线程集合
    threads=[]

    # 获得主机号，同时逐个给主机创建一个线程，发送代码文件
    hosts=get_hosts()
    for host in hosts:
        print(host)
        t=threading.Thread(target=send_code,args=(host.strip(),))
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


    end=time.time()
    print("总时间为:",end-start)


main()
