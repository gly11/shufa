import csv
import shutil
import requests
from bs4 import BeautifulSoup
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookies": "",
}


def postHTML(url, word, type, code="utf-8", time = 10):
    # search character
    data = {"keyboard": word, "sort": type}
    try:
        r = requests.post(url, headers=headers, data=data, timeout=time)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except requests.exceptions.HTTPError:
        print("Error: not 200 code. Code: 7")
        return ""
    except requests.exceptions.ReadTimeout:
        print(f" HTTPConnectionPool(host='{url}', port=80): Read timed out. (read timeout={time})")
    except:
        print("Error: failed to post. Code: 4 (Maybe Network Error.)")
        return ""


def getHTML(url, code="utf-8", time = 10):
    try:
        r = requests.get(url, headers=headers, timeout=time)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except requests.exceptions.HTTPError:
        print("Error: not 200 code. Code: 9")
        return ""
    except requests.exceptions.ReadTimeout:
        print(f" HTTPConnectionPool(host='{url}', port=80): Read timed out. (read timeout={time})")
    except:
        print("Error: failded to get. Code: 5 (Maybe Network Error.)")
        print(f"url={url}")
        return ""


def findPics(html):
    soup = BeautifulSoup(html, "html.parser")
    box = soup.find("div", {"class": "writer_box"})
    ul = box.find('ul')
    pics = ul.find_all("a")                        
    ch = ul.find_all("p", {"class": "writer"})
    pics_list = []
    word_list = []
    
    for i in range(len(pics)):
        pics_list.append(pics[i]['href'])
        word_list.append(ch[i].string.split("（")[0])
    # print(word_list)
    return pics_list, word_list


def downPic(html):
    soup = BeautifulSoup(html, "html.parser")
    box = soup.find("div", {"class": "writer_box"})
    pics = box.find_all("a", {"data-fancybox": "images"})
    ch = box.find_all("p", {"class": "writer"})
    pics_list = []
    word_list = []
    # pics = soup.find_all("src")
    # print(len(pics))
    for i in range(len(pics)):
        pic_url = pics[i]['href']
        pics_list.append(pic_url)
        word_list.append(ch[i].string.split("（")[0])
        try:
            pic = requests.get(pic_url, timeout=10).content
            with open() as f:
                f.close()
        except requests.exceptions.ReadTimeout:
            print(f" HTTPConnectionPool(host='{url}', port=80): Read timed out. (read timeout={time})")
        except:
            print("Download failed code: 6")
    return pics_list


def findPages(html, type='single_word'):
    soup = BeautifulSoup(html, "html.parser")
    try:
        pages = soup.find("div", {"class": "page"}).find_all('a')
    except:
        print("Error getting Pages: code 3.")
        print(soup)

    if type == 'single_word':
        try:
            url_family = pages[-1]['href']
            last_page = url_family.split('-')
        except:
            last_page = 0
            print("No more than one page.")
    elif type == 'home':
        try:
            url_family = pages[-1]['href']
            last_page = url_family.split('_')
        except:
            last_page = 0
            print("No more than one page.")
    else:
        assert("Wrong type. Error!")
    return last_page


def singleWordDownload(html, homeurl, number, pic_path, csv_path, number_per_page=24):
    last_page = findPages(html)
    print(last_page)
    if last_page != 0:      
        # 不止一页的情形，构建页面列表
        max = last_page[1].split('.')[0]
        page_list = [f"{homeurl}{last_page[0]}.html"]

        for i in range(2, int(max) + 1):
            url_i = f"{homeurl}{last_page[0]}-{i}.html"
            page_list.append(url_i)
        # print(page_list)
        for page in page_list:
            html_page = getHTML(homeurl + page)
            pics_list, word_list = findPics(html_page)
            for pic in pics_list:
                try:
                    number = downloadPic(pic, pic_path, number, csv_path, word_list[(number - 1)%number_per_page])
                    print(f"#{(number - 1):3d} suceeded.")
                except IndexError:
                    print("IndexError: code: 8.1")
                except:
                    print("failed code: 2.1")

                # print(number)
                # data_dict[str(number - 1)] = word_list[number - 2]
    else:
        pics_list, word_list = findPics(html)
        
        for pic in pics_list:
            try:
                number = downloadPic(pic, pic_path, number, csv_path, word_list[number - 1])
                print(f"#{(number - 1):3d} suceeded.")
            except IndexError:
                print("IndexError: code: 8.2")
            except:
                print("failed code: 2.2")
            # print(number)
            # data_dict[str(number - 1)] = word_list[number - 2]

    # print(len(pic_dict))
    # return pic_dict
    return number


