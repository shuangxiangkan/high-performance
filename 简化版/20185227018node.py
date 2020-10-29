from socket import *
import threading
import pickle
import os
from queue import Queue

q=Queue

HOST="localhost"
# HOST="10.10.64.182"
PORT=8888
BUFSIZ=1024
ADDR=(HOST,PORT)

serversocket=socket(AF_INET,SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(5)

# 执行代码，并返回结果
def execute(number,amount,clientsocket):
    # 取出当前计算节点编号
    # number = dict_data["number"]
    # 取出当前所有计算节点个数
    # amount = dict_data["amount"]
    # 执行文件的路径和参数,暂时将计算的数定位1000，等会儿修改一下
    # 还有这个地方的编码问题，执行代码里面有中文注释的时候好像有问题
    path = "python code.py" + " " + str(100) + " " + str(number) + " " + str(amount)

    result = os.popen(path).read()

    result2 = eval(result)
    print(type(result2))
    print(result2)
    clientsocket.send(pickle.dumps(result2))




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
    # 执行代码，并返回结果
    execute(number,amount,clientsocket)
    # 将计算结果发送给control节点
    # clientsocket.send(result.encode("utf-8"))

# 接收其他计算节点的结果
def rev_resuls():
    return 0


def main():
    while True:
        print("waiting for connection......")
        clientsocket,addr=serversocket.accept()
        print("connection from:",addr)

        while True:
            data=clientsocket.recv(BUFSIZ).decode("utf-8")
            if data=="control":

                t=threading.Thread(target=rev_code,args=(clientsocket,))
                t.start()
                t.join()
                break
            elif data=="node":
                t=threading.Thread(target=rev_resuls)
                t.start()
                t.join()

main()

