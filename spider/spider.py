import csv
import shutil
import requests
from bs4 import BeautifulSoup
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/103.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookies": "",
}


def postHTML(url, word, _type, code="utf-8", time=10):
    # search character
    data = {"keyboard": word, "sort": _type}
    try:
        r = requests.post(url, headers=headers, data=data, timeout=time)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except requests.exceptions.HTTPError:
        print("Error: not 200 code. Code: 7")
    except requests.exceptions.ReadTimeout:
        print(f"Timeout: {url} (read timeout={time})")
        return "timeout"
    except Exception as err:
        print(f"Error: failed to post. Code: 4 (Maybe Network Error.)\n错误信息：{err}")


def getHTML(url, code="utf-8", time=10):
    try:
        r = requests.get(url, headers=headers, timeout=time)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except requests.exceptions.HTTPError:
        print("Error: not 200 code. Code: 9")
    except requests.exceptions.ReadTimeout:
        print(f"Timeout: {url} (read timeout={time})")
        return "timeout"
    except Exception as err:
        print(f"Error: failded to get. Code: 5 (Maybe Network Error.)\nurl={url}\n错误信息：{err}")


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


# def downPic(html, time=10):
#     soup = BeautifulSoup(html, "html.parser")
#     box = soup.find("div", {"class": "writer_box"})
#     pics = box.find_all("a", {"data-fancybox": "images"})
#     ch = box.find_all("p", {"class": "writer"})
#     pics_list = []
#     word_list = []
#     # pics = soup.find_all("src")
#     # print(len(pics))
#     for i in range(len(pics)):
#         pic_url = pics[i]['href']
#         pics_list.append(pic_url)
#         word_list.append(ch[i].string.split("（")[0])
#         try:
#             pic = requests.get(pic_url, timeout=time).content
#             with open() as f:
#                 f.close()
#         except requests.exceptions.ReadTimeout:
#             print(f"{pic_url}' (read timeout={time})")
#             return ""
#         except Exception as err:
#             print(f"Download failed code: 6\n错误信息：{err}")
#     return pics_list


def findPages(html, type='single_word'):
    soup = BeautifulSoup(html, "html.parser")
    try:
        pages = soup.find("div", {"class": "page"}).find_all('a')
    except Exception as err:
        print(soup)
        print(f"Error getting Pages: code 3.\n错误信息：{err}")

    try:
        url_family = pages[-1]['href']
        if type == 'single_word':
            last_page = url_family.split('-')
        elif type == 'home':
            last_page = url_family.split('_')
        else:
            print("Wrong type. Error!")
            last_page = 0
            exit(-1)
    except Exception as err:
        last_page = 0
        # print("No more than one page.")

    return last_page


def singleWordDownload(html, no, number_per_page=24, num_i=0):
    last_page = findPages(html)
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
                    no, num_i = downloadPic(pic, no, num_i, word_list[num_i % number_per_page])
                    print(f"#{(no - 1):3d}  succeeded.")
                except IndexError:
                    print("IndexError: code: 8.1")
                except Exception as err:
                    print(f"Error: failed code: 2.1\n错误信息：{err}")

                # print(no)
                # data_dict[str(no - 1)] = word_list[no - 1 - 1]
    else:
        pics_list, word_list = findPics(html)

        for pic in pics_list:
            try:
                no, num_i = downloadPic(pic, no, num_i, word_list[num_i])
                print(f"#{(no - 1):3d}  succeeded.")
            except Exception as err:
                print(f"Error: failed code: 2.2\n错误信息：{err}")
                exit()
            # print(no)
            # data_dict[str(no - 1)] = word_list[no - 1 - 1]

    # print(len(pic_dict))
    # return pic_dict
    return no


def downloadPic(pic_url, no, num_i, word, time=10):
    try:
        pic = requests.get(pic_url, timeout=10).content
        with open(f"{pic_path}{str(no)}.{pic_url.split('.')[-1]}", 'wb') as f:
            f.write(pic)
            f.close()

        writeCSV([no, word], csv_name='data')

        no += 1
        num_i += 1
    except requests.exceptions.ReadTimeout:
        print(f"{pic_url}' (read timeout={time})")
        return ""
    except Exception as err:
        print(f"Download failed code: 1\n错误信息：{err}")
    return no, num_i


def writeCSV(rows, csv_name):
    with open(f"{csv_path}{csv_name}.csv", 'a') as f:
        w = csv.writer(f)
        w.writerow(rows)
        f.close()


def initCSV(name, title):
    with open(csv_path + name, 'w') as f:
        w = csv.writer(f)
        w.writerow(title)
        f.close()


def setDir(filepath, _del=False):
    """
    如果文件夹不存在就创建，如果文件存在就清空！
    :param filepath:需要创建的文件夹路径
    :return:
    """
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        if _del:
            shutil.rmtree(filepath)
            os.mkdir(filepath)
        else:
            pass


def search(word):
    search_url = 'http://www.jidajia.com/e/search/index2.php'

    no = 1

    html = postHTML(search_url, word, _type=52)
    # data_dict = {}
    no = singleWordDownload(html, no)
    return no


def spiderAll(homeurl, type='kaishu', __mode__='count'):
    url = f'{homeurl}/{type}/'
    html = getHTML(url)

    # 构建页面列表
    last_page = findPages(html, type='home')  # 读取总页面数
    # print(last_page)
    max = last_page[1].split('.')[0]
    page_list = [f"{homeurl}{last_page[0]}.html"]

    for i in range(2, int(max) + 1):
        url_i = f"{homeurl}{last_page[0]}_{i}.html"
        page_list.append(url_i)
    # print(page_list[:2]) 
    word_list = []

    for page in page_list[:1]:
        page_html = getHTML(page)  # 楷书的某一页
        word_list += findPics(page_html)[0]

    count = 0
    no = 1

    if __mode__ == 'count':
        initCSV('words_count.csv', title=['word', 'count'])
        initCSV('error_words.csv', title=['url', '原因'])
        for word_page in word_list:
            count, no = countWord(homeurl + word_page, count, no)
        print(count)

    elif __mode__ == 'download':
        initCSV('data.csv', title=['name', 'word'])
        for word_page in word_list[:2]:
            # print(word_page)
            word_html = getHTML(homeurl + word_page)
            no = singleWordDownload(word_html, no)


def countWord(url, count, no):
    html = getHTML(url)
    if html != 'timeout':
        try:
            soup = BeautifulSoup(html, "html.parser")
            ch = soup.find_all("p", {"class": "writer"})
            div = soup.find('div', {'class': 'page'})
            # print(div)
            b = div.find('b')
            if b == None:
                number = len(ch)
            else:
                number = int(b.string)
            count += number
            word = f"{ch[0].string.split('（')[0]}({no})"
            row2 = f"{number}/{count}"
            print(f"{word}:{row2}")
            writeCSV([word, row2], 'words_count')
            no += 1
        except Exception as err:
            print(url)
            print(f"url:{url}\n异常信息：{err}")
            writeCSV([url, err], 'error_words')
    else:
        writeCSV([url, html], 'error_words')  # html == timeout
    return count, no


homeurl = 'http://www.jidajia.com'  # 末尾不加 '/' !!!
pic_path = './img/'
csv_path = './csv_files/'


def main():
    word = '芋'

    # setDir(_del=True)
    # setDir()
    # search(word, homeurl)
    # spiderAll(homeurl)
    spiderAll(homeurl, __mode__="download")


if __name__ == "__main__":
    main()
