from django.shortcuts import render
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Create your views here.
def home(request):
    if request.method == 'POST':
        userid = request.POST.get("username")
        passwd = request.POST.get("password")
        reasons = request.POST.get("reasons", "공부")

        login_url = 'https://auth.wku.ac.kr/Cert/User/Login/login.jsp'
       
        session = requests.session()

        data = {
            'nextURL': 'http://intra.wku.ac.kr/SWupis/V005/loginReturn.jsp',
            'userid': str(userid),
            'passwd': str(passwd),
        }

        try:
            res = session.post(login_url, data=data)
        except: # 인터넷 안됬을 경우 예외처리!
            content = {
                "doned":"인터넷 오류입니다!",
                "id":userid,
                "pw":passwd
            }
            return render(request, 'home.html', content)

        res.raise_for_status() 

        first_url = 'http://intra.wku.ac.kr/'

        res = session.get(first_url)
            
        login_return = 'http://intra.wku.ac.kr/SWupis/V005/loginReturn.jsp' #리턴 해야되더라...

        r = session.get(login_return)

        # 응답코드가 200 즉, OK가 아닌 경우 에러를 발생시키는 메서드입니다.
        r.raise_for_status()
        # 요청할 데이터
        if request.method == 'POST' and "score" in request.POST: #성적 확인 소스코드 if랑 밑에 있는 Else 지우고 if 안에 있는 녀석 다 지우고 html에 가서 home에서 submit 하나더 지우면 끝
            sorce_3 = 'https://intra.wku.ac.kr/SWupis/V005/Service/Stud/Score/scoreTable.jsp?sm=3'
            r = session.get(sorce_3)
            doned = "성적 확인<br><br>"
        else:
            apply_dorm = 'https://intra.wku.ac.kr/SWupis/V005/CommonServ/dormitory/stud/dormAction.jsp'

            now = datetime.now()
            today_year = str(now.year)

            time1 = datetime(int(now.year), int(now.month), int(now.day), 22, 00, 1) #10시 이후에는 불가능!
            time2 = datetime(int(now.year), int(now.month), int(now.day), 23, 59, 59) #10시 이후에는 불가능!

            if(len(str(now.month))==1): #now.month를 하면 1,2,3, 형식으로 나오는데 넣는 곳은 01, 02로 해야되서 데이터 가공
                today_month = "0" + str(now.month)
            else: 
                today_month = str(now.month)

            if(len(str(now.day))==1): #now.day를 하면 1,2,3, 형식으로 나오는데 넣는 곳은 01, 02로 해야되서 데이터 가공
                today_day = "0" + str(now.day)
            else:
                today_day = str(now.day)
            #-*- coding: euc-kr -*-
            data = { #데이터를 이렇게 보내겠다!
                'ContextPath': 'goOutList.jsp',
                'Process': 'goOutApply',
                'outDate': str(today_year) + str(today_month) + str(today_day), #오늘 날짜 내기!
                'reason': reasons.encode('euc-kr'),
                'location': '기숙사'.encode('euc-kr'),
                'emgTel': '010-0000-0000'
            }

            if datetime.now() > time1 and datetime.now() < time2: #10시 이후에는 불가능!
                doned = "22시 이후에는 불가능 합니다!!<br>다음날 기달리세요!<br><br>"
            elif datetime.now().isoweekday() == 6 or datetime.now().isoweekday() == 7: #주말에 안되게 만들기
                doned = "주말은 불가능 해요!<br><br>"
            else: #정상 처리 됬을 경우 apply_dorm에 데이터를 실어서 POST한다
                r = session.post(apply_dorm, data=data)
                r.raise_for_status()
                doned = "완료되었습니다!<br><br>"
                request.session['userid'] = userid
                request.session['passwd'] = passwd

            ##오류 나거나 했을 경우 어떤 오류인지 보여주게 bs4이용해서 그 내용 보여주기!
            #혹은 됬는지 확인 하기 위해서 보여주기

            check_dorm = 'https://intra.wku.ac.kr/SWupis/V005/CommonServ/dormitory/stud/goOutList.jsp'

            r = session.get(check_dorm)

        soup = BeautifulSoup(r.text, 'html.parser') #html로 되어있는 소스코드를 박아 버린다


        he_coin = soup.find_all('table') #크롤링을 해서 "table" 태그를 가진 친구들만 가져온다!
        he_coin = str(he_coin) #글로 바꾸기!
        
        if len(he_coin) == 0: #로그인 정보가 이상하면 he_coin 즉 table 태그를 가진 친구를 찾을 수가 없어서 길이가 0임!
            he_coin = "[회원 정보가 없습니다!]"
            doned = ""
            request.session['userid'] = "NONE"
            request.session['passwd'] = "NONE"
        else:
            pass

        return render(request, 'home.html', {"error_check":he_coin[1:-1], "doned":doned})# table을 크롤링을 통해서 가져오면 양 끝에 "[]"이 친구들이 남아서 없애려고! he_coin[1:-1]
    return render(request, 'home.html')

