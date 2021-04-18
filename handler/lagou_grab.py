import requests
import json
import time
from handler import const
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from store.image_store import uploadImage
from store.db import InsertBoard

URL = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'
HEADERS = {
    "Host": "www.lagou.com",
    "Connection": "keep-alive",
    "Content-Length": "26",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
    "X-Anit-Forge-Code": "0",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "X-Anit-Forge-Token": "None",
    "Origin": "https://www.lagou.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.lagou.com/jobs/list_c%2B%2B?labelWords=&fromSearch=true&suginput=",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "user_trace_token=20210417232416-28079fbe-cf9c-424b-a350-15dc6e287713; _ga=GA1.2.1599759225.1618673059; LGUID=20210417232417-e014dc6b-cf39-46aa-ab78-78b9391d62bf; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1618673058,1618673074; JSESSIONID=ABAAABAABEIABCI7D63C905ED78B0D8BC6649F7214F109B; WEBTJ-ID=20210417%E4%B8%8B%E5%8D%8811:24:42232442-178e06f1eeb7c-0bc5219c581b96-d7e1938-2073600-178e06f1eec94d; RECOMMEND_TIP=true; privacyPolicyPopup=false; _gid=GA1.2.681480259.1618673082; sensorsdata2015session=%7B%7D; __lg_stoken__=d08ec49ebf1e403caeb67156d1cc8afb20571f8d19eb5caa6f1c687aa0dca0b2ebde879cf5594cd77f3c70ef556c0f0010c283e9bdf430d992028e2093fa2fc9a6d36edb6916; LGSID=20210418030826-97a89323-1f2f-4cce-a3c8-84d89c8602ed; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist%5Fc%252B%252B%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; _gat=1; TG-TRACK-CODE=index_navigation; X_MIDDLE_TOKEN=dac6f75e03ee4daa90ebc91a34708c95; gate_login_token=b76d6ebbb0efb2b29132e2e22929a335261130aeb4a01fd05197febcebe9ecdf; LG_LOGIN_USER_ID=bf396e2962ee33d6ca928cd93db942d5d62a4c07bc81f90f453271d964b07065; LG_HAS_LOGIN=1; _putrc=8D2D92126A466139123F89F2B170EADC; login=true; unick=%E5%BC%A0%E6%BE%8E; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%8C%97%E4%BA%AC; X_HTTP_TOKEN=6ee99f77028f6198005786816140ead36c2e5a3fdd; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216237121%22%2C%22first_id%22%3A%22178e06f20ae6b7-04601a2af0de8a-d7e1938-2073600-178e06f20af9e8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2290.0.4430.72%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%22178e06f20ae6b7-04601a2af0de8a-d7e1938-2073600-178e06f20af9e8%22%7D; LGRID=20210418032500-af109aff-e204-456f-9138-3533c464cb2f; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1618687501; SEARCH_ID=e1d7a9b210c14a259b00704eb6dce81b"
}


#  城市 [city] 薪资 [salary] split(",") split("k")获取k前面的数字 然后求平均 教育背景 [education] 公司名 [companyFullName]


def GetLaGouData(searchJob):
    cityMap = dict()
    salaryMap = dict()
    educationMap = dict()
    companyMap = dict()
    data = dict(first="true", pn="1", kd=searchJob)
    r = requests.post(url=URL, headers=HEADERS, data=data, verify=False)
    my_data = json.loads(r.content.decode())
    # print(my_data)
    # print(my_data['content']['positionResult']['result'])
    data_list = my_data['content']['positionResult']['result']
    for value in data_list:
        city = value['city']
        salaryStr: str = value['salary']
        salaryStr = salaryStr.lower()
        # print(type(salaryStr.split("-")[0].split('k')[0]))
        # time.sleep(100)
        salary = str((float(salaryStr.split("-")[0].split("k")[0]) + float(salaryStr.split("-")[1].split("k")[0])) / 2)
        education = value['education']
        company = value['companyFullName']
        print(city, salaryStr, salary, education, company, sep="\n")
        if city not in cityMap:
            cityMap.setdefault(city, 1)
        else:
            cityMap[city] = cityMap[city] + 1
        if salary not in salaryMap:
            salaryMap.setdefault(salary, 1)
        else:
            salaryMap[salary] = salaryMap[salary] + 1
        if education not in educationMap:
            educationMap.setdefault(education, 1)
        else:
            educationMap[education] = educationMap[education] + 1
        if company not in companyMap:
            companyMap.setdefault(company, 1)
        else:
            companyMap[company] = companyMap[company] + 1
        print(cityMap, salaryMap, educationMap, companyMap, sep="\n")

    # print(r.content.decode())
    sId = my_data['content']['showId']
    for i in range(2, 7):
        time.sleep(10)
        data = dict(first="true", pn=str(i), kd=searchJob, sid=sId)
        r = requests.post(url=URL, headers=HEADERS, data=data, verify=False)
        my_data = json.loads(r.content.decode())
        # print(my_data)
        # print(my_data['content']['positionResult']['result'])
        data_list = my_data['content']['positionResult']['result']
        for value in data_list:
            city = value['city']
            salaryStr: str = value['salary']
            salaryStr = salaryStr.lower()
            salary = str(
                (float(salaryStr.split("-")[0].split("k")[0]) + float(salaryStr.split("-")[1].split("k")[0])) / 2)+'k'
            education = value['education']
            company = value['companyFullName']
            print(city, salaryStr, salary, education, company, sep="\n")
            if city not in cityMap:
                cityMap.setdefault(city, 1)
            else:
                cityMap[city] = cityMap[city] + 1
            if salary not in salaryMap:
                salaryMap.setdefault(salary, 1)
            else:
                salaryMap[salary] = salaryMap[salary] + 1
            if education not in educationMap:
                educationMap.setdefault(education, 1)
            else:
                educationMap[education] = educationMap[education] + 1
            if company not in companyMap:
                companyMap.setdefault(company, 1)
            else:
                companyMap[company] = companyMap[company] + 1
            print(cityMap, salaryMap, educationMap, companyMap, sep="\n")  # print(r.content.decode())
    cityUri = GetImage(cityMap, searchJob + "_city_" + str(time.time()))
    salaryUri = GetImage(salaryMap, searchJob + "_salary_" + str(time.time()))
    educationUri = GetImage(educationMap, searchJob + "_education_" + str(time.time()))
    companyUri = GetImage(companyMap, searchJob + "_company_" + str(time.time()))
    InsertBoard(str(const.jobTypeMap[searchJob]), cityUri, salaryUri, educationUri, companyUri, "")



