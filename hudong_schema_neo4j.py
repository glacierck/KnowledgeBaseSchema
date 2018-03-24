#coding=utf-8
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib,urllib2
from urllib import quote,unquote
import urllib
import json
from lxml import etree

from py2neo import Graph,Node,Relationship

g = Graph(
    host = "0.0.0.0", # neo4j 搭载服务器的ip地址，ifconfig可获取到
    http_port = 7478, # neo4j 服务器监听的端口号
    user = "0", # 数据库user name，如果没有更改过，应该是neo4j
    password = "0" # 自己设定的密码
)

import pymongo
conn=pymongo.MongoClient()
db=conn['concept_project']

record_list=set()

def get_categories(url):
    data = urllib.urlopen(url).read()
    if len(data)>0:
        data = json.loads(data)
    return data
   
def check_child(p_name,p_id,content):
    if len(content) <1 :
        return 
    else:
       for item in content:
            name=item['name']
            _id=item['id']
            print name,_id,p_id,p_name
            pair=name+'_'+str(_id)+'_'+str(p_id)+'_'+p_name
            if pair not in record_list:
                record_list.add(pair)
                if p_name == name:
                    return 
                else:
                    # insert_db(name,_id,p_id,p_name)
                    insert_neo("Concept", name, p_name)
                    content = get_categories('http://fenlei.baike.com/category/Ajax_cate.jsp?catename=' + quote(name.encode('utf-8')))
                    check_child(name, _id, content)
                    
def insert_db(name,_id,p_id,p_name):
    data={}
    data['name']=name
    data['id']=_id
    data['p_id']=p_id
    data['p_name']=p_name
    db['hudong_concept'].insert(data)

def insert_neo(lable,name,pname):
    c_node = Node(lable, name=name)
    p_node = Node(lable, name=pname)
    rel = Relationship(c_node, "ISA", p_node)
    g.merge(rel)



def collect_categorys(start_name):
    url ='http://fenlei.baike.com/category/Ajax_cate.jsp?catename='+start_name.encode('utf-8')
    print(url)
    content=get_categories(url)
    print(content)
    _id = 0
    sum=0
    if len(content)>0:
        check_child(start_name,_id,content)

def main():
    node = g.data("Match (n:Concept) Return n.name Order by ID(n) desc Limit 1")
    last_objname = '页面总分类'
    if len(node)>0:
        last_objname = node[0]["n.name"];

    print(last_objname)
    collect_categorys(last_objname)

main()
# if __name__=="__main__":
#     count_words()
