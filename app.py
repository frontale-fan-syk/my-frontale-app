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
    
    # 勝ち点の計算ロジック
    def calc_points(res):
        if res == "90分勝": return 3
        elif res == "PK勝": return 2
        elif res == "PK負": return 1
        elif res == "90分負": return 0
        else: return 0

    # 数値計算
    total_points = df["結果"].apply(calc_points).sum()
    latest_rank = df["順位"].iloc[-1] if "順位" in df.columns else "-"
    total_games = len(df)
    counts = df["結果"].value_counts()

    # --- 1段目：メイン指標 (2x2で配置) ---
    # 試合数が中途半端に余るので、3つ＋空欄 または 4つめの指標を入れると綺麗です
    m_row1_col1, m_row1_col2 = st.columns(2)
    m_row2_col1, m_row2_col2 = st.columns(2)

    with m_row1_col1:
        st.metric("🔥 総勝ち点", f"{total_points} pt")
    with m_row1_col2:
        st.metric("🏆 最新順位", f"{latest_rank} 位")
    with m_row2_col1:
        st.metric("⚽ 試合数", f"{total_games} 試合")
    with m_row2_col2:
        # 4つ目が空くと寂しいので「平均勝ち点」などを入れるのもアリです！
        avg_points = round(total_points / total_games, 2) if total_games > 0 else 0
        st.metric("📈 平均勝ち点", f"{avg_points}")

    st.markdown("---") # 区切り線

    # --- 2段目：戦績詳細 (2x2で配置) ---
    st.write("**戦績内訳**")
    d_row1_col1, d_row1_col2 = st.columns(2)
    d_row2_col1, d_row2_col2 = st.columns(2)

    with d_row1_col1:
        st.metric("90分勝", f"{counts.get('90分勝', 0)}回")
    with d_row1_col2:
        st.metric("PK勝", f"{counts.get('PK勝', 0)}回")
    with d_row2_col1:
        st.metric("PK負", f"{counts.get('PK負', 0)}回")
    with d_row2_col2:
        st.metric("90分負", f"{counts.get('90分負', 0)}回")

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