def GetLaGouTechData():
    techMap = dict()
    data = dict(first="true", pn="1", kd="")
    r = requests.post(url=URL, headers=HEADERS, data=data, verify=False)
    my_data = json.loads(r.content.decode())
    # print(my_data)
    # print(my_data['content']['positionResult']['result'])
    data_list = my_data['content']['positionResult']['result']
    for value in data_list:
        if "thirdType" not in value:
            continue
        tech = value['thirdType']
        if tech not in techMap:
            techMap.setdefault(tech, 1)
        else:
            techMap[tech] = techMap[tech] + 1
        print(techMap, sep="\n")

    # print(r.content.decode())
    sId = my_data['content']['showId']
    for i in range(2, 7):
        time.sleep(10)
        data = dict(first="true", pn=str(i), kd=searchJob, sid=sId)
        r = requests.post(url=URL, headers=HEADERS, data=data, verify=False)
        my_data = json.loads(r.content.decode())
        # print(my_data)
        # print(my_data['content']['positionResult']['result'])
        data_list = my_data['content']['positionResult']['result']
        for value in data_list:
            if "thirdType" not in value:
                continue
            tech = value['thirdType']
            if tech not in techMap:
                techMap.setdefault(tech, 1)
            else:
                techMap[tech] = techMap[tech] + 1
    techUri = GetImage(techMap, "tech_" + str(time.time()))
    InsertBoard(str(const.jobTypeMap["tech"]), "", "", "", "", techUri)



def GetImage(imageData, fileName):
    sum = 0.0
    for key in imageData:
        sum += imageData[key]
    newData = dict()
    maxKey = ""
    maxi=0
    for key in imageData:
        newData.setdefault(key + ":" + str(imageData[key]), imageData[key] / sum)
        if imageData[key] > maxi:
            maxi=imageData[key]
            maxKey = key + ":" + str(imageData[key])
    data = pd.Series(newData)
    # print(data)

    from matplotlib.font_manager import FontProperties  # 显示中文，并指定字体
    myfont = FontProperties(fname=r'C:/Windows/Fonts/simhei.ttf', size=14)
    sns.set(font=myfont.get_name())

    plt.rcParams['figure.figsize'] = (24.0, 16.0)  # 调整图片大小

    lbs = data.index
    explodes = [0.1 if i == maxKey else 0 for i in lbs]
    plt.pie(data, explode=explodes, labels=lbs, autopct="%1.1f%%",
            colors=sns.color_palette("muted"), startangle=90, pctdistance=0.6,
            textprops={'fontsize': 14, 'color': 'black'})
    plt.title(fileName.split("_")[0]+'-'+fileName.split("_")[1])
    plt.axis('equal')  # 设置x，y轴刻度一致，以使饼图成为圆形。
    filePath='../image/' + fileName + '.png'
    plt.savefig(filePath)  # 保存图片
    plt.clf()
    plt.cla()
    url = uploadImage(filePath)
    return url
    # plt.show()


if __name__ == '__main__':
    # 根据职位落 城市 薪资 公司 教育背景
    for searchJob in const.SearchList:
        GetLaGouData(searchJob)
        time.sleep(20)
    # 空搜落tech
    GetLaGouTechData()
