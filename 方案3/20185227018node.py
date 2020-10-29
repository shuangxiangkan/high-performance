from socket import *
import threading
import pickle
from queue import Queue

HOST="localhost"
# HOST="10.10.64.182"
PORT=8888
BUFSIZ=1024
ADDR=(HOST,PORT)
# 队列,用来收集所有计算节点的结果
q=Queue()


serversocket=socket(AF_INET,SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(5)

# 执行代码，并返回结果
def execute(dict_data):
    number=dict_data["number"]
    # 计算节点编号为1，直接将结果放进队列
    if number==1:
        q.put([1,2,3])

    # 计算节点编号不为1，则创建一个一个客户端进程，将结果发送给计算节点1
    else:
        HOST1=dict_data["collect_node"].strip()
        ADDR1=(HOST1,PORT)
        clientSocket1 = socket(AF_INET, SOCK_STREAM)
        clientSocket1.connect(ADDR1)

        # 表明是其他计算节点发送过来的
        clientSocket1.send("node".encode("utf-8"))
        data = clientSocket1.recv(BUFSIZ).decode("utf-8")

        if data=="result ready":
            clientSocket1.send(pickle.dumps([4,5,6]))



# 接收代码文件
def rev_code(clientsocket):
    # 准备接收数据
    clientsocket.send("receive ready".encode("utf-8"))
    # 收到字典数据
    dict_data=pickle.loads(clientsocket.recv(BUFSIZ))
    if isinstance(dict_data,dict):
        number=dict_data["number"]
        # print("number:",number)
        # amount=dict_data["amount"]
        # print("amount",amount)
        # collect_node_address=dict_data["collect_node"]
        # print("collect_node_address",collect_node_address)
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

    # 执行代码，并返回结果
    execute(dict_data)
    # result=execute(dict_data)
    # 将计算结果发送给control节点
    # clientsocket.send(result.encode("utf-8"))


def send_results(clientsocket):
    # 准备接收数据

    clientsocket.send("receive ok".encode("utf-8"))
    amount=clientsocket.recv(BUFSIZ).decode("utf-8")
    while True:
        # print("队列长度:",q.qsize())
        if q.qsize()==int(amount):
            t=[]
            while not q.empty():
                t+=q.get()
            clientsocket.send(pickle.dumps(t))
            break


# 接收其他计算节点的结果
def rev_resuls(clientsocket):
    clientsocket.send("result ready".encode("utf-8"))
    result=pickle.loads(clientsocket.recv(BUFSIZ))
    q.put(result)



def main():
    while True:
        print("waiting for connection......")
        clientsocket,addr=serversocket.accept()
        print("connection from:",addr)

        # while True:
        data=clientsocket.recv(BUFSIZ).decode("utf-8")

        # print("....................",data)

        if data=="control":

            t=threading.Thread(target=rev_code,args=(clientsocket,))
            t.start()
            t.join()
            # break
        elif data=="node":
            t=threading.Thread(target=rev_resuls,args=(clientsocket,))
            t.start()
            t.join()
            # break

        elif data=="results":
            # print("创建结果线程")
            t=threading.Thread(target=send_results,args=(clientsocket,))
            t.start()
            t.join()
        # while not q.empty():
        #     qdata=q.get()
        #     print("队列中的数据为:",qdata)

main()

