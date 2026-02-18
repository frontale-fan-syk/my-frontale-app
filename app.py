import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="フロンターレ戦績管理", layout="centered")
st.title("🐬 フロンターレ戦績管理")

# --- 1. 入力エリア (Googleフォーム) ---
st.subheader("📝 試合結果を入力")

# ここに【Googleフォーム】のURLを貼る
# ※最後が viewform?embedded=true になっているものです
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSerTyVg6oe6KDo887eBIfBXP4_Y9jhW-WujXooSFbZa3NBE0g/viewform?usp=dialog"

if "docs.google.com/forms" in form_url:
    st.components.v1.iframe(form_url, height=600, scrolling=True)
else:
    st.warning("GoogleフォームのURLを正しく貼り付けてください。")

st.markdown("---")

# --- 2. 表示エリア (スプレッドシート) ---
st.subheader("📊 これまでの戦績")
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # ttl=0で最新のデータを読み込む
    df = conn.read(ttl=0)
    st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.info("データが入力されると、ここに一覧が表示されます。")
