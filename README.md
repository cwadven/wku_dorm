<h1 align="center">원클릭 외박신청</h1>

원광대학교 기숙사 원클릭 외박신청하기~!

<h3 align="center">웹페이지</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/wku_dorm/blob/master/assets/page1.PNG"/>
</p>

## 만들게된 계기

기숙사에서 살게 된다면 휴일 및 휴일 전날 제외하고, 기본적으로 평일 월~목요일은 밤 11시 30분에 `점호`라는 것을 한다.

`점호`를 받지 않으면 **벌점**을 받게되며 피치 못할 사정으로 `점호`를 못 받는 경우 `외박`이라는 시스템을 이용하여 학교 사이트에 접속하여 `외박` 신청을 당일 22:00 전에 신청을 해야한다.

이 `외박`을 신청하기 위해서 많은 절차를 걸쳐야하고, 귀찮아서 만들게 된 사이트다.

얼마나 많은 클릭을 및 과정을 거친 후, `외박`신청이 가능한지 아래 설명을 해놓았다.

## 외박신청 과정

<h3 align="center">1. 로그인</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/wku_dorm/blob/master/assets/step1.PNG"/>
</p>

<h3 align="center">2. 카테고리 선택</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/wku_dorm/blob/master/assets/step2.PNG"/>
</p>

<h3 align="center">3. 기숙사 정보 관리 선택</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/wku_dorm/blob/master/assets/step3.PNG"/>
</p>

<h3 align="center">4. 외박 정보 선택</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/wku_dorm/blob/master/assets/step4.PNG"/>
</p>

<h3 align="center">5. 외박 신청하기 선택</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/wku_dorm/blob/master/assets/step5.PNG"/>
</p>

<h3 align="center">6. 외박하기 위한 정보 입력 및 신청</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/wku_dorm/blob/master/assets/step6.PNG"/>
</p>

위의 과정을 보다시피 너무 많은 과정 및 시간을 소모한다는 사실을 알 것이다.

이것을 웹사이트를 구현하여 클릭 한번으로 만들기 위한 프로젝트를 진행하였다.

📢 추가 : `외박신청` 뿐만 아니라 `이번학기 성적 조회` 및 `졸업 진단`에 관한 것도 같이 이용할 수 있도록 만들었다.
🚧 주의 : `외박신청` 후에 생기는 외박신청 취소하기를 클릭할 경우 Heorku에서 session의 초과 때문에 문제가 생겨서 해당 작업은 안된다.

## 서비스 주소
**주소 :**<br>
http://wkudorm.herokuapp.com/
<br><br>

## 개발자

**👤 이창우**

- Github : https://github.com/cwadven
- Backend : Django
- Service : Heroku
- Server : Heroku 호스팅
- 기술스택 : Django, bs4, requests
- 개발기간 : <br>
    - 2019년 11월 19일 ~ 2019년 11월 23일 
    - 2020년 12월 18일 ~ 2020년 2월 12일 (유지보수)

## 환경 구축

~~~
1. python -m venv myvenv (가상환경 생성)
2. python source myvenv/Script/activates (가상환경 실행)
3. pip install -r requirements.txt (의존성 모듈 설치)
4. python manage.py collectstatic (static 파일 생성)
8. python manage.py migrate (세션 테이블 생성)
10. python manage.py runserver
~~~
