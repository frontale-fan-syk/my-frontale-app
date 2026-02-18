import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="フロンターレ戦績管理", layout="centered")
st.title("🐬 フロンターレ戦績管理")

# --- 1. 入力エリア (Googleフォームを埋め込む) ---
st.subheader("📝 今日の試合を入力")

# 【https://docs.google.com/forms/d/e/1FAIpQLSerTyVg6oe6KDo887eBIfBXP4_Y9jhW-WujXooSFbZa3NBE0g/viewform?usp=dialog】
form_url = "こhttps://docs.google.com/forms/d/e/1FAIpQLSerTyVg6oe6KDo887eBIfBXP4_Y9jhW-WujXooSFbZa3NBE0g/viewform?usp=dialog"

st.components.v1.iframe(form_url, height=600, scrolling=True)

st.markdown("---")

# --- 2. 表示エリア (スプレッドシートを読む) ---
st.subheader("📊 これまでの戦績")
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # ttl=0 で常に最新のデータを読み込むようにします
    df = conn.read(ttl=0)
    st.dataframe(df, use_container_width=True, hide_index=True)
except:
    st.info("データがスプレッドシートに入力されると、ここに一覧が表示されます。")
    st.write("※スプレッドシートの共有設定が『閲覧者』以上になっているか確認してくださいね。")
