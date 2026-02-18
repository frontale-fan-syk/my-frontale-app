import streamlit as st

st.set_page_config(page_title="テスト中", layout="centered")
st.title("🐬 フォーム表示テスト")

# あなたがコピーしたURLをここに正しく貼り付けてください
# 前後の " " を消さないように注意！
form_url = "ここにコピーしたURLを貼り付け"

if "http" in form_url:
    st.components.v1.iframe(form_url, height=800, scrolling=True)
else:
    st.error("URLが正しく設定されていないようです。")
