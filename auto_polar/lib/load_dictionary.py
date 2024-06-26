import pandas as pd
from janome.tokenizer import Tokenizer


def polar2score(p):
    """
    dictionary1.txtの極性をスコアに変換する
        Args:
            p(str): dictionary1.txtに書かれている極性
        Returns:
            int: p->1, n->-1, dictionary1.txtの極性の欄に書かれていたp,n以外の文字->0, 予想外の文字->エラーを吐く
    """
    match p:
        case "p":
            return 1
        case "n":
            return -1
        case "e":
            return 0
        case "?p?n":
            return 0
        case "?e":
            return 0
        case "o":
            return 0
        case "?p?e":
            return 0
        case "　":
            return 0
        case "a":
            return 0
        case "?p":
            return 0
        case _:
            raise ValueError(f"Invalid polar: {p}")  # 予想外の文字に対するエラー


def load_dict1(dict1):
    """
    dictionary1.txtを読み込み、辞書に変換する
        Args:
            dict1: dictionary1.txtのファイルパス
        Returns:
            dict: テキストをkeyに、(スコア, 説明)のタプルをvalueとする辞書
        Examples:
            >>> d1 = load_dict1('../../data/dictionary1.txt')
            >>> print(d1)
            (0, '〜である・になる（状態）客観')
    """
    reference1_df = pd.read_csv(
        dict1, sep="\t", header=None
    )  # TSVファイルをデータフレームに変換
    reference1_df.columns = ["text", "polar", "description"]  # 列名を指定
    reference1_dict = {
        row[0]: (polar2score(row[1]), row[2]) for row in reference1_df.values
    }  # 辞書に変換
    return reference1_dict


tkn = Tokenizer()  # インスタンス作成


def load_dict2(dict2):
    """
    dictionary2.txtを読み込み、辞書に変換する
        Args:
            dict2: dictionary2.txtのファイルパス
        Returns:
            dict: テキストをkeyに、(スコア, トークンリスト, タイプ)のタプルのリストをvalueとする辞書
        Examples:
            >>> d2 = load_dict2('../../data/dictionary2.txt')
            >>> print(d2['あきれる'])
            [(['あきれる'], -1, '経験'), (['あきれる', 'た'], -1, '経験'), (['あきれる', 'て', 'もの', 'が', '言える', 'ない'], -1, '評価')]
    """
    reference2_df = pd.read_csv(
        dict2, sep="\t", header=None
    )  # TSVファイルをデータフレームに変換
    reference2_df.columns = ["polar", "text"]  # 列名を指定
    reference2_df["PosiNega"] = reference2_df["polar"].str.extract(
        r"(ポジ|ネガ)"
    )  # 極性を抽出
    reference2_df["type"] = reference2_df["polar"].str.extract(
        r"（(.+)）"
    )  # タイプ(経験or評価)を抽出
    reference2_df["PosiNega"] = reference2_df["PosiNega"].map(
        {"ポジ": 1, "ネガ": -1}
    )  # 極性をスコアに変換
    reference2_dict = {}  # 辞書を作成
    for row in reference2_df.values:
        text = str(row[1]).replace(" ", "")
        words = tkn.tokenize(text)
        tokens = []
        for s in words:
            tokens.append(str(s.base_form))
        if tokens[0] in reference2_dict:
            reference2_dict[tokens[0]].append((tokens, row[2], row[3]))  # 辞書に追加
        else:
            reference2_dict[tokens[0]] = [(tokens, row[2], row[3])]  # 新しいkeyを作成
    return reference2_dict


def load_PnJa(PnJa):
    """
    pn_ja.txtを読み込み、辞書に変換する
        Args:
            PnJa: pn_ja.txtのファイルパス
        Returns:
            dict: テキストをkeyに、(スコア, 読み, 品詞)のタプルをvalueとする辞書
        Examples:
            >>> d3 = load_PnJa('../../data/pn_ja.txt')
            >>> print(d3)
            (0.999995, 'よい', '形容詞')
    """
    referencePnJa_df = pd.read_csv(
        PnJa, sep=":", header=None
    )  # CSVファイルをデータフレームに変換
    referencePnJa_df.columns = ["text", "reading", "word_class", "polar"]  # 列名を指定
    referencePnJa_dict = {
        row[0]: (row[3], row[1], row[2]) for row in referencePnJa_df.values
    }  # 辞書に変換
    return referencePnJa_dict
