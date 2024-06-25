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
        debug_text = ""
        if verbose:
            debug_text+="text: "+text+"\n"
        score = 0
        for token in self.tokenizer.tokenize(text):
            if token.base_form in self.dict1:
                s = self.dict1[token.base_form][0]
                if verbose:
                    debug_text+="[dict1] "+str(token.base_form)+" "+ str(s)+"\n"
                score += s
        if verbose:
            return score, debug_text
        else:
            return score

    def estimate_v2(self, text: str, *, verbose=False) -> int:
        debug_text=""
        score ,d_text= self.estimate_v1(text, verbose=verbose)

        debug_text+=d_text
        is_pending = False
        pending = []
        for token in self.tokenizer.tokenize(text):
            debug_text+=str(token)+"\n"
            flag=False
            if(token.base_form =="落ち込む"):
                print("||||||||||||")
                flag=True
            if token.base_form in self.dict2:
                if flag:
                    print("#####")
                    print(token)
                is_pending = True

            if is_pending:
                pending.append(token.base_form)

                settled = True
                if(flag):
                    print(pending)
                    print(self.dict2[pending[0]])
                for record in self.dict2[pending[0]]:
                    debug_text+="[dict2]found "+str(record)+"\n"
                    if pending == record[0]:
                        s = record[1]
                        if verbose:
                            debug_text+="[dict2] "+str(pending)+str(s)+"\n"
                        score += s
                        break
                    elif partial_match(pending, record[0]):
                        settled = False

                if settled:
                    is_pending = False
                    pending = []
        if verbose:
            return score, debug_text
        return score
