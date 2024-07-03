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

### ・・・ログイン処理・・・

#### ログイン画面
指定されたURLをブラウザに入力すると次のようなログイン画面に遷移します。  
useridを入力してログインしてください。  
・管理者：管理者ID    
・一般ユーザー：一般ユーザーID  
<img width="1440" alt="login_home" src="https://github.com/sub-seminar/book_management_system/assets/148195758/21043dbe-110c-406c-86be-b1bad33ef6d8">

#### ユーザー新規登録画面
ログイン用ユーザーID未所持の方は、ログイン画面の「新規登録はこちら」をクリックしてください。  
以下のような画面に遷移しますので、必要事項を入力し登録ボタンをクリックしてください。  
登録が完了するとログイン画面に再び遷移するので、IDを入力してログインしてください。
<img width="1440" alt="login_regist" src="https://github.com/sub-seminar/book_management_system/assets/148195758/07cbe683-e1e6-4884-b767-1812b885ada8">

### ・・・管理者・・・
#### 管理者ホーム画面
管理者IDでログインすると管理者ホーム画面に遷移します。  
ここでは一般ユーザーの本の貸し出し状況を確認することができます。 
使用後は「ログアウトボタン」を押してからアプリを閉じてください。
<img width="1440" alt="admin_home" src="https://github.com/sub-seminar/book_management_system/assets/148195758/6fc7e782-6641-46ac-b162-c835b8cfa62f">
また、画面下部の「在庫確認」と「ユーザー情報確認」ボタンを押すことでそれぞれ次のような画面に遷移します。
<br><br><br>

#### 在庫確認画面  
この画面では蔵書の管理を行えます。  
蔵書一覧が表示されており、削除ボタンを押すことで本の在庫を消すことができます。  
「管理者ホームに戻る」ボタンを押すと先ほどの管理者画面に戻ります。
<img width="1440" alt="admin_book_inv" src="https://github.com/sub-seminar/book_management_system/assets/148195758/631c3594-57a0-4025-846a-d285d842baf2">
また、「新規本の登録」ボタンを押すことで次の画面に遷移します。
<br><br><br>

#### 新規本の登録画面
蔵書への新規本の登録を行えます。必要事項を入力し、登録ボタンを押してください。  
登録された本は在庫確認画面にてご確認ください。
<img width="1440" alt="admin_regist_book" src="https://github.com/sub-seminar/book_management_system/assets/148195758/3c5d13cb-5724-41be-a5a7-85d46daec54c">

#### ユーザー情報確認画面  
このシステムに登録している全一般ユーザーの情報を確認できます。  
操作カラムの削除ボタンを押すことでユーザーの削除を行えます。  
「管理者ホームに戻る」ボタンを押すことで、管理者トップ画面に戻ります。
<img width="1440" alt="admin_users" src="https://github.com/sub-seminar/book_management_system/assets/148195758/8f07076d-2176-4e43-ac39-138e45177f9a">


### ・・・一般ユーザー・・・
#### ユーザーホーム画面
ログイン画面で一般ユーザーのIDを入力すると次のようなホーム画面に遷移します。   
この画面ではご自身の貸し出し状況の確認と、本の返却申請を行えます。  
貸し出し中の本には、返却日カラムに赤い「返却ボタン」が表示されています。  
返却ボタンをクリックすることで本の返却登録を行えます。  
使用後は「ログアウトボタン」を押してからアプリを閉じてください。
<img width="1440" alt="users_home" src="https://github.com/sub-seminar/book_management_system/assets/148195758/1591eb77-0d64-44ee-9fe1-c442ef458fdd">
また、「本の一覧取得・検索・貸出」ボタンを押すと次の画面に遷移します。
<br><br><br>

#### 本の検索・貸し出し申請画面
この画面では蔵書の一覧を確認できます。  
現在貸出が可能な本に関しては「貸出申請ボタン」が表示されており、クリックすることで貸出申請をすることができます。また検索欄に文字列を入力し「検索ボタン」をクリックすることで、本のタイトルとキーワード一致による絞り込みを行えます。空白で検索ボタンを再び押すことで全ての本を表示できます。 
<img width="1440" alt="users_book_rental" src="https://github.com/sub-seminar/book_management_system/assets/148195758/d4668d4e-2b18-4c5b-974e-2aefb16a0104">


##### ●開発者
新井陽登（Arai Haruto）：フロントエンド（HTML,CSS,JavaScript）  
小村涼太郎（Komura Ryotaro）：バックエンド（Flask・SQL）  
リクカケツ（Riku）：データベース（SQL・SQlite3）  
小原和磨（Obara Kazuma）：マネジメント  



