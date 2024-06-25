from janome.tokenizer import Tokenizer
import dataclasses
from enum import Enum
import abc


def partial_match(tokens: list, reference: list) -> bool:
    if len(tokens) > len(reference):
        return False
    for i in range(len(tokens)):
        if tokens[i] != reference[i]:
            return False
    return True


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

        pending = []
        for token in self.tokenizer.tokenize(text):
            for tokens in pending:
                tokens.append(token.base_form)

            res = self.dict2.query([token.base_form])
            match res.match_type:
                case MatchType.FULL:
                    if verbose:
                        print("[dict2] ", [token.base_form], res.score)
                    score += res.score
                case MatchType.PARTIAL:
                    pending.append([token.base_form])
                case MatchType.NONE:
                    pass

            drop_list = []
            for i, tokens in enumerate(pending):
                res = self.dict2.query(tokens)
                match res.match_type:
                    case MatchType.FULL:
                        if verbose:
                            print("[dict2] ", tokens, res.score)
                        score += res.score
                        drop_list.append(i)
                    case MatchType.PARTIAL:
                        pass
                    case MatchType.NONE:
                        drop_list.append(i)
            for i in drop_list:
                pending.pop(i)
        return score
