# count_polarity_statistics.py

def token_to_polarity(token, dict1, dict2):
    """
    単語を極性値に変換する関数
        Args:
            token: 単語(string)
            dict1: load_dictionary.pyで作成した辞書1
            dict2: load_dictionary.pyで作成した辞書2
        Returns:
            polarity: [一致度(string), 極性値(float?)]の配列
                一致度：full(完全一致) / partial(部分一致) / none(不一致)
                極性値：fullの場合+1/0/-1 partialの場合は部分一致した極性値の平均値 noneの場合は0
    """
    ans = ["none", 0]
    # dict1を検索
    if token in dict1:
        ans = ["full", dict1[token][0]]
        return ans

    # dict2を検索
    partial_scores = []
    if token in dict2:
        for record in dict2[token]:
            if len(record[0]) == 1 and token in record[0]: 
                ans = ["full", record[1]]
                break
            elif len(record[0]) > 1 and token in record[0]:
                ans = ["partial", 0]
                partial_scores.append(record[1])
    if ans[0] == "partial":
        ans[1] = sum(partial_scores) / len(partial_scores)
    return ans

