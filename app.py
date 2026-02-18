import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("🐬 フロンターレ戦績管理 (DB版)")

# スプレッドシートとの接続設定
conn = st.connection("gsheets", type=GSheetsConnection)

# 既存データの読み込み
df = conn.read()

# 入力フォーム
with st.form("input_form"):
    date = st.date_input("試合日")
    opponent = st.text_input("対戦相手")
    score = st.text_input("スコア (例: 2-1)")
    result = st.selectbox("結果", ["勝ち", "負け", "引き分け"])
    submit = st.form_submit_button("保存する")

if submit:
    # 新しいデータを作成
    new_data = pd.DataFrame([{
        "日付": str(date),
        "対戦相手": opponent,
        "スコア": score,
        "結果": result
    }])
    
    # データを追加して更新
    updated_df = pd.concat([df, new_data], ignore_index=True)
    conn.update(data=updated_df)
    st.success("スプレッドシートに保存しました！")

# データの表示
st.subheader("これまでの戦績")
st.dataframe(updated_df)
