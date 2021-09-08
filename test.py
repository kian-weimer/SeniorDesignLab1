import pandas as pd
from pandas.errors import EmptyDataError


def archive_temp(temp):
    import os.path
    if os.path.isfile('temps.csv'):
        try:
            df = pd.read_csv('temps.csv')
            pd.read_csv('temps.csv', usecols=['Temp(F)', 'Temp(C)'])
            df2 = pd.DataFrame([[C2F(temp), temp]], columns=['Temp(F)', 'Temp(C)'], index=['x'])
            df = df.append(df2, ignore_index=True)
        except EmptyDataError as e:
            df = pd.DataFrame([[C2F(temp), temp]], columns=['Temp(F)', 'Temp(C)'], index=['x'])
    else:
        df = pd.DataFrame([[C2F(temp), temp]], columns=['Temp(F)', 'Temp(C)'], index=['x'])

    print(len(df.index))
    while len(df.index) > 300:
        df = df.iloc[1:]
        print(1)
    print(df)
    df.to_csv('temps.csv', mode='w', index=False, header=True)


def F2C(degrees):
    return (degrees - 32)*5/9


def C2F(degrees):
    return degrees*9/5 + 32


if __name__ == '__main__':
    archive_temp(75.4)
