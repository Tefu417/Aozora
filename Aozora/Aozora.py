zip = "50_Natsume.zip"

# zip解凍
import zipfile
with zipfile.ZipFile(zip, "r") as myzip:
    myzip.extractall()
    # 解凍後のファイルからデータ読み込み
    for myfile in myzip.infolist():
        # 解凍後ファイル名取得
        filename = myfile.filename
        # ファイルオープン時にencodingを指定してsjisの変換をする
        with open(filename, encoding = "sjis") as file:
            text = file.read()

# ファイル整形
import re
# | の除去
text = text.replace("|", "")
# ルビの削除
text = re.sub("《.+?》", "", text)
# 入力注の削除
text = re.sub("[#.+?]", "", text)
" 空行の削除"
text = re.sub("\n\n", "\n", text)
text = re.sub("\r", "", text)


# Janomeのインストール
# pip install janome | tail -n 1

# Janomeのロード
from janome.tokenizer import Tokenizer

# Tokenizerインスタンスの生成
t = Tokenizer()

# テキストを引数として、形態素解析の結果、名詞・動詞・形容詞の
# 原形のみを配列で抽出する関数を定義
def extract_words(text):
    tokens = t.tokenize(text)
    return [token.base_form for token in tokens
        if token.part_of_speech.split(",")[0]
            in ["名詞", "動詞", "形容詞"]]

# 全体のテキストを句点("。")で区切った配列にする
sentences = text.split("。")
# それぞれの文章を単語リストに変換(処理に数分かかる)
word_list = [extract_words(sentence) for sentence in sentences]

print(word_list[1])

# Word2Vecライブラリの導入
# !pip install gensim | tail -n 1

# Word2Vecライブラリのロード
from gensim.models import word2vec

# size: 圧縮次元数
# min_count: 出現頻度の低いものをカットする
# window: 前後の単語を拾う際の窓の広さを決める
# iter: 機械学習の繰り返し回数(デフォルト:5)十分学習できていないときにこの値を調整する
# model.wv.most_similarの結果が1に近いものばかりで、
# model.dict['wv']のベクトル値が小さい値ばかりのときは
# 学習回数が少ないと考えられる
# その場合、iterの値を大きくして、再度学習を行う

# 事前準備したword_listを使ってWord2Vecの学習実施
model = word2vec.Word2Vec(word_list, size=100,min_count=5,window=5,iter=1000)


# 結果の確認1
# 一つ一つの単語は100次元のベクトルになっている 
# 「する」のベクトル値を確認
print(model.__dict__['wv']['する'])


# 結果の確認2
# 関数most_similarを使って「する」の類似単語を調べる 
ret = model.wv.most_similar(positive=['する']) 
for item in ret:
    print(item[0], item[1])