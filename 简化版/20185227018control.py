import threading
from socket import *
import time
import pickle
from queue import Queue


q=Queue()

# 总结点个数
amount=2


# 端口号
PORT=8888
# 接收的最大字节数
BUFSIZE=1024

def send_code(HOST,dict):
    ADDR=(HOST.strip(),PORT)

    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(ADDR)

    while True:
        clientSocket.send("control".encode("utf-8"))
        data=clientSocket.recv(BUFSIZE).decode("utf-8")
        if data=="receive ready":
            # 发送字典数据
            clientSocket.send(pickle.dumps(dict))
            data=clientSocket.recv(BUFSIZE).decode("utf-8")
            if data=="dict success":
                content=get_code()
                # 发送代码文件
                for line in content:
                    clientSocket.send((line+"$").encode("utf-8"))
                # 最后一句发送"###"，表示发送结束
                clientSocket.send("###".encode("utf-8"))
                result=pickle.loads(clientSocket.recv(BUFSIZE))
                # print(result)
                q.put(result)
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


def resutls():
    result=[]
    while True:
        if q.qsize()==amount:
            while not q.empty():
                result+=q.get()

            # 排序
            sorted_list=sorted(result)
            print(sorted_list)
            break


def main():

    # 开始时间
    start=time.time()

    # 线程集合
    threads=[]

    number=1
    # 获得主机号，同时逐个给主机创建一个线程，发送代码文件
    hosts=get_hosts()
    for host in hosts:
        print(host)
        dict={"number":number,"amount":amount}
        t=threading.Thread(target=send_code,args=(host.strip(),dict))
        threads.append(t)
        number+=1

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


    t=threading.Thread(target=resutls)
    t.start()
    t.join()


    end=time.time()
    print("总时间为:",end-start)


main()
