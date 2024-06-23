import pytest
import os
import sys
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(project_root_path)
import src.my_library.load_dictionary as dictionary_loader 

def test_load_dictionary1():
    '''
    dictionary_loaderモジュール内のload_dict1関数のテスト
    dictionary.txtと同様の形式のファイルから辞書が正しくloadされるかチェックする
    '''
    input_file = os.path.join(project_root_path, 'tests', 'test_load_dictionary_files', 'test_dictionary1.txt')
    expected_output = {
        '２，３日': (0, '〜である・になる（状態）客観'), 
        '10%': (0, '〜である・になる（状態）客観'), 
        '100%': (0, '〜である・になる（状態）客観'), 
        '25%': (0, '〜である・になる（状態）客観'), 
        '80%': (0, '〜である・になる（状態）客観')
    }
    assert dictionary_loader.load_dict1(input_file) == expected_output
def test_load_dictionary2():
    '''
    dictionary_loaderモジュール内のload_dict2関数のテスト
    dictionary2.txtと同様の形式のファイルから辞書が正しくloadされるかチェックする
    '''
    input_file = os.path.join(project_root_path, 'tests', 'test_load_dictionary_files', 'test_dictionary2.txt')
    expected_output = {
        'あがく': [(-1, ['あがく'], '経験')], 
        'あきらめる': [(-1, ['あきらめる'], '経験')], 
        'あきる': [(-1, ['あきる'], '経験')], 
        'あきれる': [(-1, ['あきれる'], '経験'), (-1, ['あきれる', 'た'], '経験')]
    }
    assert dictionary_loader.load_dict2(input_file) == expected_output
def test_load_PnJa():
    '''
    dictionary_loaderモジュール内のload_PnJa関数のテスト
    pn_ja.txtと同様の形式のファイルから辞書が正しくloadされるかチェックする
    '''
    input_file = os.path.join(project_root_path, 'tests', 'test_load_dictionary_files', 'test_pn_ja.txt')
    expected_output = {
        '優れる': (1.0, 'すぐれる', '動詞'), 
        '良い': (0.999995, 'よい', '形容詞'), 
        '喜ぶ': (0.999979, 'よろこぶ', '動詞'), 
        '褒める': (0.999979, 'ほめる', '動詞'), 
        'めでたい': (0.999645, 'めでたい', '形容詞')}
    assert dictionary_loader.load_PnJa(input_file) == expected_output
    