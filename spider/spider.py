import csv
import shutil
# import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/103.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookies": "",
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

time = 20
__local__ = 'local'
__count__ = 'count'
__download__ = 'download'
__record__ = 'record'
__fix_page__ = 'fix_page'
__get_picture_list__ = 'get_picture_list'
__get__ = 'get'
__post__ = 'post'
__fix_raw_data__ = 'fix_raw_data'
number_per_page = 24
_word_type = 52

homeurl = 'http://www.jidajia.com'  # 末尾不加 '/' !!!
search_url = 'http://www.jidajia.com/e/search/index2.php'
pic_path = './img/'
csv_path = './csv_files/'


class Error:
    dict = {
        'not_200': 'not200',
        'timeout': 'timeout',
        'connection_error': 'connectionError',
        'unexpected': 'unexpectedError',
        'error': 'error',
    }

    def __init__(self, x):
        self.error = dict[x]


def get_html(url, code="utf-8", __mode__=__get__, word=''):
    try:
        if __mode__ == __get__:
            r = requests.get(url, headers=headers, timeout=time)
        elif __mode__ == __post__:
            # search character
            data = {"keyboard": word, "sort": _word_type}
            r = requests.post(url, headers=headers, data=data, timeout=time)
        else:
            r = ''
        r.raise_for_status()
        r.encoding = code
        return r.text
    except requests.exceptions.HTTPError:
        print("Getting HTML Error: not 200 code. Code: 9\turl={url}\t错误信息：{err}")
        return Error('not_200')
    except requests.exceptions.ReadTimeout:
        print(f"Getting HTML  Timeout: {url} (read timeout={time}). Code: 10")
        return Error('timeout')
    except requests.exceptions.ConnectionError as err:
        print(f"Connection Error. Code: 12. Message: {err}")
        return Error('connection_error')
    except Exception as err:
        print(f"Getting HTML  Error: failed to get. Code: 5 (Maybe Network Error.)\turl={url}\t错误信息：{err}")
        return Error('unexpected')


def find_pics(url, html=''):
    pics_list = []
    word_list = []
    try:
        if html == '':
            html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        box = soup.find("div", {"class": "writer_box"})
        ul = box.find('ul')
        pics = ul.find_all("a")
        ch = ul.find_all("p", {"class": "writer"})

        for i in range(len(pics)):
            pics_list.append(pics[i]['href'])
            word_list.append(ch[i].string.split("（")[0])
    except Exception as err:
        write_csv([url, f"Find_pics_of_page_error:{str(err).split(' ')[0]}"], 'read_error')
    return pics_list, word_list


def find_pages(html, _type='single_word'):
    soup = BeautifulSoup(html, "html.parser")
    try:
        pages = soup.find("div", {"class": "page"}).find_all('a')
        url_family = pages[-1]['href']
        if _type == 'single_word':
            last_page = url_family.split('-')
        elif _type == 'home':
            last_page = url_family.split('_')
        else:
            print("Wrong type. Error!")
            last_page = 0
            exit(-1)
    except Exception as err:
        last_page = 0
    return last_page


def fpow(url, no, html=''):
    # find pics of a word
    if html == '':
        html = get_html(url)
    last_page = find_pages(html)
    if last_page != 0:
        # 不止一页的情形，构建页面列表
        _max = last_page[1].split('.')[0]
        page_list = [f"{last_page[0]}.html"]
        pics_list = []
        word_list = []
        for i in range(2, int(_max) + 1):
            url_i = f"{last_page[0]}-{i}.html"
            page_list.append(url_i)
        for page in page_list:
            page_url = homeurl + page
            results = find_pics(page_url)
            pics_list += results[0]
            word_list += results[1]
    else:
        pics_list, word_list = find_pics(url, html=html)
    l = len(pics_list)
    df = pd.DataFrame({"No": list(range(no, no + l)), "Word": word_list, 'URL': pics_list, 'Status': ['N'] * l},
                      columns=['No', 'Word', 'URL', "Status"])
    df.to_csv(csv_path + 'raw_data.csv', index=False, encoding='utf-8-sig', mode='a', header=False)
    return no + l


