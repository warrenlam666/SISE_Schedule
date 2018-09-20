from urllib import request,parse
from http import cookiejar
from bs4 import BeautifulSoup
import re
from icalendar import Calendar,Event
import hashlib
import datetime
def schedule(username, password, year=2018, semester=1, openday=20180903):
    """这是一个用于从sise学生系统导出ics格式日历的程序
    
    :param username: sise学生系统用户名，即学号，类型为str 如：'1740123321'
    :param password: sise学生系统密码，类型为str 如：'123456789'
    :param year: 要获取的课程表的年度，类型为int，如：2018
    :param semester: 要获取的课程表学期，值为1或2，类型为int，如1
    :param openday: 该年度的开学时间，类型为str型,如：'20180903'
    :return: 
    """""
    # 开学日期
    SchoolOpenday = ['', '', '']
    SchoolOpenday[0] = openday[0:4]
    SchoolOpenday[1] = openday[4:6]
    SchoolOpenday[2] = openday[6:8]

    # 定义星期缩写对照字典
    wk = {1: 'MO', 2: 'TU', 3: 'WE', 4: 'TH', 5: 'FR'}

    # 定义登陆页面的地址
    login_url = 'http://class.sise.com.cn:7001/sise/login_check_login.jsp'

    #定义一个变量用于计数
    class_count=0

    # 定义提交的数据form_data
    getHash = BeautifulSoup(request.urlopen("http://class.sise.com.cn:7001/sise/login.jsp").read().decode("GBK"),
                            features="lxml").select("input[type=hidden]")[0]
    form_data = {
        getHash['name']: getHash['value'],
        'username': username,
        'password': password
    }
    form_data = parse.urlencode(form_data).encode('UTF-8')

    # 定义提交头文件
    head = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://class.sise.com.cn:7001/sise/login.jsp',
        'Accept-Encoding': ' gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'

    }

    cookie = cookiejar.MozillaCookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cookie))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    res = request.Request(url=login_url, data=form_data);
    req1 = opener.open(res)
    print(req1.read().decode("GBK"))
    res2 = opener.open(
        'http://class.sise.com.cn:7001/sise/module/student_schedular/student_schedular.jsp?schoolyear={}&semester={}'.format(
            year, semester))
    soup = BeautifulSoup(res2.read().decode('GBK'), features='lxml')
    print(soup)
    all_day = soup.html.body.form.find_all('table', recursive=False)[4].find_all('tr')[1:10]  # 长度为8
    for i in range(0, 8):
        all_day[i] = all_day[i].find_all('td')[0:9]
    for i in range(0, 8):
        for j in range(0, 8):
            all_day[i][j] = all_day[i][j].get_text()

    # 生成ics文件


    # 输出上课时间段
    print('上课时间段如下：')
    for i in range(0, 8):
        print(all_day[i][0])
    print('***********************************************')
    cal = Calendar()
    # 添加文件头
    cal['PRODID'] = '-//Google Inc//Google Calendar 70.9054//EN'
    cal['VERSION'] = '2.0'
    cal['CALSCALE'] = 'GREGORIAN'
    cal['METHOD'] = 'PUBLISH'
    cal['X-WR-TIMEZONE'] = 'Asia/Shanghai'

    for i in range(0, 8):
        print(all_day[i][0])

        # 获取每节课的上课时间
        star_h = re.search('(?<=节).*?(?=\s-)', all_day[i][0]).group(0).split(':')[0]
        star_m = re.search('(?<=节).*?(?=\s-)', all_day[i][0]).group(0).split(':')[1]
        end_h = re.search('(?<=0\s-\s).*$', all_day[i][0]).group(0).split(':')[0]
        end_m = re.search('(?<=0\s-\s).*$', all_day[i][0]).group(0).split(':')[1]

        # print('上课时间{}时{}分，下课时间为{}时{}分'.format(star_h, star_m, end_h, end_m))
        for j in range(1, 6):
            # 判断该时间段是否有课，若有，则继续
            if len(all_day[i][j]) > 5:

                #考虑同一时间段出现多节课的可能
                for all_day[i][j] in str(all_day[i][j]).split(','):
                    # 由于每周五下午上课时间与其他时间不一样，故需特殊设置
                    if i == 3 and j == 5:
                        star_h = 13
                        star_m = 20
                        end_h = 14
                        end_m = 40
                    if i == 4 and j == 5:
                        star_h = 14
                        star_m = 50
                        end_h = 16
                        end_m = 10

                    print(all_day[i][j])

                    # 获取课程名称
                    class_name = re.search('(^.*)(?=\()', all_day[i][j]).group(0)
                    all_day[i][j] = all_day[i][j].replace(class_name, '')

                    # 获取课程代码及教师名称
                    teacher_name = re.search('(?<=\()(.*?)((?=\s\d))', all_day[i][j]).group(0).strip()
                    print(teacher_name)

                    # 获取课程的上课周
                    resq = re.search('(?<={}\s)(.*?)((?=周))'.format(teacher_name), all_day[i][j]).group(0).split(' ')
                    print(resq)
                    count = len(resq)
                    if (len(resq) == 1):
                        INTERVAL = 1
                    else:
                        INTERVAL = (int(resq[1]) - int(resq[0]))

                    # 获取课程所在周几
                    BYDAY = wk[j]

                    # 在ics中添加课程事件
                    event = Event()
                    # 添加课程开始时间
                    event.add('dtstart',
                              datetime.datetime(int(SchoolOpenday[0]), int(SchoolOpenday[1]),
                                                int(SchoolOpenday[2]) + (j - 1), int(star_h),
                                                int(star_m)) + datetime.timedelta(days=(int(resq[0]) - 1) * 7), 0)
                    # 添加课程结束时间
                    event.add('dtend',
                              datetime.datetime(int(SchoolOpenday[0]), int(SchoolOpenday[1]),
                                                int(SchoolOpenday[2]) + (j - 1), int(end_h),
                                                int(end_m)) + datetime.timedelta(days=(int(resq[0]) - 1) * 7), 0)

                    # 添加重复规则
                    event.add('1RRULE', 'FREQ=WEEKLY;COUNT={};INTERVAL={};BYDAY={}'.format(count, INTERVAL, BYDAY))
                    print(all_day[i][j])
                    print('课室:{}'.format(re.search('(?<=\[).*(?=\])', all_day[i][j]).group(0)))
                    print('课程名称：{}'.format(class_name))
                    # 添加课程教师名称及课程代码
                    event.add('DESCRIPTION',teacher_name)
                    print('教师名及课程代码：{}'.format(teacher_name))
                    # 添加课室位置
                    event.add('LOCATION', re.search('(?<=\[).*(?=\])', all_day[i][j]).group(0))
                    # 添加ics事件所需其他项
                    event.add('SEQUENCE', '0')
                    event.add('STATUS', 'CONFIRMED')
                    event.add('SUMMARY', class_name)
                    event.add('TRANSP', 'OPAQUE')
                    cal.add_component(event)
                    class_count += 1
                    print('***********************************************')
    f = open('{}-{}-{}.ics'.format(username,year,semester), 'w')
    new_str = cal.to_ical().decode('UTF-8')
    new_str = new_str.replace('1RRULE', 'RRULE')
    new_str = new_str.replace('\\', '')
    f.write(new_str)
    f.close()
    print('文件已成功导出到当前目录下！')
    print('ics包含课程数为{}'.format(class_count))