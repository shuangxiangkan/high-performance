import threading
from socket import *
import time
import pickle
from queue import Queue

# 队列
q=Queue()


# 计算素数的最大范围
max=10000


# 端口号
PORT=8888
# 接收的最大字节数
BUFSIZE=10240

# 发送代码
def send_code(HOST,dict):
    ADDR=(HOST,PORT)
    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(ADDR)

    while True:
        clientSocket.send("control".encode("utf-8"))
        data=clientSocket.recv(BUFSIZE).decode("utf-8")
        if data=="receive ready":
            # 发送字典数据，其中包含计算节点编号，总计算节点数，收集计算节点的ip地址，计算的最大范围max
            clientSocket.send(pickle.dumps(dict))
            data=clientSocket.recv(BUFSIZE).decode("utf-8")
            if data=="dict success":
                content=get_code()
                # 发送代码文件
                for line in content:
                    clientSocket.send((line+"$").encode("utf-8"))
                # 最后一句发送"###"，表示发送结束
                clientSocket.send("###".encode("utf-8"))
                end=clientSocket.recv(BUFSIZE).decode("utf-8")
                q.put(end)
                break

    clientSocket.close()


# 获得所有主机号
def get_hosts():
    with open("hosts.txt","r") as f:
        hosts=f.readlines()
    return hosts

def get_code():
    with open("20185227018.py","r") as f:
        contents=f.readlines()
    return contents


def results(node1,amount):
    ADDR = (node1, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(ADDR)

    clientSocket.send("results".encode())
    data=clientSocket.recv(BUFSIZE).decode("utf-8")
    if data=="ok":
        clientSocket.send(str(amount).encode("utf-8"))
        data = pickle.loads(clientSocket.recv(BUFSIZE))

        print("计算结果为:",data)

    clientSocket.close()

def main():

    # 开始时间
    start=time.time()

    # 线程集合
    threads=[]

    number=1
    # 获得主机号，同时逐个给主机创建一个线程，发送代码文件
    hosts=get_hosts()
    # 计算节点总个数
    amount=len(hosts)
    for host in hosts:
        dict={"number":number,"amount":amount,"node1":hosts[0].strip(),"max":max}
        t=threading.Thread(target=send_code,args=(host.strip(),dict))
        threads.append(t)
        number+=1

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    while True:
        if q.qsize()==amount:
            t=threading.Thread(target=results,args=(hosts[0].strip(),amount))
            t.start()
            t.join()
            break


    end=time.time()
    print("总时间为:",end-start)


main()
