# -*- coding: utf-8 -*-
# python version : 3.6

import urllib.request
import os
import datetime
import random
from lxml import etree
import time
import requests
import win32con,win32api 
import argparse
import datetime
import re
import subprocess


def use_proxy(url):
    req=urllib.request.Request(url)
    proxy_addr = None # get_OneProxy()
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler(proxy_addr)
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data

def waiting_times(judge,times = None):
    sleeptime = 0
    if times == None:
        sleeptime = random.randint(1,5)
    if( judge % 3 == 0):
        print("Sleeping timezone :  %s"%sleeptime)
        time.sleep(sleeptime)
 
def download_icons(url,save_name):
    icon_names = []  
    stime = time.perf_counter()
    print(u"%s downloading ......"% datetime.datetime.now().strftime('[%H:%M:%S]'))
    picName = "%s" % (save_name)
    print(picName)
    if os.path.exists(picName) : # 存在 末尾增(2)或(3) (4) (5) (6) ...
        basename = os.path.splitext(picName)[0]
        extname = os.path.splitext(picName)[1]
        if len(basename) > 3:
            spatt = basename[-3:]
            if spatt.find("(")>0 and spatt.find(")") and (spatt[1].isnumeric())>0 :
                new_nums = int(spatt[1]) + 1
                spatt = "(%s)" % new_nums
                basename = "%s%s" % ( basename[:-4],spatt)
            else:
                basename = "%s(2)"  % basename
        else:
            basename = "%s(2)"  % basename
        print(basename)
        picName = "%s%s" % (basename,extname)
        print(picName)
    response = requests.get(url)
    if response.status_code == 200:
        fn = picName
        with open( fn , 'wb') as f:  # 以二进制写入到本地
            f.write(response.content)
            f.close()
        icon_names.append(fn)                
    etime = time.perf_counter()
    times = etime - stime
    print(u"%s downloaded  耗时: %.2f 秒"% (datetime.datetime.now().strftime('[%H:%M:%S]'),times))
    
    return icon_names
 
            
def find_Icons_Url_FromWeb(url,save_dir,key):
    rets = []
    content = use_proxy(url)
    baseUrl = "https://www.easyicon.net"
    if content.find("无任何结果") > 0 :
        print("Found None")
        return rets
    try:        
        html =  etree.HTML(content)
        icon_divs =  html.xpath('//div[@class="icon_img"]')
        icon_url = ""
        for i_div in icon_divs:
            icon_url = i_div.xpath('.//a/@href')[0]
            break
        two_url = "%s%s" % (baseUrl,icon_url)
        print("two_url=  %s" %two_url)
        #exit(0)
        twopage = use_proxy(two_url)
        html2 =  etree.HTML(twopage)
        detail_icon_url = html2.xpath('/html/body/div[2]/div[2]/div[2]/h4/a[2]/@href')[0]      
        print("detail_icon_url= %s"%detail_icon_url)
        save_name = "%s/%s.ico" % ( save_dir,key)
        print("save_name = %s"% save_name)
        rets = download_icons (detail_icon_url,save_name) 
        return rets
    except etree.ParserError as e: 
        print("At url=%s  \nError type = %s"%(url,e  ))
        return rets

 
def modify_directory_icon(target_dir,icons_names,icon_index = 0 )  :
    exe_file = os.path.join(".","modSetter")
    iconfile =  os.path.abspath(icons_names)
    desktop_file = r"%s/%s"%(target_dir,"desktop.ini")
    #win32api.WriteProfileSection(".ShellClassInfo",  "IconFile", iconfile  , desktop_file)
    #win32api.WriteProfileval("IconFile", iconfile)
    #win32api.WriteProfileSection(".ShellClassInfo", "IconIndex","0",desktop_file)
    #with open (desktop_file,'w') as  fn:
     #   fn.write(".ShellClassInfo\n")
     #   fn.write("IconFile=%s\n"%iconfile)
     #   fn.write("IconIndex=%s\n"% str(0))
    set_icon (exe_file,target_dir,iconfile)
    #win32api.SetFileAttributes(desktop_file,win32con.FILE_ATTRIBUTE_READONLY)
    #win32api.SetFileAttributes(iconfile, win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_ARCHIVE)
    time.sleep(0.5)

def getKeysFromDirectoryNames(cur_dir):
    targets = [] 
    #从文件夹名称中 分词 提取名词
    for tar in os.listdir(cur_dir):         
        if os.path.isdir(tar) and tar !=".idea":
            if tar.find(" ")> 0 :
                print("暂不提供设置含有空格的文件夹的图标")
                pass
            else:
                targets.append(tar)
    print(tar)
    return targets


def set_icon(exe_file,dir_name, icon_file):
    process = subprocess.Popen(
        [exe_file,dir_name,icon_file],
        stderr=subprocess.PIPE,
        close_fds=True
    )
    output = ""
    iterations = 0
    # ensure the output contains "Duration"
    while (not "start" in output and iterations < 100):
        buffer_read = str(process.stderr.read())
        iterations += 1
        if (buffer_read != "None"):
            output += buffer_read
        # print(iterations)
        time.sleep(.01)


def main():   
    cur_dir = "." # input('Set handling directory to Icon : ')
    while  os.path.isdir(cur_dir) !=True:
        cur_dir = input('Input a directory\nSet handling directory to Icon : ')
    save_download_icons = "./icons_download_historys"
    if os.path.exists(save_download_icons) == False:
        os.mkdir(save_download_icons)
    keys = getKeysFromDirectoryNames(cur_dir)
    for key in keys:
        print("key=%s"%key) 
        query_url = "https://www.easyicon.net/iconsearch/%s/" % requests.utils.quote(key) 
        print(query_url)
        icons = find_Icons_Url_FromWeb (query_url,save_download_icons,key)
        if icons != [] :
            target_dir = os.path.abspath("%s/%s"%(cur_dir,key))
            print(target_dir)
            modify_directory_icon(target_dir,icons[0])
        
 
if __name__ == '__main__':    
    main()
