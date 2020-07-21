"""
创建一个数据库dict
里面创建一个数据表words
id   word  mean
讲dict.txt单词本中的所有单词和解释插入到对应数据库字段中

create table words (id int primary key auto_increment,
word char(30),
mean varchar(256));
"""
import re
import pymysql

# 打开单词本
f = open("dict.txt")

# 装单词 [(word,mean),(),()] -> executemany
args_list = []
for line in f:
    # result --> [(work,mean)]
    result = re.findall(r"(\w+)\s+(.*)",line)
    args_list.append(result[0])
f.close()

# 连接数据库 (连接自己计算机可以不写host port)
db = pymysql.connect(
                     user='root',
                     password='123456',
                     database='dict',
                     charset='utf8'
                     )

# 创建游标 (游标对象负责调用执行sql语句，操作数据，得到结果)
cur = db.cursor()

# 对数据库写操作
try:
    sql = "insert into words (word,mean) values (%s,%s);"
    cur.executemany(sql,args_list)
    db.commit() # 提交，将sql语句的操作行为提交写入到数据库
except Exception as e:
    print(e)
    db.rollback() # 没有提交到数据库的内容，全部失效


# 关闭游标和数据库
cur.close()
db.close()
