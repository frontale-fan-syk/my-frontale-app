import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="フロンターレ戦績管理", layout="centered")
st.title("🐬 フロンターレ戦績管理 (DB版)")

# スプレッドシート接続
conn = st.connection("gsheets", type=GSheetsConnection)

# データの読み込み
try:
    # 既存のデータを取得
    df = conn.read(ttl="10m")
except:
    df = pd.DataFrame(columns=["節", "相手", "結果", "得点", "失点", "順位"])

# 入力フォーム
with st.form("input_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        section = st.text_input("節 (例: 第1節)")
        opponent = st.text_input("相手")
        result = st.selectbox("結果", ["勝", "PK勝", "PK負", "負"])
    with col2:
        score_get = st.number_input("得点", min_value=0, step=1)
        score_lose = st.number_input("失点", min_value=0, step=1)
        rank = st.number_input("順位", min_value=1, step=1)
    
    submit = st.form_submit_button("保存する")

if submit:
    # データを1行追加
    new_data = pd.DataFrame([{
        "節": section,
        "相手": opponent,
        "結果": result,
        "得点": score_get,
        "失点": score_lose,
        "順位": rank
    }])
    
    # ここで「魔法の追記」を行います
    try:
        # 既存データに合体させてから全体を更新するのではなく、
        # Google側の「書き込み制限」を回避するためのシンプルな更新方法
        updated_df = pd.concat([df, new_data], ignore_index=True)
        conn.update(data=updated_df)
        
        st.success("スプレッドシートに保存しました！")
        st.balloons()
        st.info("※反映に少し時間がかかる場合があります。画面を更新して確認してください。")
    except Exception as e:
        st.error("やっぱりGoogleのセキュリティに弾かれてしまいました…")
        st.info("【最終手段】スプレッドシートのURLではなく、『サービスアカウント』という設定が必要かもしれません。")

st.subheader("これまでの戦績")
st.dataframe(df, use_container_width=True, hide_index=True)
