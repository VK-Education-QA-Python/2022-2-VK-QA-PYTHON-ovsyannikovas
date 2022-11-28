import pandas as pd


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


def get_task2_df(df):
    return df['method'].value_counts()


def get_task3_df(df, length):
    return df['url'].value_counts().head(length)


def get_task4_df(df, length):
    return df[df['status'].str.contains('4..')].sort_values(by='requests_amount', ascending=False).head(length)


def get_task5_df(df, length):
    return df[df['status'].str.contains('5..')]['ip'].sort_values().value_counts().head(length)


def get_task1_dict(filepath):
    file = readfile(filepath)
    df = create_df(file)

    return {'amount': len(df)}


def get_task2_dict(filepath):
    file = readfile(filepath)
    df = create_df(file)
    task2_df = get_task2_df(df)
    res = {}
    for method, num in task2_df.items():
        res[method] = num

    return res


def get_task3_dict(filepath):
    file = readfile(filepath)
    df = create_df(file)
    task3_df = get_task3_df(df, 10)
    res = {}
    for url, num in task3_df.items():
        res[url] = num

    return res


def get_task4_dict(filepath):
    file = readfile(filepath)
    df = create_df(file)
    task4_df = get_task4_df(df, 5)
    res = {}
    for column in task4_df:
        res[column] = []
        for row in task4_df[column]:
            res[column].append(row)

    return res


def get_task5_dict(filepath):
    file = readfile(filepath)
    df = create_df(file)
    task5_df = get_task5_df(df, 5)
    res = {}
    for ip, num in task5_df.items():
        res[ip] = num

    return res