def delete(request):
    if request.method == 'POST':
        if request.session.get('userid','NONE') == 'NONE': #예외처리를 위해서 어떠한 경우 이렇게 만들기! 즉 seesion 값이 중간에 사라졌을 경우!
            he_coin = "[회원 정보가 없습니다!<br>로그인 후 이용하세요]"
            doned = ""
            return render(request, 'home.html', {"error_check":he_coin[1:-1], "doned":doned})

        login_url = 'https://auth.wku.ac.kr/Cert/User/Login/login.jsp'
        #아에 alert에서 막혀버림....
        session = requests.session()

        data = {
            'nextURL': 'http://intra.wku.ac.kr/SWupis/V005/loginReturn.jsp',
            'userid': str(request.session.get('userid','NONE')),
            'passwd': str(request.session.get('passwd','NONE')),
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

        now = datetime.now()
        today_year = str(now.year)

        time1 = datetime(int(now.year), int(now.month), int(now.day), 22, 00, 1) #10시 이후에는 불가능!
        time2 = datetime(int(now.year), int(now.month), int(now.day), 23, 59, 59) #10시 이후에는 불가능!

        if(len(str(now.month))==1):
            today_month = "0" + str(now.month)
        else:
            today_month = str(now.month)

        if(len(str(now.day))==1):
            today_day = "0" + str(now.day)
        else:
            today_day = str(now.day)

        delete_reservation = "http://intra.wku.ac.kr/SWupis/V005/CommonServ/dormitory/stud/dormAction.jsp"
        
        data = {
            "ContextPath": "goOutList.jsp",
            "Process": "goOutDelete",
            "outDate": str(today_year) + str(today_month) + str(today_day),
            "reason": "(unable to decode value)",
            "location": "(unable to decode value)",
            "emgTel": "010-0000-0000"
        }

        r = session.post(delete_reservation, data=data)
        soup = BeautifulSoup(r.text, 'html.parser') #html로 되어있는 소스코드를 박아 버린다
        script = soup.find("script").extract() #메시지창 떳을 경우 예외처리하기

        # find all alert text
        alert = re.findall(r'(?<=alert\(\").+(?=\")', script.text) #메시지창 떳을 경우 예외처리하기
        
        if str(alert[0]) == "외박신청 취소 중 오류가 발생하였습니다.": #메시지창 떳을 경우 예외처리하기
            doned = "취소중 오류가 생겼습니다<br><br>" #메시지창 떳을 경우 예외처리하기
        else:
            doned = "취소가 완료되었습니다!<br><br>" #메시지창 떳을 경우 예외처리하기


        check_dorm = 'https://intra.wku.ac.kr/SWupis/V005/CommonServ/dormitory/stud/goOutList.jsp' #크롤링 해서 밑에 보여주기 위해서 아래 전부 크롤링

        r = session.get(check_dorm)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser') #html로 되어있는 소스코드를 박아 버린다

        he_coin = soup.find_all('table')

        he_coin = str(he_coin)

        return render(request, 'home.html', {"error_check":he_coin[1:-1], "doned":doned})
