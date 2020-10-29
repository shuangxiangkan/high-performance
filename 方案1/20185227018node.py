from socket import *
import threading

HOST="localhost"
# HOST="10.10.64.182"
PORT=8888
BUFSIZ=1024
ADDR=(HOST,PORT)

serversocket=socket(AF_INET,SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(5)

# 执行代码，并返回结果
def execute():
    return "messi"

# 接收代码文件
def rev_code(clientsocket):
    clientsocket.send("receive ready".encode("utf-8"))
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
    print(str)
    with open("code.py","w") as f:
        f.write(str)

    # 执行代码，并返回结果
    result=execute()
    # 将计算结果发送给control节点
    clientsocket.send(result.encode("utf-8"))

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

