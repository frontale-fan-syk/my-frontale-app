import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="フロンターレ戦績管理", layout="centered")
st.title("🐬 フロンターレ戦績管理 (DB版)")

conn = st.connection("gsheets", type=GSheetsConnection)

# 既存データを読み込む
try:
    df = conn.read(ttl=0)
except:
    df = pd.DataFrame(columns=["節", "相手", "結果", "得点", "失点", "順位"])

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        section = st.text_input("節 (例: 第1節)")
        opponent = st.text_input("相手")
        # 選択肢を「勝」「PK勝」「PK負」「負」に変更
        result = st.selectbox("結果", ["勝", "PK勝", "PK負", "負"])
    with col2:
        score_get = st.number_input("得点", min_value=0, step=1)
        score_lose = st.number_input("失点", min_value=0, step=1)
        rank = st.number_input("順位", min_value=1, step=1)
    
    submit = st.form_submit_button("保存する")

if submit:
    new_data = pd.DataFrame([{
        "節": section,
        "相手": opponent,
        "結果": result,
        "得点": score_get,
        "失点": score_lose,
        "順位": rank
    }])
    
    updated_df = pd.concat([df, new_data], ignore_index=True)
    
    try:
        conn.update(data=updated_df)
        st.success("スプレッドシートに保存しました！")
        st.balloons()
        df = updated_df
    except Exception as e:
        st.error(f"保存に失敗しました。エラー: {e}")

st.subheader("これまでの戦績")
# 表の左側の番号（index）を隠して表示
st.dataframe(df, use_container_width=True, hide_index=True)
