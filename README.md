# programing_for_calculators

## 開発 Tips

- 仮想環境の用意と依存関係のインストール

```bash
$ python3 -m venv venv
$ source venv/bin/activate // Windowsの場合はvenv\Scripts\activate
$ pip install -r requirements.txt
```

- 仮想環境の終了

```bash
$ venb/bin/deactivate // Windowsの場合はvenv\Scripts\deactivate
```

- フォーマッターの実行

```bash
$ python -m black .
```

- リンターの実行

```bash
$ python -m flake8 my_project/
```

- ユニットテストの実行

```bash
$ python -m unittest
```

- pip でパッケージをインストールする（開発中のパッケージ）

```bash
$ pip install -e <package_name>
```
