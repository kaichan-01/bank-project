import tkinter as tk
from tkinter import messagebox

# 入金ウィンドウクラス
class DepositWindow(tk.Toplevel):
    def __init__(self, master, db, current_user, refresh_callback):
        super().__init__(master) 
        self.db = db  # データベースオブジェクト
        self.current_user = current_user  # 現在ログイン中のユーザー情報
        self.refresh_callback = refresh_callback  # メインメニューを更新するための関数
        self.title("入金")  
        self.geometry("300x150")  
        
        self.create_widgets()  # ウィジェット作成
    
    def create_widgets(self):
        # 入金額の入力欄
        self.amount_label = tk.Label(self, text="入金額を入力してください")
        self.amount_label.place(x=90, y=20)
        self.amount_entry = tk.Entry(self, width=20)
        self.amount_entry.place(x=90, y=45)
        # 単位表示
        self.en_label = tk.Label(self, text="円")
        self.en_label.place(x=220, y=45)
        
        # 入金ボタン
        self.deposit_button = tk.Button(self, text="入金", command=self.deposit)
        self.deposit_button.place(x=140, y=80)
    
    # 入金処理を実行するメソッド
    def deposit(self):
        try:
            # 入力された金額を整数に変換
            amount = int(self.amount_entry.get())
            # データベースで入金処理を実行
            success, message = self.db.deposit(self.current_user['user_id'], amount)
            if success:
                # 入金成功
                messagebox.showinfo("入金結果", message, parent=self)
                self.destroy() 
                self.refresh_callback()  # メインメニューの残高表示を更新
            else:
                # 入金失敗
                messagebox.showerror("入金失敗", message, parent=self)
        except ValueError:
            # 数値以外が入力された場合のエラー処理
            messagebox.showerror("エラー", "正しい数値を入力してください")
