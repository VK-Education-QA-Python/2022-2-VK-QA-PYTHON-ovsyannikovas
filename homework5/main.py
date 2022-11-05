import json

import pandas as pd
import sys


def pytest_addoption(parser):
    parser.addoption("--json", action="store_true")


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
    return df


def write_results(filename, task2_df, task3_df, task5_df, jsonify=False):
    if not jsonify:
        with open(''.join((filename, '.txt')), 'w') as file:
            file.writelines(f"2. Общее количество запросов по типу, например: GET - 20, POST - 10 и т.д.\n"
                            f"{str(task2_df)}"
                            f"\n\n3. Топ 10 самых частых запросов\n"
                            f"{str(task3_df)}"
                            f"\n\n5. Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой\n"
                            f"{str(task5_df)}")
    else:
        res = {
            2: {},
            3: {},
            5: {}
        }
        for method, num in task2_df.items():
            res[2][method] = num
        for url, num in task3_df.items():
            res[3][url] = num
        for ip, num in task5_df.items():
            res[5][ip] = num
        with open(''.join((filename, '.json')), "w", encoding="utf-8") as file:
            json.dump(res, file)


def main():
    jsonify = '--json' in sys.argv
    filename_logs = 'access.log'
    filename_res = 'results'

    file = readfile(filename_logs)
    df = create_df(file)

    task2_df = df['method'].value_counts()
    task3_df = df['url'].value_counts().head(10)
    task5_df = df[df['status'].str.contains('5..')]['ip'].sort_values().value_counts().head(5)

    write_results(filename_res, task2_df, task3_df, task5_df, jsonify)


if __name__ == '__main__':
    main()
