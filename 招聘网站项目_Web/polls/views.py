from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators import csrf
import sys
from matplotlib.pyplot import eventplot
import pandas as pd

# post主页面


def show_main_page(request):
    f = open("./pythons/city_tuple.txt")
    dlist = dict(eval(f.read()))
    f.close()
    log = open("./pythons/log.txt", "w")
    log.write("^")
    log.close()
    return render(request, './main/招聘网站数据分析.html', dlist)


def test(request):
    ctx = {}
    if request.POST:
        ctx['city'] = request.POST['city']
        ctx['job'] = request.POST['job']
    return render(request, 'temp.html', ctx)


# 搜索按钮
def search_button(request):
    sys.path.append('..')
    ctx = {}
    city = request.POST['city']
    job = request.POST['job']
    # if (city and job):
    #     ctx = {}
    #     ctx['event_content'] = "输入框中信息错误，请确保输入正确！"
    #     return render(request, './event_raise.html', ctx)
    ctx['city'] = city
    ctx['job'] = job
    log = open("./pythons/log.txt", "w")
    log.write(city + '^' + job)
    log.close()
    try:
        string = "./database/" + job + '.jpg'
        jpg = open(string)
        jpg.close()
        path = string = "../database/" + job + '.jpg'
        return render(request, './wordcloud/canvas.html', {'wordcloud': path})
    except FileNotFoundError:
        return render(request, './event_raise.html',
                      {'event_content': '数据库中无此信息,请点击更新数据库按钮更新！'})


def craw(request):
    from pythons import Data_analysis as da
    from pythons import Recrawler as rc
    f = open("./pythons/log.txt")
    log = f.read()
    log = log.split('^')
    if log[1] and log[0]:
        da.general_func(log[1], log[0], filename=log[1],
                        num=20, path="./database/")
        return render(request, './jump.html')
    else:
        ctx = {}
        ctx['event_content'] = "输入框中信息错误，请确保输入正确！"
        return render(request, './event_raise.html', ctx)


def show_wordcloud(request):
    sys.path.append('..')
    f = open("./pythons/log.txt")
    log = f.read()
    log = log.split('^')
    job = log[1]
    try:
        string = "./database/" + job + '.jpg'
        jpg = open(string)
        jpg.close()
        path = string = "../database/" + job + '.jpg'
        return render(request, './wordcloud/canvas.html', {'wordcloud': path})
    except FileNotFoundError:
        return render(request, './event_raise.html',
                      {'event_content': '数据库中无此信息,请点击更新数据库按钮更新！'})


# 图表页面内的四个图表
def show_cpny_wordcloud(request):
    sys.path.append('..')
    f = open("./pythons/log.txt")
    log = f.read()
    log = log.split('^')
    job = log[1]
    try:
        string = "./database/" + job + 'jobwc.jpg'
        jpg = open(string)
        jpg.close()
        path = string = "../database/" + job + 'jobwc.jpg'
        return render(request, './salary/canvas.html', {'plot': path, 'title': '公司经营方向词云图'})
    except FileNotFoundError:
        return render(request, './event_raise.html',
                      {'event_content': '数据库中无此信息,请点击更新数据库按钮更新！'})


def show_barplot(request):
    sys.path.append('..')
    f = open("./pythons/log.txt")
    log = f.read()
    log = log.split('^')
    job = log[1]
    try:
        string = "./database/" + job + 'edu.png'
        jpg = open(string)
        jpg.close()
        path = string = "../database/" + job + 'edu.png'
        return render(request, './salary/canvas.html', {'plot': path, 'title': '职位学历要求柱状图'})
    except FileNotFoundError:
        return render(request, './event_raise.html',
                      {'event_content': '数据库中无此信息,请点击更新数据库按钮更新！'})

def show_bubble(request):
    sys.path.append('..')
    f = open("./pythons/log.txt")
    log = f.read()
    log = log.split('^')
    job = log[1]
    try:
        string = "./database/" + job + 'bub.png'
        jpg = open(string)
        jpg.close()
        path = string = "../database/" + job + 'bub.png'
        return render(request, './salary/canvas.html', {'plot': path, 'title': '公司薪酬气泡图'})
    except FileNotFoundError:
        return render(request, './event_raise.html',
                      {'event_content': '数据库中无此信息,请点击更新数据库按钮更新！'})

def show_boxplot(request):
    sys.path.append('..')
    f = open("./pythons/log.txt")
    log = f.read()
    log = log.split('^')
    job = log[1]
    try:
        string = "./database/" + job + 'slry.png'
        jpg = open(string)
        jpg.close()
        path = string = "../database/" + job + 'slry.png'
        return render(request, './salary/canvas.html', {'plot': path, 'title': '热门城市薪资图'})
    except FileNotFoundError:
        return render(request, './event_raise.html',
                      {'event_content': '数据库中无此信息,请点击更新数据库按钮更新！'})


def show_form(request):
    sys.path.append('..')
    f = open("./pythons/log.txt")
    log = f.read()
    log = log.split('^')
    job = log[1]
    try :
        df = pd.read_csv('./database/'+ job +'.csv', encoding='gbk')
        data = df.values[:, :]
        dlist = []
        for line in data:
            ls = []
            for j in line:
                ls.append(j)
            dlist.append(ls)
        return render(request, './form/canvas.html', {'dlist': dlist})
    except FileNotFoundError:
        return render(request, './event_raise.html',
                      {'event_content': '数据库中无此信息,请点击更新数据库按钮更新！'})


def show_intro(request):
    return render(request, './intro/canvas.html')