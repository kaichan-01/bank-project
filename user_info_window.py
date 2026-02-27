import tkinter as tk
from tkinter import messagebox

# 会員情報変更ウィンドウクラス
class UserInfoWindow(tk.Toplevel):
    def __init__(self, master, db, current_user, refresh_callback):
        super().__init__(master) 
        self.db = db  # データベースオブジェクト
        self.current_user = current_user  # 現在ログイン中のユーザー情報
        self.refresh_callback = refresh_callback  # メインメニューを更新するためのコールバック関数
        self.title("会員情報変更") 
        self.geometry("350x250")  
        
        self.create_widgets()  # ウィジェット作成
    
    def create_widgets(self):
        # データベースから現在のユーザー情報を取得
        user_info = self.db.get_user_info(self.current_user['user_id']) or {}
        
        # ユーザーニックネームのラベルと入力欄
        self.user_nickname_label = tk.Label(self, text="ユーザーニックネーム")
        self.user_nickname_label.place(x=90, y=20)
        self.user_nickname_entry = tk.Entry(self, width=25)
        self.user_nickname_entry.insert(0, user_info.get('username', "") or "")  # 現在のニックネームを表示
        self.user_nickname_entry.place(x=90, y=45)
        
        # パスワードのラベルと入力欄（
        self.password_label = tk.Label(self, text="パスワード")
        self.password_label.place(x=90, y=80)
        self.password_entry = tk.Entry(self, width=25, show="*") 
        self.password_entry.insert(0, "")  # 空欄（変更しない場合は空のまま）
        self.password_entry.place(x=90, y=105)

        # メールアドレスのラベルと入力欄
        self.email_label = tk.Label(self, text="メールアドレス(ログインID)")
        self.email_label.place(x=90, y=140)
        self.email_entry = tk.Entry(self, width=25)
        self.email_entry.insert(0, user_info.get('email', "") or "")  # 現在のメールアドレスを表示
        self.email_entry.place(x=90, y=165)
        
        # 更新ボタン
        self.update_button = tk.Button(self, text="更新", command=self.update)
        self.update_button.place(x=155, y=200)

    
    # 会員情報を更新するメソッド
    def update(self):
        # 入力された情報を取得
        user_nickname = self.user_nickname_entry.get()  # ニックネーム
        password = self.password_entry.get()  # パスワード（空の場合は変更しない）
        email = self.email_entry.get()  # メールアドレス
            
        # データベースで会員情報を更新
        success, message = self.db.update_user_info(self.current_user['user_id'], user_nickname, password, email)
        if success:
            # 更新成功
            messagebox.showinfo("更新結果", message, parent=self)
            self.destroy()
            self.refresh_callback()  # メインメニューの表示を更新
        else:
            # 更新失敗
            messagebox.showerror("更新失敗", message, parent=self)