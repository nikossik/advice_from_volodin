import pandas as pd
from string import ascii_letters
from random import randint

def random_name():
    res = ''

    for i in range(32):
        res += ascii_letters[randint(0,51)]

    return res


def shuffle():
    df = pd.read_csv('data.csv')
    df = df.sample(frac=1)
    name = random_name()
    df.to_csv(f'user-data/{name}.csv')

    return name

def give_advice(filename, index):
    df = pd.read_csv(f'user-data/{filename}.csv')
    res = df['text'].tolist()[index]
    df = df.append({'text' : res}, ignore_index=True)
    df.to_csv(f'user-data/{filename}.csv', index=False)

    return res