import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="고로 실시간 저선량 추정기", layout="wide")
st.title("🔥 고로 실시간 저선량 추정기 (by 신동준)")

st.markdown("""
이 앱은 **07:00 기준 하루 단위(익일 07:00까지)**로 분당 **선철생산량과 출선량의 차이**를 누적 계산하여 
**현재 고로 내 저선량(Hot Metal Level)**을 추정합니다.

초기 저선량은 T-time 기준으로 자동 계산되며,
현재까지 종료된 출선량은 수기로 입력해 계산 정확도를 높입니다.
""")

# --- 입력부 ---
st.sidebar.header("🔧 입력 항목")

start_time = st.sidebar.time_input("기준 시작 시각 (보통 07:00)", value=datetime.now().replace(hour=7, minute=0).time())
total_hours = st.sidebar.number_input("총 추적 시간 (시간)", min_value=1, max_value=48, value=24)
time_interval = st.sidebar.number_input("시간 간격 (분)", min_value=1, max_value=60, value=10)

# T-time 및 생성속도 입력
t_time_min = st.sidebar.number_input("T-time (분 단위)", min_value=1.0, value=420.0, step=1.0)
prod_rate = st.sidebar.number_input("선철 생산속도 (ton/min)", min_value=0.1, value=9.0, step=0.1)

# 누적 생성량 계산
cumulative_generated = prod_rate * t_time_min
st.sidebar.markdown(f"🔄 누적 생성량: **{cumulative_generated:.1f} ton**")

# 종료된 출선량 수기 입력
completed_tap_output = st.sidebar.number_input("📌 현재까지 종료된 출선량 (ton)", min_value=0.0, value=3600.0, step=10.0)

# 초기 저선량
initial_hot_metal = cumulative_generated - completed_tap_output
st.sidebar.markdown(f"▶️ 초기 저선량 추정값: **{initial_hot_metal:.1f} ton**")

# 출선속도 입력
tap1 = st.sidebar.number_input("출선구1 (ton/min)", min_value=0.0, value=2.0, step=0.1)
tap2 = st.sidebar.number_input("출선구2 (ton/min)", min_value=0.0, value=2.0, step=0.1)
tap3 = st.sidebar.number_input("출선구3 (ton/min)", min_value=0.0, value=2.0, step=0.1)
tap4 = st.sidebar.number_input("출선구4 (ton/min)", min_value=0.0, value=2.0, step=0.1)

total_tap_rate = tap1 + tap2 + tap3 + tap4

# 시간 생성
now = datetime.combine(datetime.today(), start_time)
times = [now + timedelta(minutes=i*time_interval) for i in range(int(total_hours*60/time_interval))]

# 계산
hot_metal = [initial_hot_metal]
cumulative_real_tap_out = 0.0
for i in range(1, len(times)):
    tap_out = total_tap_rate * time_interval
    cumulative_real_tap_out += tap_out
    new_level = max(initial_hot_metal - cumulative_real_tap_out, 0)
    hot_metal.append(new_level)

# 데이터프레임 구성
df = pd.DataFrame({
    "시간": times,
    "실시간 누적 출선량 (ton)": [completed_tap_output + total_tap_rate * time_interval * i for i in range(len(times))],
    "저선량 (ton)": hot_metal
})

# 시각화
st.subheader("📈 시간대별 저선량 변화")
st.line_chart(df.set_index("시간")["저선량 (ton)"])

# 테이블 출력
st.subheader("📋 상세 데이터")
st.dataframe(df, use_container_width=True)

# 최종 저선량 표시
st.subheader("✅ 최종 저선량")
st.metric(label="최종 저선량 (ton)", value=f"{hot_metal[-1]:.1f} ton")

# 경고 출력
if hot_metal[-1] >= 150:
    st.error(f"[경고] 최종 저선량이 {hot_metal[-1]:.1f}ton으로 150ton 이상입니다. 고로 Tap 과다 저선 주의 필요.")
else:
    st.success(f"✅ 최종 저선량은 {hot_metal[-1]:.1f}ton 입니다. 정상 범위입니다.")
