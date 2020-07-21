"""
关于二级界面问题
"""

def second():
    while True:
        print("============ 二级界面==============")
        print("***           查单词           ***")
        print("***           历史记录          ***")
        print("***           注销           ***")
        print("==================================")

        cmd = input("请输入命令:")
        if cmd == "单词":
            pass
        elif cmd == "注销":
            break
        else:
            print("请输入正确命令")


while True:
    print("============ 一级界面 ==============")
    print("***           登录           ***")
    print("***           注册           ***")
    print("***           退出           ***")
    print("==================================")

    cmd = input("请输入命令:")
    if cmd == "登录":
       second()
    elif cmd == "退出":
        break
    else:
        print("请输入正确命令")