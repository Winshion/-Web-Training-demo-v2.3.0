import pandas as pd
from pythons import Data_analysis as da
import wordcloud
import jieba
import time
import matplotlib.pyplot as plt
import matplotlib
import os

# 该函数进行词云图的生成


def format_word_cloud(job, text, path, encoding='utf-8'):
    """
    该函数进行云图的生成。传入文本，系统将自动生成云图对象。
    使用结巴分词库先分词，后存入文本
    """
    proc = jieba.cut(text)  # proc是处理后的文本迭代对象
    cloud_txt = ''
    for each in proc:
        cloud_txt += (' ' + each)
    wc = wordcloud.WordCloud(width=1100, height=650, max_words=366, scale=2, colormap="Pastel1",
                             background_color='#777777', font_path='./fonts/STZHONGS.TTF')
    wc.generate(cloud_txt)
    path = path + job + '.jpg'
    picture = wc.to_image()
    wc.to_file(path)


# 以下的函数群完成热门城市薪资箱线图的描绘

def salary_lst_filter(job_csv):
    """
    筛选数据，要么是千/月，要么是万/月
    然后再进行数据的处理
    画出城市的箱线图
    """
    min_lst = []
    max_lst = []
    new_city_lst = []
    city_lst = job_csv['城市']
    lst = [str(each) for each in job_csv['薪酬']]
    for salary in range(len(lst)):
        if lst[salary] == 'nan':
            continue
        elif ("千/月" not in lst[salary]) and ('万/月' not in lst[salary]):
            continue
        else:
            lst[salary] = lst[salary].split("-")
            min_lst.append(lst[salary][0])
            max_lst.append(lst[salary][1])
            new_city_lst.append(city_lst[salary])
    return min_lst, max_lst, new_city_lst


def process_salary_lst(job_csv):
    min_slr, max_slr, city_lst = salary_lst_filter(job_csv)
    final_min = [float(each) for each in min_slr]
    # 接下来处理max_list的内容
    final_max = [float(each[:-3]) for each in max_slr]
    for value in range(len(final_max)):
        if max_slr[value][-3] == '万':
            final_min[value] *= 10
            final_max[value] *= 10
    return final_min, final_max, city_lst


def give_complete_data(job_csv):
    mil, mal, cty = process_salary_lst(job_csv)
    avrgl = []  # 平均薪资列表
    for each in range(len(mil)):
        avrgl.append(0.5 * (mil[each] + mal[each]))
        cty[each] = cty[each][:2]
    return avrgl, cty


def get_city_lst(job_csv):
    """
    按照城市分配数据
    """
    avrg, cty = give_complete_data(job_csv)
    #   北京 上海  广州  深圳  杭州 南京  武汉  长沙  重庆 成都  厦门
    BJ = []
    SH = []
    GZ = []
    SZ = []
    HZ = []
    NJ = []
    WH = []
    CS = []
    CQ = []
    CD = []
    XM = []
    for value in range(len(avrg)):
        if cty[value] == '北京':
            BJ.append(avrg[value])
        elif cty[value] == '上海':
            SH.append(avrg[value])
        elif cty[value] == '广州':
            GZ.append(avrg[value])
        elif cty[value] == '深圳':
            SZ.append(avrg[value])
        elif cty[value] == '杭州':
            HZ.append(avrg[value])
        elif cty[value] == '南京':
            NJ.append(avrg[value])
        elif cty[value] == '武汉':
            WH.append(avrg[value])
        elif cty[value] == '长沙':
            CS.append(avrg[value])
        elif cty[value] == '重庆':
            CQ.append(avrg[value])
        elif cty[value] == '成都':
            CD.append(avrg[value])
        elif cty[value] == '厦门':
            XM.append(avrg[value])
    return BJ, SH, GZ, SZ, HZ, NJ, WH, CS, CQ, CD, XM


def store_plot(job_csv, job):
    BJ, SH, GZ, SZ, HZ, NJ, WH, CS, CQ, CD, XM = \
        get_city_lst(job_csv)
    fonts = matplotlib.font_manager.FontProperties(
        fname='./fonts/STZHONGS.TTF', size=12)
    plt.figure(figsize=(8, 4))
    plt.boxplot([BJ, SH, GZ, SZ, HZ, NJ, WH, CS, CQ, CD, XM],
                labels=['北京', '上海', '广州', '深圳', '杭州',
                        '南京', '武汉', '长沙', '重庆', '成都',
                        '厦门'])
    plt.xticks(fontproperties=fonts, fontsize=8)
    plt.title(job + "岗位全国热门城市薪资水平：千元/月", fontproperties=fonts)
    plt.savefig("./database/" + job + 'slry' + '.png', dpi=250)


