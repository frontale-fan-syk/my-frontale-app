import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="フロンターレ戦績管理", layout="centered")
st.title("🐬 フロンターレ戦績管理")

# --- データ読み込み ---
conn = st.connection("gsheets", type=GSheetsConnection)
try:
    # 最新データを読み込む
    df = conn.read(ttl=0)
except:
    df = pd.DataFrame()

# --- 1. 成績まとめ (Dashboard) ---
if not df.empty:
    st.subheader("📊 今シーズンの状況")
    
    # 勝ち点の新ルール適用
    def calc_points(res):
        if res == "90分勝": return 3
        elif res == "PK勝": return 2
        elif res == "PK負": return 1
        elif res == "90分負": return 0
        else: return 0  # 念のため、それ以外（引き分けなど）は0

    # 全試合の勝ち点を合計
    total_points = df["結果"].apply(calc_points).sum()
    
    # 以下はそのまま
    latest_rank = df["順位"].iloc[-1] if "順位" in df.columns else "-"
    total_games = len(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("総勝ち点", f"{total_points} pt")
    col2.metric("最新順位", f"{latest_rank} 位")
    col3.metric("試合数", f"{total_games} 試合")

st.markdown("---")

# --- 2. 戦績一覧 (Table) ---
st.subheader("📅 戦績一覧")
if not df.empty:
    # タイムスタンプ列が存在する場合、それを除外した新しい表(display_df)を作る
    display_df = df.drop(columns=["タイムスタンプ"], errors="ignore")
    
    # スプレッドシートと同じ並び（最新が一番下）で表示
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("データがまだありません。下のフォームから入力してください。")

# --- 3. 入力エリア (Googleフォーム) ---
with st.expander("➕ 新しい試合結果を入力する", expanded=False):
    # 【https://docs.google.com/forms/d/e/1FAIpQLSerTyVg6oe6KDo887eBIfBXP4_Y9jhW-WujXooSFbZa3NBE0g/viewform?usp=dialog】
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSerTyVg6oe6KDo887eBIfBXP4_Y9jhW-WujXooSFbZa3NBE0g/viewform?usp=dialog"
    
    if "http" in form_url:
        st.components.v1.iframe(form_url, height=600, scrolling=True)
    else:
        st.warning("GoogleフォームのURLを設定してください。")


