import tkinter as tk

# 各機能のウィンドウクラスをインポート
from deposit_window import DepositWindow  # 入金ウィンドウ
from withdrawal_window import WithdrawalWindow  # 出金ウィンドウ
from transfer_window import TransferWindow  # 振込ウィンドウ
from transaction_history_window import TransactionHistoryWindow  # 取引履歴ウィンドウ
from user_info_window import UserInfoWindow  # 会員情報変更ウィンドウ

# メインメニューフレームクラス
class MainMenuFrame(tk.Frame):
    def __init__(self, master, db, current_user):
        super().__init__(master, width=600, height=600)
        self.master = master 
        self.db = db  # データベースオブジェクト
        self.current_user = current_user  # 現在ログイン中のユーザー情報
        self.pack()  
        master.title("メインメニュー") 
        master.geometry("500x500") 
        self.create_widgets()  # ウィジェット作成
    
    # 画面の部品を作成するメソッド
    def create_widgets(self):
        # データベースからユーザー情報を取得
        user_info = self.db.get_user_info(self.current_user['user_id'])
        balance = user_info['balance']  # 残高
        account_number = user_info['account_number']  # 口座番号
        user_nickname = user_info['username']  # ユーザーニックネーム
        
        # ヘッダーテキスト
        header_text = f"ササキネットバンクへようこそ！\n{user_nickname}さん\n口座番号: {account_number}\n残高: {balance:,.0f}円"
        self.header_label = tk.Label(self, text=header_text, font=("Arial", 14, "bold"))
        self.header_label.place(x=100, y=30)
        
        # 入金ボタン
        self.payment_button = tk.Button(self, text="入金", width=60, command=self.show_deposit)
        self.payment_button.place(x=40, y=180)
        # 出金ボタン
        self.withdrawal_button = tk.Button(self, text="出金", width=60, command=self.show_withdrawal)
        self.withdrawal_button.place(x=40, y=230)
        # 振込ボタン
        self.transfer_button = tk.Button(self, text="振込", width=60, command=self.show_transfer)
        self.transfer_button.place(x=40, y=280)
        # 取引履歴ボタン
        self.transaction_history_button = tk.Button(self, text="取引履歴", width=60, command=self.show_transaction_history)
        self.transaction_history_button.place(x=40, y=330)
        # 会員情報変更ボタン
        self.user_info_button = tk.Button(self, text="会員情報変更", width=60, command=self.show_user_info)
        self.user_info_button.place(x=40, y=380)
        # ログアウトボタン
        self.logout_button = tk.Button(self, text="ログアウト", width=60, command=self.logout)
        self.logout_button.place(x=40, y=430)
    
    # 入金画面を表示するメソッド
    def show_deposit(self):
        DepositWindow(self.master, self.db, self.current_user, self.refresh_menu)
    
    # 出金画面を表示するメソッド
    def show_withdrawal(self):
        WithdrawalWindow(self.master, self.db, self.current_user, self.refresh_menu)
    
    # 振込画面を表示するメソッド
    def show_transfer(self):
        TransferWindow(self.master, self.db, self.current_user, self.refresh_menu)
    
    # 取引履歴画面を表示するメソッド
    def show_transaction_history(self):
        TransactionHistoryWindow(self.master, self.db, self.current_user)
    
    # 会員情報変更画面を表示するメソッド
    def show_user_info(self):
        UserInfoWindow(self.master, self.db, self.current_user, self.refresh_menu)
    
    # ログアウト処理を行うメソッド
    def logout(self):
        from login_frame import LoginFrame
        # ユーザー情報をクリア
        self.current_user['user_id'] = None
        self.current_user['username'] = None
        # ログイン画面に戻る
        LoginFrame(self.master, self.db, self.current_user)
        self.destroy()
    
    # メインメニューを再読み込みするメソッド（残高更新時などに使用）
    def refresh_menu(self):
        # 新しいメインメニュー画面を作成
        MainMenuFrame(self.master, self.db, self.current_user)
        self.destroy()