def downloadPic(pic_url, pic_path, number, csv_path, word):
    try:
        pic = requests.get(pic_url, timeout=10).content
        with open(f"{pic_path}{str(number)}.{pic_url.split('.')[-1]}", 'wb') as f:
            f.write(pic)
            f.close()
        with open(f"{csv_path}data.csv", 'a') as f:
            w = csv.writer(f)
            w.writerow([number, word])
            f.close()
        number += 1
    except requests.exceptions.ReadTimeout:
        print(f" HTTPConnectionPool(host='{url}', port=80): Read timed out. (read timeout={time})")
    except:
        print("Download failed code: 1")
    return number


def writeCSV(csv_path, dict, name):
    fieldnames = ['pic', 'word']
    with open(f"{csv_path}{name}.csv", 'w') as f:  # !!! 'a'
        w = csv.writer(f)
        w.writerow(fieldnames)
        for row in dict.items():
            w.writerow(row)
        f.close()


def initCSV(path, name):
    with open(path + name, 'w') as f:
        w = csv.writer(f)
        w.writerow(['name', 'word'])
        f.close()


def setDir(filepath, _del=False):
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


def search(word, homeurl, pic_path, csv_path):
    search_url = 'http://www.jidajia.com/e/search/index2.php'

    number = 1

    html = postHTML(search_url, word, type=52)
    # data_dict = {}
    singleWordDownload(html, homeurl, number, pic_path, csv_path)


def countAll(homeurl, type='kaishu'):
    url = f'{homeurl}/{type}/'
    html = getHTML(url)

    # 构建页面列表
    last_page = findPages(html, type='home')     # 读取总页面数
    # print(last_page)
    max = last_page[1].split('.')[0]
    page_list = [f"{homeurl}{last_page[0]}.html"]

    for i in range(2, int(max) + 1):
        url_i = f"{homeurl}{last_page[0]}_{i}.html"
        page_list.append(url_i)
    # print(page_list[:2]) 
    word_list = []
    
    for page in page_list[:2]:
        page_html = getHTML(page)      # 楷书的某一页
        word_list += findPics(page_html)[0]
    
    count = 0
    no = 0
    for word_page in word_list:
        no += 1
        count = countWord(homeurl + word_page, count, no)
    print(count)


def countWord(url, count, no):
    html = getHTML(url)
    soup = BeautifulSoup(html, "html.parser")
    ch = soup.find_all("p", {"class": "writer"})
    div = soup.find('div', {'class':'page'})
    # print(div)
    b = div.find('b')
    if b == None:
        number = len(ch)
    else:
        number = int(b.string)
    count += number
    print(f"{ch[0].string.split('（')[0]}({no}):{number}/{count}")

    return count



def spiderAll(homeurl, pic_path, csv_path, type='kaishu'):
    url = f'{homeurl}/{type}/'
    html = getHTML(url)

    # 构建页面列表
    last_page = findPages(html, type='home')     # 读取总页面数
    # print(last_page)
    max = last_page[1].split('.')[0]
    page_list = [f"{homeurl}{last_page[0]}.html"]

    for i in range(2, int(max) + 1):
        url_i = f"{homeurl}{last_page[0]}_{i}.html"
        page_list.append(url_i)
    # print(page_list[:2]) 
    number = 1
    for word_page in page_list[:2]:
        word_html = getHTML(word_page)
        







def main():
    homeurl = 'http://www.jidajia.com'      # 末尾不加 '/' !!!
    pic_path = './img/'
    csv_path = './csv/'
    word = '芋'

    # setDir(pic_path, _del=True)
    # setDir(csv_path)
    # initCSV(csv_path, 'data.csv')
    # search(word, homeurl, pic_path, csv_path)
    # spiderAll(homeurl, pic_path, csv_path)
    countAll(homeurl)



if __name__ == "__main__":
    main()
