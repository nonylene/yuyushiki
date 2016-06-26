yuyushiki
=========

Annotation Tool

forked from [non117/yuyushiki](https://github.com/non117/yuyushiki)

依存関係
-----------
* Python 3.4 or higher
* flask
* peewee (SQlite)

仕様
------------
1. "pic_path" を見に行きます
2. 画像と顔の四角形をブラウザに表示します
3. キャラ分類をしてもらいます
4. submitされたら、データを記録し、次の画像を表示します

データ形式
----------------
SQlite / face

* 画像ファイルのパス : pic_path
* 人物タグ : character
* 顔の場所 : x / y / w / h
* 顔画像の場所 : face_path

* characters : see config.json.example


その他
----------------
* /list で一覧
