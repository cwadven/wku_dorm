from django.shortcuts import render
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Create your views here.
def home(request):
    if request.method == 'POST':
        userid = request.POST.get("username")
        passwd = request.POST.get("password")

        login_url = 'https://auth.wku.ac.kr/Cert/User/Login/login.jsp'
        #아에 alert에서 막혀버림....
        session = requests.session()

        data = {
            'nextURL': 'http://intra.wku.ac.kr/SWupis/V005/loginReturn.jsp',
            'userid': str(userid),
            'passwd': str(passwd),
        }

        res = session.post(login_url, data=data)

        res.raise_for_status() 

        first_url = 'http://intra.wku.ac.kr/'

        res = session.get(first_url)
            
        login_return = 'http://intra.wku.ac.kr/SWupis/V005/loginReturn.jsp' #리턴 해야되더라...

        r = session.get(login_return)

        # 응답코드가 200 즉, OK가 아닌 경우 에러를 발생시키는 메서드입니다.
        r.raise_for_status()
        # 요청할 데이터

        apply_dorm = 'https://intra.wku.ac.kr/SWupis/V005/CommonServ/dormitory/stud/dormAction.jsp'

        now = datetime.now()
        today_year = str(now.year)

        time1 = datetime(int(now.year), int(now.month), int(now.month), 22, 00, 1) #10시 이후에는 불가능!
        time2 = datetime(int(now.year), int(now.month), int(now.month), 23, 59, 59) #10시 이후에는 불가능!

        if(len(str(now.month))==1):
            today_month = "0" + str(now.month)
        else:
            today_month = str(now.month)

        if(len(str(now.day))==1):
            today_day = "0" + str(now.day)
        else:
            today_day = str(now.day)

        data = {
            'ContextPath': 'goOutList.jsp',
            'Process': 'goOutApply',
            'outDate': str(today_year) + str(today_month) + str(today_day), #오늘 날짜 내기!
            'reason': 'study',
            'location': 'dormitory',
            'emgTel': '010-0000-0000'
        }

        if datetime.now() > time1 and datetime.now() < time2:
            doned = "10시 이후에는 불가능 합니다!! 다음날 기달리세요!"
        else:
            r = session.post(apply_dorm, data=data)
            r.raise_for_status()
            doned = "완료되었습니다!"

        ##오류 나거나 했을 경우 어떤 오류인지 보여주게 bs4이용해서 그 내용 보여주기!
        #혹은 됬는지 확인 하기 위해서 보여주기

        check_dorm = 'https://intra.wku.ac.kr/SWupis/V005/CommonServ/dormitory/stud/goOutList.jsp'

        r = session.get(check_dorm)

        soup = BeautifulSoup(r.text, 'html.parser') #html로 되어있는 소스코드를 박아 버린다


        he_coin = soup.find_all('table')
        aa = he_coin

        he_coin = str(he_coin)
        
        if len(aa) == 0:
            he_coin = "[회원 정보가 없습니다!]"
            doned = ""
        else:
            doned = "완료되었습니다!"
            pass

        return render(request, 'home.html', {"error_check":he_coin[1:-1], "doned":doned})

    return render(request, 'home.html')