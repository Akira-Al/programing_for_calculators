import unittest
from auto_polar.lib import load_dictionary
from pathlib import Path


class TestLoadDictionary(unittest.TestCase):
    def test_load_dictionary1(self):
        """
        dictionary_loaderモジュール内のload_dict1関数のテスト
        dictionary.txtと同様の形式のファイルから辞書が正しくloadされるかチェックする
        """
        input_file = (
            Path(__file__).parent
            / "test_load_dictionary_files"
            / "test_dictionary1.txt"
        )
        expected_output = {
            "２，３日": (0, "〜である・になる（状態）客観"),
            "10%": (0, "〜である・になる（状態）客観"),
            "100%": (0, "〜である・になる（状態）客観"),
            "25%": (0, "〜である・になる（状態）客観"),
            "80%": (0, "〜である・になる（状態）客観"),
        }
        assert load_dictionary.load_dict1(input_file) == expected_output

    def test_load_dictionary2(self):
        """
        dictionary_loaderモジュール内のload_dict2関数のテスト
        dictionary2.txtと同様の形式のファイルから辞書が正しくloadされるかチェックする
        """
        input_file = (
            Path(__file__).parent
            / "test_load_dictionary_files"
            / "test_dictionary2.txt"
        )
        expected_output = {
            "あがく": [(["あがく"], -1, "経験")],
            "あきらめる": [(["あきらめる"], -1, "経験")],
            "あきる": [(["あきる"], -1, "経験")],
            "あきれる": [(["あきれる"], -1, "経験"), (["あきれる", "た"], -1, "経験")],
        }
        assert load_dictionary.load_dict2(input_file) == expected_output

    def test_load_PnJa(self):
        """
        dictionary_loaderモジュール内のload_PnJa関数のテスト
        pn_ja.txtと同様の形式のファイルから辞書が正しくloadされるかチェックする
        """
        input_file = (
            Path(__file__).parent / "test_load_dictionary_files" / "test_pn_ja.txt"
        )
        expected_output = {
            "優れる": (1.0, "すぐれる", "動詞"),
            "良い": (0.999995, "よい", "形容詞"),
            "喜ぶ": (0.999979, "よろこぶ", "動詞"),
            "褒める": (0.999979, "ほめる", "動詞"),
            "めでたい": (0.999645, "めでたい", "形容詞"),
        }
        assert load_dictionary.load_PnJa(input_file) == expected_output


if __name__ == "__main__":
    unittest.main()
