import re
import pandas as pd


def readfile():
    with open('access.log') as f:
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
    # df['requests_amount'] = df['requests_amount'].astype(int)
    return df


def main():
    filename = 'access.log'
    file = readfile()
    df = create_df(file)
    print(df.dtypes)
    print(df['method'].value_counts())
    print(df['url'].value_counts().head(10))
    print(df[df['status'].str.contains('5..')])#.sort_values(by='requests_amount', ascending=False).head(5))


if __name__ == '__main__':
    main()
