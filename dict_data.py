"""
连接数据库 dict:

创建user表
    user: 用户名   密码

create table user (id int primary key auto_increment,
name varchar(30),
passwd char(64));

创建history表
        history:单词  时间  user_id

create table history(id int primary key auto_increment,
word varchar(30),
time datetime default now(),
user_id int,
foreign key(user_id) references user(id));
"""
import pymysql

# 准备工作，建立与数据库的连接
class Database:
    def __init__(self):
        self.db = pymysql.connect(user="root",
                                  password="123456",
                                  database="dict",
                                  charset="utf8")
    # 每个进程各自创建游标
    def create_cursor(self):
        self.cursor=self.db.cursor()

    def close(self):
        self.db.close()

# 专门为server端提供它所需的数据方法
class DataHandle(Database):

    # 处理server端的注册诉求
    def register(self,name,passwd):
        # 判断用户是否存在
        sql = "select name from user where name=%s;"
        self.cursor.execute(sql,[name])
        r=self.cursor.fetchone() # 查看结果
        # 查询到结果，返回FALSE
        if r:
            return False
        # 可以注册，插入用户信息
        sql = "insert into user (name,passwd) values (%s,%s);"
        try:
            self.cursor.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 登录验证
    def login(self,name,passwd):
        sql = "select name from user where name=%s and passwd=%s;"
        self.cursor.execute(sql,[name,passwd])
        r=self.cursor.fetchone() # 查看结果
        # 查询到结果，返回True
        if r:
            return True
        else:
            return False

    # 查询单词
    def query(self,word)->str:
        """
                :param word: 要查询的单词
                :return: str 查询得到的解释  or Not Found
                """
        sql = "select mean from words where word=%s;"
        self.cursor.execute(sql, [word])
        result = self.cursor.fetchone()  # 查询结果：返回元组 (mean,) 或 None
        if result:
            return result[0]  # 返回元组的 (mean,)
        else:
            return "Not Found"

    # 历史记录
    def history(self,name,word):
        sql = "select id from user where name=%s;"
        self.cursor.execute(sql,[name])
        user_id=self.cursor.fetchone()[0]
        sql ="insert into history (word,user_id) values (%s,%s);"
        try:
            self.cursor.execute(sql,[word,user_id])
            self.db.commit()
        except:
            self.db.rollback()

    # 查询历史记录
    def query_history(self,name):
        # name  word    time
        sql = "select name,word,time from user inner join history " \
              "on user.id=history.user_id where name=%s order by time desc limit 10;"
        self.cursor.execute(sql,[name])
        return self.cursor.fetchall() # fetchall() 返回元组套元组：((name,word,time),(),()...)

