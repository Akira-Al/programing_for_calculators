from janome.tokenizer import Tokenizer
import pandas as pd
#address = "../../data/data.txt"

def tokenized(data_address) :
    '''
    data.txtを読み込み、形態素解析を行う
        Args:
            data_address: data.txtのファイルパス
        Return
            tokens: 文ごとのjanome.tokenizer.Tokenオブジェクトのジェネレータの配列
        
    '''
    with open(data_address, "r", encoding="UTF-8") as f:
        data_text = f.readlines()
    tokens = [Tokenizer().tokenize(s) for s in data_text ]
    return tokens

def convert_words(data_address):
    '''
    data.txtを読み込み、単語に分解する
        Args:
            data_address:data.txtのファイルパス
        Returns:
            words: dataに含まれる文の単語の2次元配列(string型)
    '''
    with open(data_address, "r", encoding="UTF-8") as f:
        data_text = f.readlines()
    tokens = [Tokenizer().tokenize(s) for s in data_text]
    words = [[] for _ in range(len(tokens))]
    for i in range(len(tokens)):
        for s in tokens[i]:
            words[i].append(str(s.surface))
    return words

