# import numpy as np
import pandas as pd
import utils
# import matplotlib.pyplot as plt
from collections import Counter
# import multiprocessing as mp
from tqdm import tqdm

root = utils.get_project_path()
csv_path = f'{root}/data/csv_files'
sel = 100
csv_file = f"{csv_path}/data_{sel}.csv"
df = pd.read_csv(f'{csv_path}/data.csv', encoding='utf-8')
index2label = dict(zip(df['No.'], df['Word']))
counter = Counter(df['Word'])  # class: Counter


def err_call_back(err):
    print(f'出错啦~ error：{str(err)}')


def func(word, n):
    if counter[word] > sel:
        n += 1
    else:
        df.drop(df[df.Word == word].index, inplace=True)
    return n

def main(sel=sel):
    # pbar = tqdm(total=len(counter.values()))
    # update = lambda *args: pbar.update()
    # pool = mp.Pool(10)
    # for word in counter.keys():
    #     pool.apply_async(func, args=(str(word),), callback=update, error_callback=err_call_back)
    # # pool.map_async(func, counter.keys(), callback=update)
    # pool.close()
    # pool.join()
    n = 0
    for word in tqdm(counter.keys()):
        n = func(word, n)
    print(f'{n} words more than {sel}.')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"Output file: {csv_file}!")


if __name__ == '__main__':
    li = [150, 200, 300]
    for s in li:
        main(s)
