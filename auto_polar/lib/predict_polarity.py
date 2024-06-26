from janome.tokenizer import Tokenizer
import dataclasses
from enum import Enum
import abc
import re
import jaconv

KATAKANA_PAT = re.compile(r"[\u30A1-\u30FF]+")


def partial_match(tokens: list, reference: list) -> bool:
    if len(tokens) > len(reference):
        return False
    for i in range(len(tokens)):
        if tokens[i] != reference[i]:
            return False
    return True


def is_katakana(s: str) -> bool:
    return KATAKANA_PAT.fullmatch(s) is not None


def get_part_of_speech(token) -> str:
    # Tokenizerの中身でtokenがどのように定義されているかあとで確認して書いておく
    return token.part_of_speech.split(",")[0]


class MatchType(Enum):
    FULL = 1
    PARTIAL = 2
    NONE = 3


@dataclasses.dataclass
class QueryResult:
    match_type: MatchType
    score: int  # 0 if match_type is PARTIAL or NONE


class Dict(abc.ABC):
    @abc.abstractmethod
    def query(self, token) -> QueryResult:
        pass


class Dict1(Dict):
    def __init__(self, dict1: dict) -> None:
        self.dict1 = dict1

    def query(self, token: str) -> QueryResult:
        if token in self.dict1:
            return QueryResult(MatchType.FULL, self.dict1[token][0])
        return QueryResult(MatchType.NONE, 0)


class Dict2(Dict):
    def __init__(self, dict2: dict) -> None:
        self.dict2 = dict2

    def query(self, tokens: list[str]) -> QueryResult:
        pairtial = False
        if tokens[0] in self.dict2:
            for record in self.dict2[tokens[0]]:
                if tokens == record[0]:
                    return QueryResult(MatchType.FULL, record[1])
                elif partial_match(tokens, record[0]):
                    pairtial = True

        if pairtial:
            return QueryResult(MatchType.PARTIAL, 0)
        else:
            return QueryResult(MatchType.NONE, 0)


class PolarEstimator:
    def __init__(self, dict1: Dict, dict2: Dict) -> None:
        self.dict1 = dict1
        self.dict2 = dict2
        self.tokenizer = Tokenizer()

    def negative_auxiliary_verb_checker(self, token) -> bool:
        denial_list = ["ない", "ぬ", "ん"]
        denial_type = "助動詞"
        return token.base_form in denial_list and get_part_of_speech(token) == denial_type

    def estimate_v1(self, text: str, *, verbose=False) -> int:
        if verbose:
            print("text:", text)
        score = 0
        for token in self.tokenizer.tokenize(text):
            res = self.dict1.query(token.base_form)
            if res.match_type == MatchType.FULL:
                if verbose:
                    print("[dict1] ", token.base_form, res.score)
                score += res.score
        return score

    def estimate_v2(self, text: str, *, verbose=False) -> int:
        score = self.estimate_v1(text, verbose=verbose)
        prev_score = [0, False]

        pending = []
        for token in self.tokenizer.tokenize(text):
            for tokens in pending:
                tokens.append(token.base_form)

            if self.negative_auxiliary_verb_checker(token):
                if prev_score[1]:
                    score += -1 * prev_score[0] * 2
                    continue
            prev_score = [0, False]

            res = self.dict2.query([token.base_form])
            match res.match_type:
                case MatchType.FULL:
                    if verbose:
                        print("[dict2] ", [token.base_form], res.score)
                    score += res.score
                    prev_score = [res.score, True]
                case MatchType.PARTIAL:
                    pending.append([token.base_form])
                case MatchType.NONE:
                    if is_katakana(token.base_form):
                        hira_token = jaconv.kata2hira(token.base_form)
                        res = self.dict2.query([hira_token])
                        if res.match_type == MatchType.FULL:
                            if verbose:
                                print("[dict2] ", [hira_token], res.score)
                            score += res.score
                            prev_score = [res.score, True]

            drop_list = []
            for i, tokens in enumerate(pending):
                res = self.dict2.query(tokens)
                match res.match_type:
                    case MatchType.FULL:
                        if verbose:
                            print("[dict2] ", tokens, res.score)
                        score += res.score
                        prev_score = [res.score, True]
                        drop_list.append(i)
                    case MatchType.PARTIAL:
                        pass
                    case MatchType.NONE:
                        drop_list.append(i)
            for i in drop_list:
                pending.pop(i)
        return score

    def estimate_v3(self, text: str, *, verbose=False) -> int:
        buf = ""
        denial_list = ["ない", "ぬ", "ん"]
        denial_type = "助動詞"
        score = 0
        for token in self.tokenizer.tokenize(text):
            if (token.base_form in denial_list) and get_part_of_speech(
                token
            ) == denial_type:
                score_e2 = self.estimate_v2(buf, verbose=verbose)
                if verbose:
                    print(
                        '[e_v3]"'
                        + buf
                        + '":'
                        + str(score_e2)
                        + "*"
                        + '"'
                        + token.surface
                        + '":-1'
                    )
                score += -1 * score_e2
                buf = ""
            buf += token.surface
        if len(buf) != 0:
            score_e2 = self.estimate_v2(buf, verbose=verbose)
            if verbose:
                print('[e_v3]"' + buf + '":' + str(score_e2))
            score += score_e2
        return score

    def estimate_v4(self, text: str, *, verbose=False) -> int:
        buf = ""
        contradictory_list = [
            "しかし",
            "けど",
            "ただ",
            "だが",
            "しかしながら",
            "けれど",
            "けれども",
            "だけど",
            "だけども",
            "そうではあるが",
            "それでも",
            "でも",
            "ではあるが",
            "にもかかわらず",
            "ところが",
            "ですが",
            "ものの",
            "しかるに",
            "とはいうものの",
            "のに",
            "なのに",
            "それなのに",
            "とはいえ",
            "そうはいうものの",
            "でも",
            "そのくせ",
        ]
        conjunction_type = ["接続詞", "助詞"]
        score = 0
        for token in self.tokenizer.tokenize(text):
            if get_part_of_speech(token) == conjunction_type[0] or (
                get_part_of_speech(token) in conjunction_type
                and token.surface in contradictory_list
            ):
                if token.base_form in contradictory_list:
                    score_e3 = self.estimate_v3(buf, verbose=verbose)
                    if verbose:
                        print(
                            '[e_v4]"'
                            + buf
                            + '":'
                            + str(score_e3)
                            + "*"
                            + '"'
                            + token.surface
                            + '":-1'
                        )
                    score += -1 * score_e3
                else:
                    score_e3 = self.estimate_v3(buf, verbose=verbose)
                    if verbose:
                        print(
                            '[e_v4]"'
                            + buf
                            + '":'
                            + str(score_e3)
                            + "*"
                            + '"'
                            + token.surface
                            + '":1'
                        )
                    score += score_e3
                buf = ""
            buf += token.surface
        if len(buf) != 0:
            score_e3 = self.estimate_v3(buf, verbose=verbose)
            if verbose:
                print('[e_v4]"' + buf + '":' + str(score_e3))
            score += score_e3
        return score
