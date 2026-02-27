import tkinter as tk
import tkinter.ttk as ttk 
from tkinter import messagebox
import random 
import string  

# 新規登録ウィンドウクラス
class RegisterWindow(tk.Toplevel):
    def __init__(self, db, master):
        super().__init__(master) 
        self.db = db  # データベースオブジェクト
        self.master = master  
        self.title("新規登録")  
        self.geometry("500x600") 
        self.create_widgets()  # ウィジェット作成
    
    def create_widgets(self):
        
        # ウィンドウタイトルラベル
        self.title_label = tk.Label(self, text="新規登録フォーム", font=("Arial", 14, "bold"))
        self.title_label.place(x=150, y=10)

        # ニックネームの入力欄
        self.nickname_label = tk.Label(self, text="ニックネーム（2～12文字以内かつ記号は使用できません。）")
        self.nickname_label.place(x=60, y=45)
        self.user_nickname_entry = tk.Entry(self, width=55)
        self.user_nickname_entry.place(x=60, y=70)

        # パスワードの入力欄
        self.password_label = tk.Label(self, text="パスワード (英数字8～20文字)")
        self.password_label.place(x=60, y=95)
        self.password_entry = tk.Entry(self, width=55, show="*")
        self.password_entry.place(x=60, y=120)

        # メールアドレスの入力欄
        self.email_label = tk.Label(self, text="メールアドレス(ログインID)")
        self.email_label.place(x=60, y=145)
        self.email_entry = tk.Entry(self, width=55)
        self.email_entry.place(x=60, y=170)

        # 名前の入力欄
        self.user_name_label = tk.Label(self, text="名前")
        self.user_name_label.place(x=60, y=205)

        self.username_sei_kana_label = tk.Label(self, text="姓(カナ)")
        self.username_sei_kana_label.place(x=60, y=230)
        self.username_sei_kana_entry = tk.Entry(self, width=25)
        self.username_sei_kana_entry.place(x=60, y=255)

        self.username_mei_kana_label = tk.Label(self, text="名(カナ)")
        self.username_mei_kana_label.place(x=240, y=230)
        self.username_mei_kana_entry = tk.Entry(self, width=25)
        self.username_mei_kana_entry.place(x=240, y=255)

        self.username_sei_label = tk.Label(self, text="姓")
        self.username_sei_label.place(x=60, y=290)
        self.username_sei_entry = tk.Entry(self, width=25)
        self.username_sei_entry.place(x=60, y=315)

        self.username_mei_label = tk.Label(self, text="名")
        self.username_mei_label.place(x=240, y=290)
        self.username_mei_entry = tk.Entry(self, width=25)
        self.username_mei_entry.place(x=240, y=315)
        
        # 電話番号の入力欄
        self.phone_label = tk.Label(self, text="電話番号(ハイフン無し)")
        self.phone_label.place(x=60, y=340)
        self.phone_entry = tk.Entry(self, width=55)
        self.phone_entry.place(x=60, y=365)

        # 生年月日の入力欄
        self.birthdate_label = tk.Label(self, text="生年月日")
        self.birthdate_label.place(x=60, y=400)
        self.years_label = tk.Label(self, text="年")
        self.years_label.place(x=145, y=430)
        years = [str(y) for y in range(1900, 2026)]
        self.years_combo = ttk.Combobox(self, values=years, width=10, state="readonly")
        self.years_combo.place(x=60, y=430)
        self.months_label = tk.Label(self, text="月")
        self.months_label.place(x=230, y=430)
        months = [str(m) for m in range(1, 12 + 1)]
        self.months_combo = ttk.Combobox(self, values=months, width=6, state="readonly")
        self.months_combo.place(x=170, y=430)
        self.days_label = tk.Label(self, text="日")
        self.days_label.place(x=330, y=430)
        days = [str(d) for d in range(1, 31 + 1)]
        self.days_combo = ttk.Combobox(self, values=days, width=6, state="readonly")
        self.days_combo.place(x=270, y=430)

        # 口座種別の選択欄
        self.account_type_label = tk.Label(self, text="口座種別")
        self.account_type_label.place(x=60, y=460)

        self.account_type_var = tk.IntVar()
        self.account_type_radio1 = tk.Radiobutton(self, variable=self.account_type_var, text="普通預金", value=1)
        self.account_type_radio2 = tk.Radiobutton(self, variable=self.account_type_var, text="当座預金", value=2)
        self.account_type_radio1.place(x=150, y=480)
        self.account_type_radio2.place(x=250, y=480)
        self.account_type_var.set(1)
        
        # 登録・キャンセルボタン
        self.register_button = tk.Button(self, text="登録", command=self.register)
        self.register_button.place(x=150, y=520)
        self.cancel_button = tk.Button(self, text="キャンセル", command=self.destroy)
        self.cancel_button.place(x=250, y=520)

        # 注意書きラベル
        self.warning_label1 = tk.Label(self, text="※必須", font=("Arial", 9, "bold"), fg="red")
        self.warning_label1.place(x=345, y=45)
        self.warning_label2 = tk.Label(self, text="※必須", font=("Arial", 9, "bold"), fg="red")
        self.warning_label2.place(x=210, y=95)
        self.warning_label3 = tk.Label(self, text="※必須", font=("Arial", 9, "bold"), fg="red")
        self.warning_label3.place(x=180, y=145)
        self.warning_label4 = tk.Label(self, text="※必須", font=("Arial", 9, "bold"), fg="red")
        self.warning_label4.place(x=90, y=205)
        self.warning_label6 = tk.Label(self, text="※必須", font=("Arial", 9, "bold"), fg="red")
        self.warning_label6.place(x=100, y=460)
        
        self.any_label1 = tk.Label(self, text="※任意", font=("Arial", 9, "bold"), fg="gray")
        self.any_label1.place(x=180, y=340)
        self.any_label2 = tk.Label(self, text="※任意", font=("Arial", 9, "bold"), fg="gray")
        self.any_label2.place(x=110, y=400)
    
    # 新規登録処理を実行するメソッド
    def register(self):
        username_sei = self.username_sei_entry.get()  # 姓
        username_mei = self.username_mei_entry.get()  # 名
        username_sei_kana = self.username_sei_kana_entry.get()  # 姓（カナ）
        username_mei_kana = self.username_mei_kana_entry.get()  # 名（カナ）
        user_nickname = self.user_nickname_entry.get()  # ニックネーム
        password = self.password_entry.get()  # パスワード
        email = self.email_entry.get()  # メールアドレス
        years = self.years_combo.get()  # 生年月日（年）
        months = self.months_combo.get()  # 生年月日（月）
        days = self.days_combo.get()  # 生年月日（日）
        phone = self.phone_entry.get()  # 電話番号
        # 生年月日をYYYY-MM-DD形式に変換
        birthdate = f"{years}-{months.zfill(2)}-{days.zfill(2)}"
        acount_type = self.account_type_var.get()  # 口座種別

        # 記号チェック用の文字セット
        symbols = string.punctuation

        # ランダムな7桁の口座番号を生成
        account_number = str(random.randint(1000000, 9999999))

        # 必須項目チェック
        if not username_sei or not username_mei or not username_sei_kana or not username_mei_kana or not user_nickname or not password or not email or not acount_type:
            messagebox.showerror("エラー", "すべての必須項目を入力してください", parent=self)
            return
        
        # ニックネームの入力チェック
        # 文字数チェック（2～12文字）
        if len(user_nickname) < 2 or len(user_nickname) > 12 :
            messagebox.showerror("エラー", "ニックネームは2～12文字で入力してください", parent=self)
            return
        
        # 記号使用チェック
        if any(char in symbols for char in user_nickname):
            messagebox.showerror("エラー", "ニックネームに記号は使用できません。", parent=self) 
            return
        
        # 名前の入力チェック
        # カナの文字種チェック
        if not username_sei_kana.isalpha() or not username_mei_kana.isalpha():
            messagebox.showerror("エラー", "名前(カナ)は全角カタカナで入力してください", parent=self)
            return
        
        # 名前の文字種チェック
        if not username_sei.isalpha() or not username_mei.isalpha():
            messagebox.showerror("エラー", "名前は全角で入力してください", parent=self)
            return
        
        # 文字数チェック（8～20文字）
        if len(password) <= 8 or len(password) >= 20 :
            messagebox.showerror("エラー", "パスワードは8～20文字で入力してください", parent=self)
            return
        
        # 英数字のみチェック
        if not password.isalnum():
            messagebox.showerror("エラー", "パスワードは英数字で入力してください", parent=self)
            return

        # メールアドレスの入力チェック
        # @が含まれているかチェック
        if "@" not in email:
            messagebox.showerror("エラー", "正しいメールアドレスを入力してください", parent=self)
            return
        
        # 電話番号の入力チェック
        # 入力されている場合のみチェック（数字のみ、10～11桁）
        if phone and (not phone.isdigit() or len(phone) < 10 or len(phone) > 11):
            messagebox.showerror("エラー", "電話番号はハイフン無しの10～11桁で入力してください", parent=self)
            return
        
        # データベースに登録
        success, message = self.db.register_user(username_sei, username_mei, username_sei_kana, username_mei_kana, user_nickname, password, email, account_number, acount_type, birthdate, phone)
        if success:
            # 登録成功
            messagebox.showinfo("成功", message, parent=self)
            self.destroy()
        else:
            # 登録失敗
            messagebox.showerror("登録失敗", message, parent=self)
