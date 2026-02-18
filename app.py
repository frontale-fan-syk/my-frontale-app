import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="フロンターレ戦績管理", layout="centered")
st.title("🐬 フロンターレ戦績管理 (DB版)")

# スプレッドシートとの接続
conn = st.connection("gsheets", type=GSheetsConnection)

# 既存データを読み込む（失敗しても空の表を作る）
try:
    df = conn.read(ttl=0) # キャッシュを無効にして最新を読む
except:
    df = pd.DataFrame(columns=["日付", "対戦相手", "スコア", "結果"])

# 入力フォーム
with st.form("input_form"):
    date = st.date_input("試合日")
    opponent = st.text_input("対戦相手")
    score = st.text_input("スコア (例: 2-1)")
    result = st.selectbox("結果", ["勝ち", "負け", "引き分け"])
    submit = st.form_submit_button("保存する")

if submit:
    if not opponent or not score:
        st.warning("対戦相手とスコアを入力してください")
    else:
        # 新しいデータを作成
        new_data = pd.DataFrame([{
            "日付": str(date),
            "対戦相手": opponent,
            "スコア": score,
            "結果": result
        }])
        
        # 既存データに新しいデータを追加
        updated_df = pd.concat([df, new_data], ignore_index=True)
        
        # 【ここが重要】スプレッドシートを更新
        try:
            conn.update(data=updated_df)
            st.success("スプレッドシートに保存しました！")
            st.balloons() # お祝いの風船
            df = updated_df # 表示用データを更新
        except Exception as e:
            st.error(f"保存に失敗しました。スプレッドシートの『共有』が『編集者』になっているか確認してください。")

# データの表示
st.subheader("これまでの戦績")
st.dataframe(df, use_container_width=True)
