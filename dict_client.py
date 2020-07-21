"""
dict 客户端：发起请求，接受结果，呈现数据
tcp循环模型客户端
"""
from socket import *
import sys

ADDR=('127.0.0.1',6666)

# 查询单词
def do_query(sock,name):
    while True:
        word=input("查询单词:").strip() # strip()去除空格
        if word == '##':
            break

        msg="Q %s %s"%(name,word)
        sock.send(msg.encode())
        # 无论是否查询到单词，把反馈回来的结果都打印
        result = sock.recv(1024).decode()
        print(result)

# 历史记录
def do_history(sock,name):
    msg = "H "+name
    sock.send(msg.encode())
    # 接收历史记录，实际客户端不知道会有多少个
    while True: # 不确定有多个时，使用死循环
        # 每次接收一个
        data = sock.recv(1024).decode()
        if data =='##':
            break
        print(data)

# 二级界面
def second(sock,name):
    while True:
        print("============= Query ==============")
        print("             1. 查单词             ")
        print("             2. 历史记录           ")
        print("             3. 注销               ")
        print("==================================")

        cmd = input("请输入命令:")
        if cmd == "1":
            do_query(sock,name)
        elif cmd == "2":
            do_history(sock,name)
        elif cmd == "3":
            return # 返回一级界面
        else:
            print("请输入正确命令:1, 2 or 3")

# 发送注册请求
def do_register(sock):

    name=input("Name:")
    passwd=input("Password:")
    passwd_=input("Password again:")

    # 两次密码要相同，名字和密码内不能有空格
    if passwd != passwd_ or " " in name or " " in passwd:
        print("用户名或密码错误")
        return

    msg="R %s %s"%(name,passwd)
    sock.send(msg.encode()) # 发送请求
    # 等结果
    result=sock.recv(128).decode()
    if result == "OK":
        print("注册成功")
    else:
        print("注册失败")

# 客户端启动函数
def do_login(sock):
    name=input("Name:")
    passwd=input("Password:")

    msg="L %s %s"%(name,passwd)
    sock.send(msg.encode()) #发送请求
    # 等待结果
    result=sock.recv(128).decode()
    if result=="OK":
        print("登录成功")
        second(sock,name) # 进入二级界面
    else:
        print("登录失败")

def main():
    # 创建tcp套接字
    sock=socket()
    sock.connect(ADDR)
    # 进入一级界面
    while True:
        print("============ Welcome ============= ")
        print("             1. 注册                ")
        print("             2. 登录                ")
        print("             3. 退出                ")
        print("================================== ")

        cmd = input("请输入命令:")
        sock.send(cmd.encode())
        if cmd == "1":
            do_register(sock)
        elif cmd == "2":
            do_login(sock)
        elif cmd == "3":
            sock.send(b"E")
            sys.exit("谢谢使用")
        else:
            print("请输入正确命令:1, 2 or 3")


if __name__ == '__main__':
    main()