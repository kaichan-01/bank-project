import tkinter as tk
from tkinter import ttk 

# 取引履歴ウィンドウクラス
class TransactionHistoryWindow(tk.Toplevel):
    def __init__(self, master, db, current_user):
        super().__init__(master)  
        self.db = db  # データベースオブジェクト
        self.current_user = current_user  # 現在ログイン中のユーザー情報
        self.title("取引履歴")  
        self.geometry("700x500") 
        
        self.create_widgets()  # ウィジェット作成
    
    def create_widgets(self):
        # Treeviewウィジェットの作成
        self.tree_view = ttk.Treeview(self, show="headings",  height=20)
        self.tree_view.pack()
        
        # テーブルの列を定義
        header = ("created_at", "transaction_type", "amount", "balance_after", "description")
        self.tree_view.config(columns=header)
        
        # 各カラムのヘッダーを設定
        self.tree_view.heading("created_at", text="日時")
        self.tree_view.heading("transaction_type", text="取引種別")
        self.tree_view.heading("amount", text="金額(円)")
        self.tree_view.heading("balance_after", text="取引後残高(円)")
        self.tree_view.heading("description", text="説明")

        # 各カラムの幅と表示位置を設定
        self.tree_view.column("created_at", width=150, anchor=tk.CENTER)  # 中央揃え
        self.tree_view.column("transaction_type", width=80, anchor=tk.CENTER)  # 中央揃え
        self.tree_view.column("amount", width=80, anchor=tk.E)  # 右揃え
        self.tree_view.column("balance_after", width=100, anchor=tk.E)  # 右揃え
        self.tree_view.column("description", width=150, anchor=tk.W)  # 左揃え
        
        
        # データベースから取引履歴を取得
        transactions = self.db.get_transactions(self.current_user['user_id'])
        
        # 取得した取引履歴をTreeviewに表示
        for trans in transactions:
            # 日時のフォーマット（ミリ秒部分を削除）
            date_str = trans['created_at'].split('.')[0] if trans['created_at'] else ""
            
            # 取引種別を日本語に変換
            transaction_type_display = {
                'deposit': '入金',
                'withdrawal': '出金',
                'transfer': '振込'
            }.get(trans['transaction_type'], trans['transaction_type'])
            
            # Treeviewに1行ずつデータを挿入
            self.tree_view.insert("", tk.END, values=(
                date_str,  # 日時
                transaction_type_display,  # 取引種別
                f"{trans['amount']:,}",  # 金額
                f"{trans['balance_after']:,}",  # 取引後残高
                trans['description']  # 説明
            ))
        
        
        # スクロールバーを作成
        # scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_view.yview)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.tree_view.configure(yscroll=scrollbar.set)