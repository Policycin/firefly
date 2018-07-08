from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import datetime
from config import DevelopmentConfig
condev=DevelopmentConfig()
mongoIP=condev.MONGOIP
mongoPort=condev.MONGOPORT
db=MongoClient(mongoIP,port=mongoPort)
db = db.FireFly
for v in range(1,100):
    admin1={
        'username':'admin'+str(v),
        'email':'2148084512@qq.com',
        'activate':True,
        'password':generate_password_hash('123456'+str(v-1)),
        'is_super':0,
        'name':'Cin',
        'role_id':1,
        'addtime':datetime.datetime.utcnow()
    }
    # db.Admin.insert_one(admin1)

for v in range(1,100):
    tag={
        'name':'经济'+str(v),
        'addtime': datetime.datetime.utcnow()
    }
    # db.Tag.insert_one(tag)
with open(r"C:\\Users\\63163\\Desktop\\1.txt") as file:
    inf=file.readlines()
    stre=''
    for line in inf:
        line=line.strip()
        line=line.replace(" ","")
        # print(line)
        stre+=line
    # print(stre)
    content={
        'indexNum':'000014349/2017-00156',
        'fileType':'商贸、海关、旅游\对外经贸合作',
        'publisher':'国务院',
        'createTime':'2017年08月08日',
        'title':'国务院关于促进外资增长若干措施的通知',
        'fileNo':'国发〔2017〕39号',
        'PublishDate':'2017年08月16日',
        'addtime':datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        'path':'/',
       'tag':'对外开放',
        'url':'http://www.gov.cn/zhengce/content/2017-08/16/content_5218057.htm',
        'content':stre
    }
    # db.SoureFile.insert_one(content)

admin1 = {
    'username': 'admin',
    'email': '2148084512@qq.com',
    'activate': True,
    'password': generate_password_hash('1'),
    'is_super': 0,
    'name': 'Cin',
    'role_id': 1,
    'addtime': datetime.datetime.utcnow()
}
# db.Admin.insert_one(admin1)

sourefile=[("请选择国发文号","请选择国发文号")]
sourefilelist=db.SoureFile.find({})
for v in sourefilelist:
    sourefile.append((v['fileNo'],v['fileNo']))
print(type(sourefile[1][0]))