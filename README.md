<br>

# 本貸し出し管理システム



<br>

## ●概要
このシステムは図書の貸し出し管理をするアプリです。2種類の利用者が存在します。  
<br>
①管理者：特定のIDでログインすることで管理者としての操作を実行できます。権限は以下の通りです。  
  ・全ての一般ユーザーの図書貸し出し状況の把握  
  ・本在庫一覧の取得  
  ・新規の本の登録  
  ・既存ユーザーの削除  
  <br>
②一般ユーザー：ユーザー登録したIDでログインすることで、一般ユーザーの操作を実行できます。　    
  ・自身の貸し出し履歴の確認  
  ・図書の返却申請  
  ・蔵書の一覧取得  
  ・図書の検索機能  
  ・図書の貸し出し機能  
  

<br><br><br>
## ●アプリのインストール方法

①dockerのインストール：https://www.docker.com/ja-jp/

②コマンドの実行
### 
```
# リポジトリのコピー
git clone https://github.com/sub-seminar/book_management_system.git

# 階層の移動
cd [任意の階層]/book_management_system

# 環境構築
docker build -t book_management_system .

# アプリ実行
docker run -p 5050:5050 book_management_system

# ブラウザでURLにアクセス
http://127.0.0.1:5050

```

<br><br><br>

## ●アプリの使用方法



