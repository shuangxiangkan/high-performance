import threading
from socket import *
import time
import pickle


# 总结点个数
amount=2


# 端口号
PORT=8888
# 接收的最大字节数
BUFSIZE=1024

def send_code(HOST,dict):
    ADDR=(HOST,PORT)
    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(ADDR)

    while True:
        # "control"表明是控制
        clientSocket.send("control".encode("utf-8"))
        data = clientSocket.recv(BUFSIZE).decode("utf-8")
        if data == "receive ready":
        # 发送一个字典数据，字典中包含计算节点编号，计算节点总数，第一个计算节点的地址
            clientSocket.send(pickle.dumps(dict))
            data=clientSocket.recv(BUFSIZE).decode("utf-8")
            if data=="dict success":
                content=get_code()
                # 发送代码文件
                for line in content:
                    clientSocket.send((line+"$").encode("utf-8"))
                # 最后一句发送"###"，表示发送结束
                clientSocket.send("###".encode("utf-8"))
                # result=clientSocket.recv(BUFSIZE).decode("utf-8")
                # print(result)
                break


def recv_results(collect_node):
    ADDR = (collect_node.strip(), PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    print("地址为:",collect_node)
    clientSocket.connect(ADDR)

    while True:
        # "results"表明是手机计算结果的socket
        clientSocket.send("results".encode("utf-8"))
        data = clientSocket.recv(BUFSIZE).decode("utf-8")
        if data=="receive ok":
            clientSocket.send(str(amount).encode("utf-8"))
            results=pickle.loads(clientSocket.recv(BUFSIZE))
            print("results:",results)
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
    # 给每个计算节点编号，第一个计算节点为1
    number=1
    # 将第一个节点作为接收其他计算节点的节点
    collect_node=hosts[0]
    for host in hosts:
        print(host)
        dict={"number":number,"amount":amount,"collect_node":collect_node}
        t=threading.Thread(target=send_code,args=(host.strip(),dict))
        threads.append(t)
        number+=1

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # 创建一个接受所有计算结果的线程
    result_thread=threading.Thread(target=recv_results,args=(collect_node,))
    result_thread.start()
    result_thread.join()


    end=time.time()
    print("总时间为:",end-start)


main()
