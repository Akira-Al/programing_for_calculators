from janome.tokenizer import Tokenizer


def partial_match(tokens: list, reference: list) -> bool:
    for i in range(len(tokens)):
        if tokens[i] != reference[i]:
            return False
    return True


class PolarEstimator:
    def __init__(self, dict1: dict, dict2: dict) -> None:
        self.dict1 = dict1
        self.dict2 = dict2
        self.tokenizer = Tokenizer()

    def estimate_v1(self, text: str, *, verbose=False) -> int:
        if verbose:
            print("text:", text)
        score = 0
        for token in self.tokenizer.tokenize(text):
            if token.base_form in self.dict1:
                s = self.dict1[token.base_form][0]
                if verbose:
                    print("[dict1] ", token.base_form, s)
                score += s
        return score

    def estimate_v2(self, text: str, *, verbose=False) -> int:
        score = self.estimate_v1(text, verbose=verbose)

        is_pending = False
        pending = []
        for token in self.tokenizer.tokenize(text):
            if token.base_form in self.dict2:
                is_pending = True

            if is_pending:
                pending.append(token.base_form)

                settled = True
                for record in self.dict2[pending[0]]:
                    if pending == record[0]:
                        s = record[1]
                        if verbose:
                            print("[dict2] ", pending, s)
                        score += s
                        break
                    elif partial_match(pending, record[0]):
                        settled = False

                if settled:
                    is_pending = False
                    pending = []
        return score