def download_pic(pic_url, no, num_i, word):
    try:
        pic = requests.get(pic_url, timeout=10).content
        with open(f"{pic_path}{str(no)}.{pic_url.split('.')[-1]}", 'wb') as f:
            f.write(pic)
            f.close()
        write_csv([no, word, pic_url, 'Succeeded'], csv_name='data')
        print(f"#{no :3d}({word})  succeeded.")
        no += 1
        num_i += 1
    except requests.exceptions.ReadTimeout:
        print(f"{pic_url}' (read timeout={time})")
        write_csv([pic_url, 'timeout'], 'download_error')
        write_csv([no, word, pic_url, 'Failed'], csv_name='data')
    except Exception as err:
        print(f"Download failed code: 1\t错误信息：{err}")
        write_csv([pic_url, str(err).split(' ')[0]], 'download_error')
    return no, num_i


def write_csv(rows, csv_name):
    with open(f"{csv_path}{csv_name}.csv", 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(rows)
        f.close()


def init_csv(name, title):
    with open(csv_path + name + '.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(title)
        f.close()


def set_dir(filepath, _del=False, file=''):
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
            if file != '':
                with open(filepath + file, 'w') as f:
                    f.write('file here.')
                    f.close()
        else:
            pass


def find_words(page_list):
    word_list = []
    i = 1
    _max = len(page_list)
    for page in page_list:
        # 楷书的某一页
        print(f"Reading page {i:3d}/{_max}.", end="")
        # if page_html != 'timeout':
        page_number = page.split('_')[1].split('.')[0]
        try:
            word_list += find_pics(page)[0]
            print(f"{'.' * 10}Success!")
            write_csv([f'Page {page_number}', page, 'Success'], 'pages')
        except Exception as err:
            print(f"{'.' * 10}Failed! Error: {err}")
            write_csv([f'Page {page_number}', page, 'Failed', str(err).split(' ')[0]], 'pages')
        i += 1
    return word_list


def spider_all(_type='kaishu', __mode__=__count__, __from__='', __init=False):
    if __from__ == '':
        url = f'{homeurl}/{_type}/'
        html = get_html(url)
        init_csv('read_error', ['URL', 'Reason'])
        init_csv('pages', ['Page', 'URL', 'Status', 'Remark'])

        try:
            # 构建页面列表
            last_page = find_pages(html, _type='home')  # 读取总页面数
            _all, _ = find_number_of_page(html)  # 读取总字数
            # print(last_page)
            _max = last_page[1].split('.')[0]
            page_list = [f"{homeurl}{last_page[0]}.html"]

            for i in range(2, int(_max) + 1):
                url_i = f"{homeurl}{last_page[0]}_{i}.html"
                page_list.append(url_i)

            word_list = find_words(page_list)

            count = 0
            no = 1
            if __mode__ == __count__:
                init_csv('words_count', title=['word', 'count', 'url'])
                init_csv('error_words', title=['url', 'Reason'])
                for word_page in word_list:
                    count, no, _ = count_word(homeurl + word_page, count, no, _all)
                print(f"{count} in total!")

            elif __mode__ == __download__:
                init_csv('data', title=['No.', 'Word', 'URL', 'Status'])
                init_csv('download_error', title=['url', 'reason'])
                i = 1
                for word_page in word_list:
                    print(f"Downloading word #{i}/{_all}.")
                    word_url = homeurl + word_page
                    try:
                        no = fpow(word_url, no)
                    except Exception as err:
                        print(f"Download Error. Code 15. Message: {err}")
                        write_csv([word_url, f'Reading_word_error:{str(err).split(" ")[0]}'], 'read_error')
                    i += 1
            elif __mode__ == __record__:
                init_csv("wordlist_all", ['URL', 'Status'])
                for word_page in word_list:
                    word_url = homeurl + word_page
                    write_csv([word_url, 'N'], 'wordlist_all')
        except Exception as err:
            print(f"Error code: 11. Message: {err}")
            write_csv([url, f'Error11:{str(err).split(" ")[0]}'], 'read_error')

    elif __from__ == __local__:
        if __mode__ == __fix_page__:
            with open(csv_path + 'pages.csv', 'r+') as f:
                reader = csv.reader(f)
                # failed_pages = [row for row in reader if row[2] == 'Failed']
                failed_pages = []
                for row in reader:
                    if row[2] == 'Failed':
                        row[2] = 'Retried'
                        failed_pages.append(row[1])
                f.close()
            word_list = find_words(failed_pages)
            for word_page in word_list:
                word_url = homeurl + word_page
                write_csv([word_url, 'N'], 'wordlist_all')

        elif __mode__ == __count__:
            init_csv('error_words', title=['url', 'Reason'])
            if __init:
                no = 1
                count = 0
                init_csv('words_count', title=['word', 'count', 'url'])
            else:
                df = pd.read_csv(csv_path + 'words_count.csv')
                tail = df.tail(1)
                no = tail.index.stop + 1
                count = int(tail['count'].values[0].split("/")[1])
            df = pd.read_csv(csv_path + 'wordlist_all.csv')
            # _all = df.value_counts('Status')["N"]
            for row in df.values:
                if row[1] == 'N':
                    # count, no, status = count_word(row[0], count, no, _all)
                    count, no, status = count_word(row[0], count, no, _all=df.value_counts('Status')["N"])
                    if status:
                        row[1] = 'Y'
                    else:
                        pass
                else:
                    pass
            df.to_csv(csv_path + 'wordlist_all.csv', index=False, encoding='utf-8-sig')

        elif __mode__ == __get_picture_list__:
            if __init:
                # 初始化
                init_csv('raw_data', title=['No.', 'Word', 'URL', 'Status'])
                init_csv('read_error', title=['URL', 'Reason'])
                no = 1
            else:
                data = pd.read_csv(csv_path + 'raw_data.csv')
                tail = data.tail(1)
                no = tail.index.stop + 1        # no: data中已有的信息条数
                # no = tail['NO.'] + 1
            wa = pd.read_csv(csv_path + 'wordlist_all.csv')
            i = 1
            _all = wa.value_counts('Status')['N']
            for row in wa.values:
                no = get_pic_lists(row, _all, no, 1, 0, i, wa, 'wordlist_all.csv')
                i += 1

        elif __mode__ == __fix_raw_data__:
            data = pd.read_csv(csv_path + 'raw_data.csv')
            tail = data.tail(1)
            no = tail.index.stop + 1            # no: data中已有的信息条数
            # no = tail['NO.'] + 1
            df = pd.read_csv(csv_path + 'read_error.csv')
            _all = df.value_counts('Status')['N']           # 统计Status='N'的个数
            i = 1
            # 遍历read_error.csv中的所有行
            for row in df.values:
                if row[2] == 'N':
                    no = get_pic_lists(row, _all, no, 2, 0, i, df, 'read_error.csv')
                    i += 1


def get_pic_lists(row, _all, no, ps, pu, i, df, file):
    # ps: position of Status
    # pu: position of URL
    if row[ps] == 'N':
        print(f"Getting pictures of word #{i}/{_all}{'.' * 10}", end='')
        word_page_html = get_html(row[pu])
        if type(word_page_html) != Error:
            no = fpow(row[pu], no, word_page_html)
            if file == "read_error.csv":
                df.drop(i-1, inplace=True)
            elif file == "wordlist_all.csv":
                row[ps] = 'Y'
            df.to_csv(csv_path + file, index=False, encoding='utf-8-sig')
            print(f'{"." * 5}done!')
        else:
            if file == "wordlist_all.csv":
                write_csv([row[pu], word_page_html.error], 'read_error')
            else:
                pass
            print(f'{"." * 5}failed...please check read_error')
    else:
        pass
    return no


def find_number_of_page(html):
    soup = BeautifulSoup(html, "html.parser")
    ch = soup.find_all("p", {"class": "writer"})
    div = soup.find('div', {'class': 'page'})
    # print(div)
    b = div.find('b')
    if b is None:
        number = len(ch)
    else:
        number = int(b.string)
    return number, ch


def count_word(url, _count, no, _all):
    html = get_html(url)
    try:
        number, ch = find_number_of_page(html)
        _count += number
        word = f"{ch[0].string.split('（')[0]}({no}/{_all})"
        row2 = f"{number}/{_count}"
        print(f"{word}:{row2}")
        write_csv([word, row2, url], 'words_count')
        no += 1
        status = True
    except Exception as err:
        print(f"Error code: 13. URL:{url}\t异常信息：{err}")
        write_csv([url, str(err).split(' ')[0]], 'error_words')
        status = False
    return _count, no, status


def main():
    # word = '芋'

    # set_dir(pic_path, _del=True, file='.pnghere.md')
    # set_dir(csv_path)
    # fpow(word=word, __mode__=__post__)

    # spider_all()
    # spider_all( __mode__=__download__)
    # spider_all( __mode__=__record__)
    # spider_all( __mode__=__fix_page__, __from__=__local__)
    # spider_all( __from__=__local__, __mode__=__count__, __init=False)
    # spider_all(__mode__=__get_picture_list__, __from__=__local__, __init=True)
    spider_all(__mode__=__fix_raw_data__, __from__=__local__)


if __name__ == "__main__":
    main()
