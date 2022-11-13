import json

import pandas as pd
import sys


def readfile(filename):
    with open(filename) as f:
        file = f.readlines()
    return file


def create_df(file):
    data = []
    for line in file:
        lst = line.split()
        data.append(lst)
    df = pd.DataFrame(data=data)
    df = df.drop([1, 2, 3, 4, 7, *range(10, 43)], axis=1)
    df.columns = ['ip', 'method', 'url', 'status', 'requests_amount']
    df['method'] = df['method'].str[1:]
    ind_missing = df[df['requests_amount'].str.contains('-')].index
    df = df.drop(ind_missing, axis=0)
    ind_missing = df[df['method'].str.len() > 20].index
    df = df.drop(ind_missing, axis=0)
    df['requests_amount'] = df['requests_amount'].astype(int)
    return df


def get_res(df):
    task2_df = get_task2_df(df)
    task3_df = get_task3_df(df, 10)
    task4_df = get_task4_df(df, 5)
    task5_df = get_task5_df(df, 5)

    res = {
        1: {'amount': len(df)},
        2: {},
        3: {},
        4: {},
        5: {}
    }

    for method, num in task2_df.items():
        res[2][method] = num
    for url, num in task3_df.items():
        res[3][url] = num
    for column in task4_df:
        res[4][column] = []
        for row in task4_df[column]:
            res[4][column].append(row)
    for ip, num in task5_df.items():
        res[5][ip] = num

    return res


def write_results(filename, df, jsonify=False):
    if not jsonify:
        with open(''.join((filename, '.txt')), 'w') as file:
            file.writelines(f"2. Общее количество запросов по типу, например: GET - 20, POST - 10 и т.д.\n"
                            f"{str(get_task2_df(df))}"
                            f"\n\n3. Топ 10 самых частых запросов\n"
                            f"{str(get_task3_df(df, 10))}"
                            f"\n\n5. Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой\n"
                            f"{str(get_task5_df(df, 5))}")
    else:
        res = get_res(df)
        with open(''.join((filename, '.json')), "w", encoding="utf-8") as file:
            json.dump(res, file)


def get_task2_df(df):
    return df['method'].value_counts()


def get_task3_df(df, length):
    return df['url'].value_counts().head(length)


def get_task4_df(df, length):
    return df[df['status'].str.contains('4..')].sort_values(by='requests_amount', ascending=False).head(length)


def get_task5_df(df, length):
    return df[df['status'].str.contains('5..')]['ip'].sort_values().value_counts().head(length)


def get_data(filepath):
    file = readfile(filepath)
    df = create_df(file)

    return get_res(df)


def main():
    jsonify = '--json' in sys.argv
    filename_logs = 'access.log'
    filename_res = 'results'

    file = readfile(filename_logs)
    df = create_df(file)

    write_results(filename_res, df, jsonify)


if __name__ == '__main__':
    main()
