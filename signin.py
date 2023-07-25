import requests
import json
import pickle
import datetime
from DingDingBot import DDBOT
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; E6883 Build/32.4.A.1.54; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36',   
    'Referer':'https://www.t00ls.com/members-profile-12894.html'
}
logindata = {}
robots_url = "https://oapi.dingtalk.com/robot/send?access_token=修改token"
dd = DDBOT.DingDing(
    webhook=robots_url)


# questionid
# 1 母亲的名字
# 2 爷爷的名字
# 3 父亲出生的城市
# 4 您其中一位老师的名字
# 5 您个人计算机的型号
# 6 您最喜欢的餐馆名称
# 7 驾驶执照的最后四位数字

def login(session):
    loginurl="https://www.t00ls.com/login.json"
    response=session.post(url=loginurl,data=logindata,headers=headers)
    responsejson=json.loads(response.text)
    try:
        return responsejson["status"],responsejson["formhash"]
    except:
        return "login_error"

# def cookielogin(session):
#     singurl="https://www.t00ls.com/ajax-sign.json"
#     signdata={
#     "signsubmit":"true"
#     }
#     with open('cookiefile', 'rb') as fn:
#         session.cookies.update(pickle.load(fn))
#     formhashpage=session.post(url=singurl,data=signdata,headers=headers).text
#     if(formhashpage.find(logindata["username"])>0):
#         result="success"
#         mark=formhashpage.find("formhash=")
#         formhash=formhashpage[mark+9:mark+9+8]
#         return result,formhash
#     else:
#         return "fail"

def signin(session,formhash):
    singurl="https://www.t00ls.com/ajax-sign.json"
    signdata={
    "formhash":"",
    "signsubmit":"true"
    }

    print(formhash)
    signdata["formhash"]=formhash
    response=session.post(url=singurl,data=signdata,headers=headers)
    #print(response.text)
    try:
        result=json.loads(response.text)["message"]
        print(result)       #出现success为签到成功，alreadysign为已经签到过
        return result
    except:
        print("Error,please give me issue")
        return "Error,please give me issue"



def dingding_push(msg):
    creent_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dd.Send_Text_Msg(f"{msg}\n{creent_time}")

def logwrite(result):
    fn=open("log.txt",'a')
    time=datetime.datetime.now()
    fn.write(str(time)+"    :   "+result+"\n")
    fn.close()


if __name__ == '__main__':
    user = "";
    password = "";
    questionid = "";
    answer = ""
    with open(r"./user.conf","r",encoding="utf-8") as config:
        for conf in config:
            conf_list = conf.replace("\n","").split("||")
            for field in conf_list:
                key = field.split("=")[0]
                value = field.split("=")[1]
                if key == "user":
                    user = value
                elif key == "password":
                    password = value
                elif key == "questionid":
                    questionid = value
                elif key == "answer":
                    answer = value
            logindata = {
                "action": "login",
                "username": f"{user}",  # 填你的用户名，不要填ID
                "password": f"{password}",  # 密码的MD5值
                "questionid": int(f"{questionid}"),  # 问题编号，对照下面注释填写，若没有设置提问则此处随便填写
                "answer": f"{answer}"  # 输入回答，若没有设置提问则此处随便填写，或不填
            }
            session = requests.session()
            try:
                login_result, formhash = login(session)
                print(login_result)
                if login_result == "success":
                    print("[+] 登入成功")
                    result = signin(session, formhash)
                    if result == "success":
                        dingding_push(f"😍签到成功😍 {logindata['username']}")
                        logwrite(f"{logindata['username']} 签到成功")
                    elif result == "alreadysign":
                        if time.localtime().tm_hour != 15:
                            dingding_push(f"👌签到过了👌 {logindata['username']}")
                            logwrite(f"alreadysign {logindata['username']}")
                else:
                    print("[+] 登入失败")
                    dingding_push(f"😭签到失败😭 {logindata['username']}")
            except:
                print("[!] 出现异常")
                dingding_push(f"😭签到失败😭 {logindata['username']}")
                logwrite(f"签到失败 {logindata['username']}")


