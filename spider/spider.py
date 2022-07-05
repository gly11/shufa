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


def postHTML(url, word, type, code="utf-8"):
    # search character
    data = {"keyboard": word, "sort": type}
    try:
        r = requests.post(url, headers=headers, data=data)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except requests.exceptions.HTTPError:
        print("Error: not 200 code. Code: 7")
        return ""
    except:
        print("Error: failed to post. Code: 4 (Maybe Network Error.)")
        return ""


def getHTML(url, code="utf-8"):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("Error: failded to get. Code: 5")
        return ""


def findPics(html):
    soup = BeautifulSoup(html, "html.parser")
    box = soup.find("div", {"class": "writer_box"})
    pics = box.find_all("a", {"data-fancybox": "images"})
    ch = box.find_all("p", {"class": "writer"})
    pics_list = []
    word_list = []
    # pics = soup.find_all("src")
    # print(len(pics))
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
            pic = requests.get(pic_url).content
            with open() as f:
                f.close()
        except:
            print("Download failed code: 6")
    return pics_list


def findPages(html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        pages = soup.find("div", {"class": "page"}).find_all('a')
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


def getPicList(html, homeurl, number, pic_path, csv_path, number_per_page=24):
    last_page = findPages(html)
    if last_page != 0:
        max = last_page[1].split('.')[0]
        page_list = [last_page[0] + '.html']

        for i in range(2, int(max) + 1):
            url_i = last_page[0] + '-' + str(i) + '.html'
            # print(url_i)
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
                # data_dict[str(number - 1)] = word_list[number - 1]
    else:
        pics_list, word_list = findPics(html)
        # pic_dict.update(dict.fromkeys(pics_list,word))
        for pic in pics_list:
            try:
                number = downloadPic(pic, pic_path, number, csv_path, word_list[number - 1])
                print(f"#{(number - 1):3d} suceeded.")
            except IndexError:
                print("IndexError: code: 8.2")
            except:
                print("failed code: 2.2")
            # data_dict[str(number - 1)] = word_list[number - 1]

    # print(len(pic_dict))
    # return pic_dict


def downloadPic(pic_url, pic_path, number, csv_path, word):
    try:
        pic = requests.get(pic_url).content
        with open(f"{pic_path}{str(number)}.{pic_url.split('.')[-1]}", 'wb') as f:
            f.write(pic)
            f.close()
        with open(f"{csv_path}data.csv", 'a') as f:
            w = csv.writer(f)
            w.writerow([number, word])
            f.close()
        number += 1
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
    getPicList(html, homeurl, number, pic_path, csv_path)


def main():
    homeurl = 'http://www.jidajia.com'
    pic_path = './img/'
    csv_path = './csv/'
    word = '芋'

    setDir(pic_path, _del=True)
    setDir(csv_path)
    initCSV(csv_path, 'data.csv')
    search(word, homeurl, pic_path, csv_path)


if __name__ == "__main__":
    main()
