import MySQLdb
import hashlib
import random

# ネットバンキングのデータベース操作クラス
class BankingDatabase:
    # ソルトを生成するメソッド
    def get_salt(self):
        random_source = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        salt = ''
        for i in range(20):
            salt += random.choice(random_source)
        return salt
    
    # パスワードをハッシュ化するメソッド
    def hash_password(self, password, salt):
        hashed_pw = hashlib.pbkdf2_hmac(
          'sha256',  
          password.encode(),  
          salt.encode(),  
          19720  
          ).hex()
        return hashed_pw


    def get_connection(self):
        connection = MySQLdb.connect(
            user='root',  
            password='dummy',  # 個人情報のため、ダミーのパスワードを使用しています。
            host='localhost',  
            database='dummy'  # 個人情報のため、ダミーのデータベース名を使用しています。
        )
        return connection
    
    # 新規ユーザーを登録するメソッド
    def register_user(self, username_sei, username_mei, username_sei_kana, username_mei_kana, user_nickname, password, email, account_number, account_type, birthdate='', phone=''):
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            # ユーザーごとにランダムなソルトを生成
            salt = self.get_salt()
            hashed_pwd = self.hash_password(password, salt)
            # 電話番号と生年月日の有無で異なるSQL文を実行
            if phone and birthdate:
                # 電話番号あり、生年月日ありの場合
                sql = ("INSERT INTO users (username_sei, username_mei, username_sei_kana, username_mei_kana, "
                       "user_nickname, password, salt, email, birthdate, account_type, account_number, phone, balance) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)")
                cursor.execute(sql, (username_sei, username_mei, username_sei_kana, username_mei_kana, user_nickname, hashed_pwd, salt, email, birthdate, account_type, account_number, phone))
            elif phone:
                # 電話番号あり、生年月日なしの場合
                sql = ("INSERT INTO users (username_sei, username_mei, username_sei_kana, username_mei_kana, "
                       "user_nickname, password, salt, email, account_type, account_number, phone, balance) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)")
                cursor.execute(sql, (username_sei, username_mei, username_sei_kana, username_mei_kana, user_nickname, hashed_pwd, salt, email, account_type, account_number, phone))
            elif birthdate:
                # 電話番号なし、生年月日ありの場合
                sql = ("INSERT INTO users (username_sei, username_mei, username_sei_kana, username_mei_kana, "
                       "user_nickname, password, salt, email, birthdate, account_type, account_number, balance) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)")
                cursor.execute(sql, (username_sei, username_mei, username_sei_kana, username_mei_kana, user_nickname, hashed_pwd, salt, email, birthdate, account_type, account_number))
            else:
                # 電話番号なし、生年月日なしの場合
                sql = ("INSERT INTO users (username_sei, username_mei, username_sei_kana, username_mei_kana, "
                       "user_nickname, password, salt, email, account_type, account_number, balance) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)")
                cursor.execute(sql, (username_sei, username_mei, username_sei_kana, username_mei_kana, user_nickname, hashed_pwd, salt, email, account_type, account_number))
            connection.commit()
            return (True, "登録成功しました")
        # 一意制約などのDB整合性エラー時の処理
        except MySQLdb.IntegrityError as e:
            if "user_nickname" in str(e):
                return (False, "ニックネームは既に使用されています")
            elif "email" in str(e):
                return (False, "メールアドレスは既に使用されています")
            else:
                return (False, "この情報は既に登録されています")
        # その他の予期しないエラー時の処理
        except Exception as e:
            return (False, f"エラー: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    
    # ユーザー認証を行うメソッド
    def authenticate_user(self, email, password):
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            # データベースからユーザーのソルト値を取得
            try:
                cursor.execute("SELECT salt FROM users WHERE email = %s", (email,))
                row = cursor.fetchone()
            # 読み込み不可の場合の処理
            except MySQLdb.OperationalError:
                # saltが存在しない場合
                row = None
            
            # ソルトが存在する場合
            if row and row[0]:
                # 保存されているソルト値を使用してパスワードを検証
                stored_salt = row[0]
                # 入力されたパスワードを同じソルトでハッシュ化
                hashed_pwd = self.hash_password(password, stored_salt)
                # ハッシュ化されたパスワードで認証
                cursor.execute("SELECT user_id, user_nickname FROM users WHERE email = %s AND password = %s", (email, hashed_pwd))
                user = cursor.fetchone()
                if user:
                    # 認証成功
                    user_id, user_nickname = user
                    return (True, user_id, user_nickname)
                else:
                    # 認証失敗
                    return (False, None, "ログインIDまたはパスワードが間違っています")
            else:
                # ソルトがレコードにない場合
                hashed_pwd = self.hash_password(password, '')
                cursor.execute("SELECT user_id, user_nickname FROM users WHERE email = %s AND password = %s", (email, hashed_pwd))
                user = cursor.fetchone()
                if user:
                    # 認証成功
                    user_id, user_nickname = user
                    return (True, user_id, user_nickname)
                else:
                    # 認証失敗
                    return (False, None, "ログインIDまたはパスワードが間違っています")
        finally:
            cursor.close()
            connection.close()
    
    # ユーザー情報を取得するメソッド
    def get_user_info(self, user_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            # ユーザー情報を取得
            sql = ("SELECT user_id, user_nickname, balance, phone, email, birthdate, created_at, account_number "
                   "FROM users WHERE user_id = %s")
            cursor.execute(sql, (user_id,))
            
            result = cursor.fetchone()
            if result:
                # 取得したデータを返す
                return {
                    'id': result[0],
                    'username': result[1],
                    'balance': result[2],
                    'phone': result[3],
                    'email': result[4],
                    'birthdate': result[5],
                    'created_at': result[6],
                    'account_number': result[7]
                }
            # ユーザーが見つからない場合
            return None
        finally:
            cursor.close()
            connection.close()
    
    # ユーザー情報を更新するメソッド
    def update_user_info(self, user_id, user_nickname='', password='', email=''):
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            # パスワードが入力されている場合は新しいソルトを生成してハッシュ化
            if password:
                salt = self.get_salt()
                hashed_pwd = self.hash_password(password, salt)
                # パスワードを含めて更新
                sql = ("UPDATE users "
                       "SET user_nickname = %s, password = %s, salt = %s, email = %s "
                       "WHERE user_id = %s")
                cursor.execute(sql, (user_nickname, hashed_pwd, salt, email, user_id))
            else:
                # パスワードが空の場合はパスワード以外の項目のみ更新
                sql = ("UPDATE users "
                       "SET user_nickname = %s, email = %s "
                       "WHERE user_id = %s")
                cursor.execute(sql, (user_nickname, email, user_id))
            
            # データベースに変更を確定
            connection.commit()
            return (True, "登録成功しました")
        # 一意制約などのDB整合性エラー時の処理
        except MySQLdb.IntegrityError as e:
            if "user_nickname" in str(e):
                return (False, "ニックネームは既に使用されています")
            elif "email" in str(e):
                return (False, "メールアドレスは既に使用されています")
            else:
                return (False, "この情報は既に登録されています")
        # その他の予期しないエラー時の処理
        except Exception as e:
            return (False, f"エラー: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    
    # 入金処理を行うメソッド
    def deposit(self, user_id, amount):
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            # 入金額のチェック
            if amount <= 0:
                return (False, "入金額は0より大きい値で入力してください")
            
            # 残高を更新
            sql = ("UPDATE users "
                   "SET balance = balance + %s "
                   "WHERE user_id = %s")
            cursor.execute(sql, (amount, user_id))
            
            # 更新後の残高を取得
            sql = 'SELECT balance FROM users WHERE user_id = %s'
            cursor.execute(sql, (user_id,))
            new_balance = cursor.fetchone()[0]
            
            # 取引履歴テーブルに入金履歴を保存
            sql = ("INSERT INTO transactions (user_id, transaction_type, amount, balance_after, description) "
                   "VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(sql, (user_id, 'deposit', amount, new_balance, '入金'))
            
            # データベースに変更を確定
            connection.commit()
            return (True, f"入金しました（額：{amount:,}円）")
        # その他の予期しないエラー時の処理
        except Exception as e:
            # エラー発生時は未確定の変更を取り消す処理
            connection.rollback()
            return (False, f"エラー: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    
    # 出金処理を行うメソッド
    def withdrawal(self, user_id, amount):
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            # 出金額のチェック
            if amount <= 0:
                return (False, "出金額は0より大きい値で入力してください")
            
            # 現在の残高を取得
            sql = 'SELECT balance FROM users WHERE user_id = %s'
            cursor.execute(sql, (user_id,))
            current_balance = cursor.fetchone()[0]
            
            # 残高不足チェック
            if current_balance < amount:
                return False, "残高が不足しています"
            
            # 残高を更新
            sql = ("UPDATE users "
                   "SET balance = balance - %s "
                   "WHERE user_id = %s")
            cursor.execute(sql, (amount, user_id))
            
            # 更新後の残高を取得
            sql = 'SELECT balance FROM users WHERE user_id = %s'
            cursor.execute(sql, (user_id,))
            new_balance = cursor.fetchone()[0]
            
            # 取引履歴テーブルに出金履歴を保存
            sql = ("INSERT INTO transactions (user_id, transaction_type, amount, balance_after, description) "
                   "VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(sql, (user_id, 'withdrawal', amount, new_balance, '出金'))
            
            # データベースに変更を確定
            connection.commit()
            return (True, f"出金しました（額：{amount:,}円）")
        # その他の予期しないエラー時の処理
        except Exception as e:
            # エラー発生時は未確定の変更を取り消す処理
            connection.rollback()
            return (False, f"エラー: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    
    # 振込処理を行うメソッド
    def transfer(self, from_user_id, to_username, to_account_number, amount):
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            # 振込額のチェック
            if amount <= 0:
                return (False, "振込額は0より大きい値で入力してください")
            
            # 振込先ユーザーの情報を取得
            sql = 'SELECT user_id, user_nickname, account_number FROM users WHERE user_nickname = %s AND account_number = %s'
            cursor.execute(sql, (to_username, to_account_number))
            to_user = cursor.fetchone()
            
            # 振込先ユーザーが存在しない場合
            if not to_user:
                return (False, "振込先ユーザーが見つかりません（ユーザー名または口座番号が間違っています）")
            
            to_user_id = to_user[0]
            
            # 自分自身への振込を禁止
            if from_user_id == to_user_id:
                return (False, "同じユーザーへの振込はできません")
            
            # 送金元の残高確認
            sql = 'SELECT balance FROM users WHERE user_id = %s'
            cursor.execute(sql, (from_user_id,))
            current_balance = cursor.fetchone()[0]            
            # 残高不足チェック
            if current_balance < amount:
                return (False, "残高が不足しています")
            
            # 残高の更新
            # 送金元の残高を減らす
            sql = ("UPDATE users "
                   "SET balance = balance - %s "
                   "WHERE user_id = %s")
            cursor.execute(sql, (amount, from_user_id))
            
            # 送金先の残高を増やす
            sql = ("UPDATE users "
                   "SET balance = balance + %s "
                   "WHERE user_id = %s")
            cursor.execute(sql, (amount, to_user_id))
            
            # 送金元の新しい残高を取得
            sql = 'SELECT balance FROM users WHERE user_id = %s'
            cursor.execute(sql, (from_user_id,))
            from_new_balance = cursor.fetchone()[0]
            
            # 送金元の取引履歴を記録
            sql = ("INSERT INTO transactions (user_id, transaction_type, amount, balance_after, related_user, description) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
            cursor.execute(sql, (from_user_id, 'transfer', amount, from_new_balance, to_username, f'{to_username}さんへ振込'))
            
            # 送金先の新しい残高を取得
            sql = 'SELECT balance FROM users WHERE user_id = %s'
            cursor.execute(sql, (to_user_id,))
            to_new_balance = cursor.fetchone()[0]
            
            # 送金元のニックネームを取得
            sql = 'SELECT user_nickname FROM users WHERE user_id = %s'
            cursor.execute(sql, (from_user_id,))
            from_username = cursor.fetchone()[0]

            # 送金先の取引履歴を記録
            sql = ("INSERT INTO transactions (user_id, transaction_type, amount, balance_after, related_user, description) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
            cursor.execute(sql, (to_user_id, 'transfer', amount, to_new_balance, from_username, f'{from_username}さんからの振込'))            
            # データベースに変更を確定
            connection.commit()
            return (True, f"{to_username}さんに{amount:,}円を振込しました")
        # その他の予期しないエラー時の処理
        except Exception as e:
            # エラー発生時は未確定の変更を取り消す処理
            connection.rollback()
            return (False, f"エラー: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    
    # 取引履歴を取得するメソッド
    def get_transactions(self, user_id, limit=50):
        # ユーザーの取引履歴を新しい順に取得(デフォルトで50件)
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            # 取引履歴を日時の降順（新しい順）で取得
            sql = ("SELECT id, transaction_type, amount, balance_after, related_user, description, created_at "
                   "FROM transactions "
                   "WHERE user_id = %s "
                   "ORDER BY created_at DESC "
                   "LIMIT %s")
            cursor.execute(sql, (user_id, limit))
            
            # 取得結果をリストに変換
            results = cursor.fetchall()
            transactions = []
            for row in results:
                transactions.append({
                    'id': row[0],  # 取引ID
                    'transaction_type': row[1],  # 取引種別
                    'amount': row[2],  # 金額
                    'balance_after': row[3],  # 取引後の残高
                    'related_user': row[4],  # 関連ユーザー（振込の場合）
                    'description': row[5],  # 説明
                    'created_at': str(row[6])  # 取引日時
                })
            return transactions
        finally:
            cursor.close()
            connection.close()
