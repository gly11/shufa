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
    'Accept-Language':'zh-CN,zh;q=0.9',
}

time = 10

def postHTML(url, word, _type, code="utf-8"):
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


def getHTML(url, code="utf-8"):
    try:
        r = requests.get(url, headers=headers, timeout=time)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except requests.exceptions.HTTPError as err:
        print("Getting HTML Error: not 200 code. Code: 9\nurl={url}\n错误信息：{err}")
        return 'not200'
    except requests.exceptions.ReadTimeout:
        print(f"Getting HTML  Timeout: {url} (read timeout={time}). Code: 10")
        return "timeout"
    except Exception as err:
        print(f"Getting HTML  Error: failded to get. Code: 5 (Maybe Network Error.)\nurl={url}\n错误信息：{err}")


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
        # print(last_page)
        max = last_page[1].split('.')[0]
        page_list = [f"{last_page[0]}.html"]

        for i in range(2, int(max) + 1):
            url_i = f"{last_page[0]}-{i}.html"
            page_list.append(url_i)
        # print(page_list)
        for page in page_list:
            page_url = homeurl + page
            html_page = getHTML(page_url)

            try:
                pics_list, word_list = findPics(html_page)
                for pic in pics_list:
                    try:
                        no, num_i = downloadPic(pic, no, num_i, word_list[num_i % number_per_page])
                    except IndexError:
                        print("IndexError: code: 8.1")
                    except Exception as err:
                        print(f"Error: failed code: 2.1\n错误信息：{err}")
            except Exception as err:
                writeCSV([page_url, f'Single Word Download read error: {err}'], 'read_error')

                    # print(no)
                    # data_dict[str(no - 1)] = word_list[no - 1 - 1]
    else:
        pics_list, word_list = findPics(html)

        for pic in pics_list:
            try:
                no, num_i = downloadPic(pic, no, num_i, word_list[num_i])
            except Exception as err:
                print(f"Error: failed code: 2.2\n错误信息：{err}")
                exit()
            # print(no)
            # data_dict[str(no - 1)] = word_list[no - 1 - 1]

    # print(len(pic_dict))
    # return pic_dict
    return no


def downloadPic(pic_url, no, num_i, word):
    try:
        pic = requests.get(pic_url, timeout=10).content
        with open(f"{pic_path}{str(no)}.{pic_url.split('.')[-1]}", 'wb') as f:
            f.write(pic)
            f.close()
        writeCSV([no, word], csv_name='data')
        print(f"#{no :3d}  succeeded.")
        no += 1
        num_i += 1
    except requests.exceptions.ReadTimeout:
        print(f"{pic_url}' (read timeout={time})")
        writeCSV([pic_url, 'timeout'], 'download_error')
    except Exception as err:
        print(f"Download failed code: 1\n错误信息：{err}")
        writeCSV([pic_url, err], 'download_error')
    return no, num_i


def writeCSV(rows, csv_name):
    with open(f"{csv_path}{csv_name}.csv", 'a') as f:
        w = csv.writer(f)
        w.writerow(rows)
        f.close()


def initCSV(name, title):
    with open(csv_path + name + '.csv', 'w') as f:
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
    initCSV('read_error', ['url', 'reason'])

    try:
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
        i = 1
        for page in page_list:
            print(f"Reading page {i:3d}/{int(max)+1}.", end="")
            i += 1
            page_html = getHTML(page)  # 楷书的某一页
            # if page_html != 'timeout':
            try:
                word_list += findPics(page_html)[0]
                print(f"{'.'*10}Success!")
            except Exception as err:
                print(f"{'.'*10}Failed! Error: {err}")
                writeCSV([page, f'Reading page error: {err}'], 'read_error')
    
        count = 0
        no = 1
        i = 1
    
        if __mode__ == 'count':
            initCSV('words_count', title=['word', 'count'])
            initCSV('error_words', title=['url', '原因'])
            for word_page in word_list:
                print(f"Reading page {i:3d}/{int(max)+1}.", end="")
                count, no = countWord(homeurl + word_page, count, no)
                i += 1
            print(f"{count} in total!")
    
        elif __mode__ == 'download':
            initCSV('data', title=['name', 'word'])
            initCSV('download_error', title=['url', 'reason'])
            for word_page in word_list:
                print(f"Downloading page {i:3d}/{int(max)+1}.", end="")
                word_url = homeurl + word_page
                word_html = getHTML(word_url)
                try:
                    no = singleWordDownload(word_html, no)
                except Exception as err:
                    print(f"Download Error. Code 12. Message: {err}")
                    writeCSV([word_url, f'Reading word error: {err}'], 'read_error')
                i += 1
    except Exception as err:
        print(f"Error code: 11. Message: {err}")
        writeCSV([url, 'timeout'], 'read_error')



def countWord(url, count, no):
    html = getHTML(url)
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
    return count, no


homeurl = 'http://www.jidajia.com'  # 末尾不加 '/' !!!
pic_path = './img/'
csv_path = './csv_files/'


def main():
    word = '芋'

    # setDir(_del=True)
    # setDir()
    # search(word, homeurl)

    spiderAll(homeurl)
    # spiderAll(homeurl, __mode__="download")


if __name__ == "__main__":
    main()
