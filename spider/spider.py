import csv
import shutil
import requests
from bs4 import BeautifulSoup
import os


headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", 
	"Content-Type": "application/x-www-form-urlencoded", 
    "Cookies":"",
}


def postHTML(url, word, type, code="utf-8"):
    # search character
    data = {"keyboard":word, "sort":type}
    try:
        r = requests.post(url, headers=headers, data=data)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("Error: failded to post. Code :4")
        return ""


def getHTML(url,code="utf-8"):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("Error: failded to get. Code :5")
        return ""


def findPics(html):
    soup = BeautifulSoup(html, "html.parser")
    box = soup.find("div",{"class":"writer_box"})
    pics = box.find_all("a",{"data-fancybox":"images"})
    ch = box.find_all("p", {"class":"writer"})
    pics_list = []
    word_list = []
    # pics = soup.find_all("src")
    # print(len(pics))
    for i in range(len(pics)):
        pics_list.append(pics[i]['href'])
        word_list.append(ch[i].string.split("（")[0])
        # pic = requests.get(pic_url).content
    return pics_list


def findPages(html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        pages = soup.find("div", {"class":"page"}).find_all('a')
    except:
        print("Error getting Pages: code 3.")
        print(soup)

    try:
        url_family = pages[-1]['href']
        last_page = url_family.split('-')
    except:
        last_page = 0
        print("No more than one page.")
    return last_page


def getPicList(html, homeurl, word, pic_dict, number, pic_path, data_dict, csv_path):
    last_page = findPages(html)
    if last_page != 0:
        max = last_page[1].split('.')[0]
        page_list = [last_page[0]+'.html']


        for i in range(2, int(max)+1):
            url_i = last_page[0] + '-' + str(i) + '.html'
            # print(url_i)
            page_list.append(url_i)
        # print(page_list)
        for page in page_list:
            html_page = getHTML(homeurl + page)
            pics_list = findPics(html_page)
            # pic_dict.update(dict.fromkeys(pics_list,word))
            for pic in pics_list:
                try:
                    number = downloadPic(pic, pic_path, number, csv_path, word)
                    print("#"+str(number-1)+" suceeded.")
                except:
                    print("failed code:2")
                data_dict[str(number-1)] = word
    else:
        pics_list = findPics(html)
        # pic_dict.update(dict.fromkeys(pics_list,word))
        for pic in pics_list:
            try:
                number = downloadPic(pic, pic_path, number, csv_path, word)
                print("#"+str(number-1)+" suceeded.")
            except:
                print("failed code:2")
            data_dict[str(number-1)] = word

    # print(len(pic_dict))
    return pic_dict


def downloadPic(pic_url, pic_path, number, csv_path, word):
    try:
        pic = requests.get(pic_url).content
        with open(pic_path+str(number)+'.'+pic_url.split(".")[-1], 'wb') as f:
            f.write(pic)
            f.close()
        with open(csv_path + "data.csv", 'a') as f:      
            w = csv.writer(f)
            w.writerow([number, word])
            f.close()
        number += 1
    except:
        print("failed code:1")
    return number


def writeCSV(csv_path, dict, name):
    fieldnames = ['pic','word']
    with open(csv_path+ name + '.csv', 'w') as f: # !!! 'a'
        w = csv.writer(f)
        w.writerow(fieldnames)
        for row in dict.items():
            w.writerow(row)
        f.close()


def initCSV(path, name):
    with open(path+name, 'w') as f:
        w = csv.writer(f)
        w.writerow(['name', 'word'])
        f.close()


def setDir(filepath, _del = False):
    '''
    如果文件夹不存在就创建，如果文件存在就清空！
    :param filepath:需要创建的文件夹路径
    :return:
    '''
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        if _del:
            shutil.rmtree(filepath)
            os.mkdir(filepath)
        else:
            pass



def main():
    search_url = 'http://www.jidajia.com/e/search/index2.php'
    homeurl = 'http://www.jidajia.com'
    pic_path = './img/'
    csv_path = './csv/'

    setDir(pic_path, _del = True)
    setDir(csv_path)
    initCSV(csv_path, 'data.csv')

    word = "芋"
    number = 1

    html = postHTML(search_url, word, type=52)
    pic_dict_all = {}
    data_dict = {}
    pic_dict_all = getPicList(html, homeurl, word, pic_dict_all, number, pic_path, data_dict, csv_path)
    # print( pic_dict_all) 
    

if __name__ == "__main__":
    main()