# 学历要求柱状图的存储
def education_plot(job_csv, job):
    edu_lst = list(job_csv['学历要求'])
    x_axis = ["初中", "中专", "中技", "高中", "本科", "大专", "硕士", "博士"]
    y_axis = []
    colors = ["red", "orange", "yellow", "green",
              "cyan", "skyblue", "blue", "purple"]
    for each in x_axis:
        y_axis.append(edu_lst.count(each))
    fonts = matplotlib.font_manager.FontProperties(
        fname='./fonts/STZHONGS.TTF', size=12)
    plt.figure(figsize=(8, 4))
    plt.bar(x_axis, y_axis, color=colors)
    plt.title(job + "岗位学历要求柱状图", fontproperties=fonts)
    plt.xticks(fontproperties=fonts, fontsize=8)
    plt.savefig("./database/" + job + 'edu' + '.png', dpi=250)


# 以下函数群用于处理公司类型、公司规模与薪酬均值之间的关系
def bubble_lst_filter(job_csv):
    """
    筛选数据，要么是千/月，要么是万/月
    然后再进行数据的处理
    画出城市的箱线图
    """
    min_lst = []
    max_lst = []
    new_cpny_lst = []
    new_scale_lst = []
    cpny_lst = job_csv['公司类型']
    scale_lst = job_csv['公司规模（人）']
    lst = [str(each) for each in job_csv['薪酬']]
    for salary in range(len(lst)):
        if lst[salary] == 'nan':
            continue
        elif ("千/月" not in lst[salary]) and ('万/月' not in lst[salary]):
            continue
        else:
            lst[salary] = lst[salary].split("-")
            min_lst.append(lst[salary][0])
            max_lst.append(lst[salary][1])
            new_cpny_lst.append(cpny_lst[salary])
            new_scale_lst.append(scale_lst[salary])
    return min_lst, max_lst, new_cpny_lst, new_scale_lst


def process_bubble_lst(scale_lst):
    return_lst = []
    temp_lst = []
    for each in scale_lst:
        each = str(each)
        each = each.replace('人', '')
        each = each.replace('少于', '')
        each = each.replace('以上', '')
        temp_lst.append(each)
    for each in temp_lst:
        if each != 'nan':
            each = each.split('-')
            for i in range(len(each)):
                each[i] = int(each[i])
            return_lst.append(0.5*sum(each))
        else:
            return_lst.append(0)
    return return_lst


def process_salary_lst2(job_csv):
    min_slr, max_slr, new_cpny_lst, new_scale_lst = bubble_lst_filter(job_csv)
    new_scale_lst = process_bubble_lst(new_scale_lst)
    final_min = [float(each) for each in min_slr]
    # 接下来处理max_list的内容
    final_max = [float(each[:-3]) for each in max_slr]
    for value in range(len(final_max)):
        if max_slr[value][-3] == '万':
            final_min[value] *= 10
            final_max[value] *= 10
    return final_min, final_max, new_cpny_lst, new_scale_lst


def give_bubble_data(job_csv):
    mil, mal, cpny, scale = process_salary_lst2(job_csv)
    avrgl = []  # 平均薪资列表
    for each in range(len(mil)):
        avrgl.append(0.5 * (mil[each] + mal[each]))
    return avrgl, cpny, scale


def format_bubble_plot(job_csv, job):
    """绘制气泡图并保存到数据库中"""
    avr, cpny, scale = give_bubble_data(job_csv)
    # 处理公司类型
    cpny_dict = {}
    slry_dict = {}
    scale_dict = {}
    i = 0  # 计数
    for each in cpny:
        cpny_dict[each] = cpny_dict.get(each, 0) + 1
        slry_dict[each] = slry_dict.get(each, 0) + avr[i]
        scale_dict[each] = scale_dict.get(each, 0) + scale[i]
        i += 1
    # 计算薪酬和规模的均值
    for each in cpny_dict.keys():
        slry_dict[each] /= cpny_dict[each]
        scale_dict[each] /= cpny_dict[each]
    x = list(scale_dict.values())
    y = list(slry_dict.values())
    ss = [i*30 for i in cpny_dict.values()]
    txt = list(scale_dict.keys())
    fonts = matplotlib.font_manager.FontProperties(
        fname='./fonts/STZHONGS.TTF', size=12)
    plt.figure(figsize=(8, 4))
    plt.scatter(x, y, s=ss, c=list(cpny_dict.values()),
                cmap="prism", marker=(150, 0, 15), alpha=0.5)
    for i in range(len(x)):
        plt.annotate(txt[i], xy=(x[i], y[i]), xytext=(x[i], y[i]),
                     fontproperties=fonts)
    plt.xlabel("公司规模/人", fontproperties=fonts)
    plt.ylabel("公司薪酬（千元/月）", fontproperties=fonts)
    plt.title(job + "岗位气泡图", fontproperties=fonts)
    plt.savefig("./database/" + job + 'bub' + '.png', dpi=250)

    # 进行公司经营方向词云图的构建

def format_dir_wordcloud(job_csv, job):
    wc_txt = ""
    dir_lst = list(job_csv['公司经营方向'])
    for each in dir_lst:
        each = each.split('/')
        for i in each:
            wc_txt = wc_txt + ' ' + i
    wc = wordcloud.WordCloud(width=1100, height=650, max_words=366, scale=2, colormap="Pastel2",
                             background_color='#777777', font_path='./fonts/STZHONGS.TTF')
    wc.generate(wc_txt)
    path = './database/' + job + 'jobwc.jpg'
    wc.to_file(path)
