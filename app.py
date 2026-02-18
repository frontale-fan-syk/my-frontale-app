import streamlit as st

st.set_page_config(page_title="テスト中", layout="centered")
st.title("🐬 フォーム表示テスト")

# https://docs.google.com/spreadsheets/d/1gt15QP3KD4O8JZdPOKKh6NvE8EIdsl9dqBp6orNqjwc/edit?resourcekey=&gid=1109624288#gid=1109624288
# 前後の " " を消さないように注意！
form_url = "https://docs.google.com/spreadsheets/d/1gt15QP3KD4O8JZdPOKKh6NvE8EIdsl9dqBp6orNqjwc/edit?resourcekey=&gid=1109624288#gid=1109624288"

if "http" in form_url:
    st.components.v1.iframe(form_url, height=800, scrolling=True)
else:
    st.error("URLが正しく設定されていないようです。")

