from socket import *
import threading
import pickle
import os
from queue import Queue

q=Queue()

HOST="localhost"
# HOST="10.10.64.182"
PORT=8888
BUFSIZ=1024
ADDR=(HOST,PORT)

serversocket=socket(AF_INET,SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(5)

# 执行代码，并返回结果
def execute(number,amount,node1,max):
    # 调用os.popen()函数去执行control节点发过来的代码文件
    path = "python code.py" + " " + str(max) + " " + str(number) + " " + str(amount)
    result = os.popen(path).read()
    result2 = eval(result)
    dict={}
    dict["number"]=number
    dict["result"]=result2
    # 输出计算结果
    print("计算节点 ["+str(number)+"] 计算得到的结果为:",result2)

    # 如果是计算节点1，则直接将计算结果放到队列中
    if number==1:
        q.put(dict)
    # 如果不是计算节点1，则需要将计算结果发送到计算节点1，由计算节点1收集所有的计算结果，并返回给控制节点control
    else:
        ADDR1=(node1,PORT)
        node2Socket = socket(AF_INET, SOCK_STREAM)
        node2Socket.connect(ADDR1)

        # 发送node，表明是其他计算节点准备发送给计算节点1
        node2Socket.send("node".encode("utf-8"))
        data=node2Socket.recv(BUFSIZ).decode("utf-8")
        if data=="receive ready":
            node2Socket.send("result ready".encode("utf-8"))
            data=node2Socket.recv(BUFSIZ).decode("utf-8")
            if data=="ok":
                node2Socket.send(pickle.dumps(dict))



# 接收代码文件
def rev_code(clientsocket):
    clientsocket.send("receive ready".encode("utf-8"))
    dict1=pickle.loads(clientsocket.recv(BUFSIZ))
    if isinstance(dict1,dict):
        clientsocket.send("dict success".encode("utf-8"))
        str=""
        flag=True
        while flag:
            data=clientsocket.recv(BUFSIZ).decode("utf-8")
            meta_datas=data.split("$")
            for meta_data in meta_datas:
                if len(meta_data)!=0:
                    if meta_data=="###":
                        flag=False
                        break
                    else:
                        str+=meta_data
        with open("code.py","w") as f:
            f.write(str)

    number = dict1["number"]
    amount = dict1["amount"]
    # node1是计算节点1的ip地址
    node1 = dict1["node1"]
    max = dict1["max"]
    # 执行代码，并返回结果
    execute(number, amount, node1, max)
    clientsocket.send("1".encode("utf-8"))

# 用来接收其他计算节点的结果
def rev_resuls(clientsocket):
    clientsocket.send("receive ready".encode("utf-8"))
    data=clientsocket.recv(BUFSIZ).decode("utf-8")
    if data == "result ready":
        clientsocket.send("ok".encode("utf-8"))
        dict = pickle.loads(clientsocket.recv(BUFSIZ))
        number = dict["number"]
        result = dict["result"]
        print("计算节点 [" + str(number) + "] 计算得到的结果为:", result)
        q.put(dict)

# 用来响应控制节点要求返回结果的要求
def send_results(clientsocket):
    clientsocket.send("ok".encode("utf-8"))
    amount=int(clientsocket.recv(BUFSIZ).decode("utf-8"))

    sum=0
    if q.qsize() == amount:
        while not q.empty():
            result = q.get()
            number = result["result"]
            sum += number
        clientsocket.send(str(sum).encode("utf-8"))

def main():
    while True:
        print("waiting for connection......")
        clientsocket,addr=serversocket.accept()
        print("connection from:", addr)


        # 根据收到的data的值判断该socket的目的
        data=clientsocket.recv(BUFSIZ).decode("utf-8")
        # 如果data=control，则表示是控制节点发出的用来发送代码文件的
        if data=="control":

            t=threading.Thread(target=rev_code,args=(clientsocket,))
            t.start()
            t.join()
        # 如果data=node，则表示是其他计算节点发送的
        elif data=="node":
            t=threading.Thread(target=rev_resuls,args=(clientsocket,))
            t.start()
            t.join()
        # 如果data=results,则表示也是控制节点发来的，但是是用来收集结果的
        elif data=="results":
            t = threading.Thread(target=send_results, args=(clientsocket,))
            t.start()
            t.join()

main()

