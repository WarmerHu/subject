#coding:utf-8
'''
Created on 2016年3月19日
@author: Warmer
思路：维度=2；正则匹配
'''
import urllib2
import re
import time
from jobs.dao import insert_jobs

joblist = []
massage = []
detail = []

'''
模拟浏览器
'''
def getHTML(url):
    req_header = {
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36',
                  'Referer':'http://search.51job.com'
                  }
    
#     req_timeout = 5
    opener = urllib2.build_opener(urllib2.ProxyHandler({'http':'14.18.252.61:80'}), urllib2.HTTPHandler(debuglevel=1))
    urllib2.install_opener(opener)
    req = urllib2.Request(url,headers=req_header)
#     resp = urllib2.urlopen(req,None,req_timeout)
    resp = urllib2.urlopen(req)
    html = resp.read()
    print("html:",html)
    return html

def getJOB(html):
    regLIST = '<div class="el">(.*?)</div>'
    jobreg = re.compile(regLIST)
    joblisthtml = re.findall(jobreg, html)
    print("joblisthtml:",joblisthtml)
    
    regTIME = '<span class="t5">(.+)</span>'
    regURL = '<a onmousedown="" href="(.+)"' 
    now = time.strftime('%m-%d',time.localtime(time.time()))
    timereg = re.compile(regTIME)
    urlreg = re.compile(regURL)
    print("now:",now)
    for v,n in enumerate(joblisthtml):
        publishtime = re.findall(timereg, v)[0]
        print("publishtime:",publishtime)
        if publishtime == now:
            joblist.append(re.findall(urlreg, v)[0])
        if n==10:
            break
    
    print("joblist",joblist)
    return joblist

def getDetail(joblist):
    for v in joblist:
        html = getHTML(v)
        positionreg = '<h1 title="(.+)"'
        regP = re.compile(positionreg)
        companyreg = '<a title="(.+)" target="_blank"'
        regCP = re.compile(companyreg)
        dutyreg = '<div class="bmsg job_msg inbox">(.+)<div class="mt10">'
        regD = re.compile(dutyreg)
        contactreg = '\w+@\W+\.[A-Z]{2,6}'
        regCT = re.compile(contactreg)
        position = re.match(regP, html)
        company = re.match(regCP, html)
        duty = re.match(regD, html)
        contact = re.match(regCT, html)
        detail.append({'positon':position,
                       'source':v,
                       'company':company,
                       'duty':duty,
                       'contact':contact,
                       'createtime':time.localtime(time.time())})
        
    print("detail:",detail)
    return detail

def JobCraw():
    url = []
#     url.append('http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=04%2C05%2C06%2C07&keyword=python&keywordtype=2&curr_page=1&lang=c&stype=2&postchannel=0000&workyear=99&cotype=99&degreefrom=04%2C05%2C06&jobterm=99&companysize=03%2C04%2C05%2C06%2C07&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confirmdate=9')
    url.append('http://search.51job.com/jobsearch/search_result.php?fromJs=1&issuedate=9&providesalary=99&keyword=python&keywordtype=2&lang=c&stype=2&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&fromType=1')
    for v in url:
        insert_jobs(getDetail(getJOB(getHTML(v))))
        