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
def execute(number,amount,node1):
    # 取出当前计算节点编号
    # number = dict_data["number"]
    # 取出当前所有计算节点个数
    # amount = dict_data["amount"]
    # 执行文件的路径和参数,暂时将计算的数定位1000，等会儿修改一下
    # 还有这个地方的编码问题，执行代码里面有中文注释的时候好像有问题
    path = "python code.py" + " " + str(1000) + " " + str(number) + " " + str(amount)
    result = os.popen(path).read()
    result2 = eval(result)
    print(type(result2))
    print(result2)

    if number==1:
        q.put(result2)
        print("rev_results的queue的个数为：",q.qsize())
    else:
        ADDR1=(node1,PORT)
        node2Socket = socket(AF_INET, SOCK_STREAM)
        node2Socket.connect(ADDR1)

        node2Socket.send("node".encode("utf-8"))
        data=node2Socket.recv(BUFSIZ).decode("utf-8")
        if data=="receive ready":
            node2Socket.send("result ready".encode("utf-8"))
            data=node2Socket.recv(BUFSIZ).decode("utf-8")
            if data=="ok":
                node2Socket.send(pickle.dumps(result2))

    print("execute 结束了")



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
        # print(str)
        with open("code.py","w") as f:
            f.write(str)

    number=dict1["number"]
    amount=dict1["amount"]
    node1=dict1["node1"]
    # 执行代码，并返回结果
    execute(number,amount,node1)
    # 将计算结果发送给control节点
    # clientsocket.send(result.encode("utf-8"))
    print("rev_code结束了")
    clientsocket.send("1".encode("utf-8"))

# 接收其他计算节点的结果
def rev_resuls(clientsocket):
    clientsocket.send("receive ready".encode("utf-8"))
    data=clientsocket.recv(BUFSIZ).decode("utf-8")
    if data=="result ready":
        clientsocket.send("ok".encode("utf-8"))
        # results=[]
        # while True:
        #     result=pickle.loads(clientsocket.recv(BUFSIZ))
        #     if not result:
        #         break
        #     results+=result()
        result = pickle.loads(clientsocket.recv(BUFSIZ))
        print("rev_results接收到的值为:",result)
        print("rev_results的queue的个数为:",q.qsize())
        q.put(result)


def send_results(clientsocket):
    clientsocket.send("ok".encode("utf-8"))
    amount=int(clientsocket.recv(BUFSIZ).decode("utf-8"))

    results=[]
    if q.qsize()==amount:
        print("amount的值为:",amount)
        while not q.empty():
            result=q.get()
            results+=result
        clientsocket.send(pickle.dumps(results))
    print("send_results结束了")

def main():
    while True:
        print("waiting for connection......")
        clientsocket,addr=serversocket.accept()
        print("connection from:",addr)



        data=clientsocket.recv(BUFSIZ).decode("utf-8")
        print(".........",data)
        if data=="control":

            t=threading.Thread(target=rev_code,args=(clientsocket,))
            t.start()
            t.join()
        elif data=="node":
            t=threading.Thread(target=rev_resuls,args=(clientsocket,))
            t.start()
            print("是否执行了node")
            t.join()
        elif data=="results":
            t = threading.Thread(target=send_results, args=(clientsocket,))
            print("是否执行results")
            t.start()
            t.join()

main()

