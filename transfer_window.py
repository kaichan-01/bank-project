import tkinter as tk
from tkinter import messagebox

# 振込ウィンドウクラス
class TransferWindow(tk.Toplevel):
    def __init__(self, master, db, current_user, refresh_callback):
        super().__init__(master)  
        self.db = db  # データベースオブジェクト
        self.current_user = current_user  # 現在ログイン中のユーザー情報
        self.refresh_callback = refresh_callback  # メインメニューを更新するためのコールバック関数
        self.title("振込")  
        self.geometry("350x250")  
        
        self.create_widgets()  # ウィジェット作成
    
    def create_widgets(self):
        # 振込先ユーザー名のラベルと入力欄
        self.to_yuser_label = tk.Label(self, text="振込先ユーザー名")
        self.to_yuser_label.place(x=90, y=20)
        self.to_user_entry = tk.Entry(self, width=25)
        self.to_user_entry.place(x=90, y=45)
        
        # 振込先口座番号のラベルと入力欄
        self.to_account_label = tk.Label(self, text="振込先口座番号")
        self.to_account_label.place(x=90, y=80)
        self.to_account_entry = tk.Entry(self, width=25)
        self.to_account_entry.place(x=90, y=105)
        
        # 振込額のラベルと入力欄
        self.amount_label = tk.Label(self, text="振込額")
        self.amount_label.place(x=90, y=140)
        self.amount_entry = tk.Entry(self, width=25)
        self.amount_entry.place(x=90, y=165)

        # 単位表示
        self.en_label = tk.Label(self, text="円")
        self.en_label.place(x=250, y=165)
        
        # 振込ボタン
        self.amount_button = tk.Button(self, text="振込", command=self.transfer)
        self.amount_button.place(x=155, y=200)
    
    # 振込処理を実行するメソッド
    def transfer(self):
        try:
            # 入力された情報を取得
            to_user = self.to_user_entry.get()  # 振込先ユーザー名
            to_account = self.to_account_entry.get()  # 振込先口座番号
            amount = int(self.amount_entry.get())  # 振込額
            
            # 入力チェック：振込先ユーザー名が空の場合
            if not to_user:
                messagebox.showerror("エラー", "振込先ユーザー名を入力してください", parent=self)
                return
            
            # 入力チェック：振込先口座番号が空の場合
            if not to_account:
                messagebox.showerror("エラー", "振込先口座番号を入力してください", parent=self)
                return
            
            # データベースで振込処理を実行
            success, message = self.db.transfer(self.current_user['user_id'], to_user, to_account, amount)
            if success:
                # 振込成功：結果を表示してウィンドウを閉じる
                messagebox.showinfo("振込結果", message, parent=self)
                self.destroy()  # ウィンドウを閉じる
                self.refresh_callback()  # メインメニューの残高表示を更新
            else:
                # 振込失敗（残高不足、ユーザーが見つからないなど）：エラーメッセージを表示
                messagebox.showerror("振込失敗", message, parent=self)
        except ValueError:
            # 数値以外が入力された場合のエラー処理
            messagebox.showerror("エラー", "正しい数値を入力してください")