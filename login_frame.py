import tkinter as tk
from tkinter import messagebox

# データベース操作用のクラスをインポート
from database import BankingDatabase
# 新規登録画面用のクラスをインポート
from register_window import RegisterWindow

# ログイン画面フレームクラス
class LoginFrame(tk.Frame):
    def __init__(self, master, db, current_user):
        super().__init__(master)
        self.db = db    # データベースオブジェクト
        self.current_user = current_user  # 現在ログイン中のユーザー情報
        self.master = master
        master.geometry("500x400")
        master.title("ネットバンキングシステム - ログイン")
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        # メインフレームの作成
        self.main_frame = tk.Frame(self, width=460, height=460)
        self.main_frame.pack()
        
        # タイトル
        self.title_label = tk.Label(self.main_frame, text="ネットバンキング", font=("Arial", 20, "bold"))
        self.title_label.place(x=150, y=10)
        

        # ログイン入力欄を囲むフレーム
        login_frame = tk.LabelFrame(self.main_frame, text="ログイン", width=420, height=220)
        login_frame.pack(pady=10)

        # ログインID（メールアドレス）入力欄
        self.userid_label = tk.Label(login_frame, text="ログインID(メールアドレス)")
        self.userid_label.place(x=120, y=20)
        self.userid_entry = tk.Entry(login_frame, width=30)
        self.userid_entry.place(x=120, y=45)

        # パスワード入力欄
        self.password_label = tk.Label(login_frame, text="パスワード")
        self.password_label.place(x=120, y=80)
        self.password_entry = tk.Entry(login_frame, width=30, show="*")
        self.password_entry.place(x=120, y=105)
        
        # ログインボタン
        self.login_button = tk.Button(login_frame, text="ログイン", command=self.login)
        self.login_button.place(x=180, y=140)
        
        # 新規登録ボタンを囲むフレーム
        button_frame = tk.Frame(self.main_frame, width=420, height=60)
        button_frame.pack(pady=10)
        
        # 新規登録ボタン
        self.register_button = tk.Button(button_frame, text="新規登録", command=self.open_register)
        self.register_button.place(x=178, y=10)

    # 新規登録画面を開くメソッド
    def open_register(self):
        # 新規登録ウィンドウを表示
        RegisterWindow(self.db, self.master)
    
    # ログイン処理を行うメソッド
    def login(self):
        # 入力されたログインIDとパスワードを取得
        login_id = self.userid_entry.get()
        password = self.password_entry.get()
        
        # ログインIDまたはパスワードが空の場合
        if not login_id or not password:
            messagebox.showerror("エラー", "ログインIDとパスワードを入力してください", parent=self)
            return
        
        # データベースでユーザー認証
        success, user_id, payload = self.db.authenticate_user(login_id, password)
        if success:
            # 認証成功
            self.current_user['user_id'] = user_id
            self.current_user['username'] = payload
            self.show_main_menu()
        else:
            # 認証失敗
            messagebox.showerror("ログイン失敗", payload, parent=self)
    
    # メインメニュー画面を表示するメソッド
    def show_main_menu(self):
        # メインメニューフレームをインポート
        from main_menu import MainMenuFrame
        # メインメニュー画面を作成して表示
        MainMenuFrame(self.master, self.db, self.current_user)
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk() #ウィンドウクラスのインスタンス作成
    
    # データベース接続用のBankingDatabaseクラスをインスタンス化
    db = BankingDatabase()
    # ユーザーのログイン情報を管理する変数を初期化
    current_user = {'user_id': None, 'username': None}
    
    # ログイン画面フレームをインスタンス化して表示
    app = LoginFrame(master=root, db=db, current_user=current_user)
    app.mainloop()