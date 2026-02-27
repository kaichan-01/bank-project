-- ユーザーテーブル
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER AUTO_INCREMENT PRIMARY KEY,  -- ユーザーID
    username_sei VARCHAR(100) NOT NULL, -- ユーザーの姓
    username_mei VARCHAR(100) NOT NULL, -- ユーザーの名
    username_sei_kana VARCHAR(100) NOT NULL, -- ユーザーの姓（カナ）
    username_mei_kana VARCHAR(100) NOT NULL, -- ユーザーの名（カナ）
    user_nickname VARCHAR(200) UNIQUE NOT NULL, -- ユーザーニックネーム
    password TEXT NOT NULL, -- ハッシュ化されたパスワード
    salt VARCHAR(100), -- ハッシュ用ソルト
    balance DECIMAL(15, 0) NOT NULL DEFAULT 0, -- 残高
    phone VARCHAR(25), -- 電話番号
    email VARCHAR(100) NOT NULL UNIQUE, -- メールアドレス(ログイン時のID)
    birthdate VARCHAR(25), -- 生年月日
    account_type VARCHAR(1) NOT NULL, -- 口座種別(普通 = 1, 当座 = 2)
    account_number VARCHAR(10) UNIQUE, -- 口座番号
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- アカウント作成日時
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- 最終更新日時
);

-- 取引履歴テーブル
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER AUTO_INCREMENT PRIMARY KEY, -- 取引ID
    user_id INTEGER NOT NULL, -- 取引を行ったユーザーのID
    to_account_number VARCHAR(10), -- 振込先の口座番号（振込の場合）
    transaction_type VARCHAR(100) NOT NULL,  -- 取引の種類
    amount DECIMAL(12, 0) NOT NULL, -- 取引金額
    balance_after DECIMAL(15, 0) NOT NULL, -- 取引後の残高
    related_user VARCHAR(200),  -- 振込の場合、相手方のユーザー名
    description VARCHAR(255), -- 取引の説明
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 取引日時
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
