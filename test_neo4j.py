#coding=utf-8
import urllib,urllib2
from urllib import quote,unquote
import json
from py2neo import Graph,Node,Relationship
# from pandas import DataFrame

g = Graph(
    host = "0.0.0.0", # neo4j 搭载服务器的ip地址，ifconfig可获取到
    http_port = 7478, # neo4j 服务器监听的端口号
    user = "0", # 数据库user name，如果没有更改过，应该是neo4j
    password = "0" # 自己设定的密码
)

class selfException(BaseException):
    def __init__(self,mesg="raise a selfException"):
        print mesg

def insert_neo(lable,name,pname):
    c_node = Node(lable, name=name)
    p_node = Node(lable, name=pname)
    rel = Relationship(c_node, "ISA", p_node)
    g.merge(rel)


def main():
    insert_neo("Concept","儿子","父亲")
    insert_neo("Concept","儿子1", "父亲1")
    insert_neo("Concept","儿子2", "父亲2")
    node = g.data("Match (n:Concept) Return n.name Order by ID(n) desc Limit 1")
    print(node[0]["n.name"] )

main()
