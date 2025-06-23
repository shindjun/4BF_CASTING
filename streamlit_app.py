import streamlit as st

st.title("🔥 고로 저선량 계산기")

st.markdown("""
이 계산기는 다음 공식에 기반합니다:  
**저선량 = T-time × 출선속도**
- T-time: 분(min)
- 출선속도: ton/min
- 저선량: ton
""")

# 입력방식 선택
option = st.radio("어떤 항목을 계산할까요?", ["저선량 계산", "T-time 계산", "출선속도 계산"])

if option == "저선량 계산":
    t_time = st.number_input("T-time (분)", min_value=1.0, value=120.0, step=1.0)
    speed = st.number_input("출선속도 (ton/min)", min_value=0.1, value=8.0, step=0.1)
    result = t_time * speed
    st.success(f"✅ 현재 저선량은 **{result:.2f} ton** 입니다.")

elif option == "T-time 계산":
    hot_metal = st.number_input("현재 저선량 (ton)", min_value=1.0, value=86.0, step=1.0)
    speed = st.number_input("출선속도 (ton/min)", min_value=0.1, value=8.0, step=0.1)
    result = hot_metal / speed
    st.success(f"✅ T-time은 약 **{result:.2f} 분** 입니다.")

elif option == "출선속도 계산":
    hot_metal = st.number_input("현재 저선량 (ton)", min_value=1.0, value=86.0, step=1.0)
    t_time = st.number_input("T-time (분)", min_value=1.0, value=120.0, step=1.0)
    result = hot_metal / t_time
    st.success(f"✅ 출선속도는 **{result:.2f} ton/min** 입니다.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="고로 실시간 저선량 추정기", layout="wide")
st.title("🔥 고로 실시간 저선량 추정기 (by 신동준)")

st.markdown("""
이 앱은 분당 **선철생산량과 출선량의 차이**를 시간 누적으로 계산하여 
**현재 고로 내 저선량(Hot Metal Level)**을 추정합니다.
""")

# --- 입력부 ---
st.sidebar.header("🔧 입력 항목")

start_time = st.sidebar.time_input("시작 시각", value=datetime.now().replace(hour=7, minute=0).time())
total_hours = st.sidebar.number_input("총 추적 시간 (시간)", min_value=1, max_value=48, value=12)
time_interval = st.sidebar.number_input("시간 간격 (분)", min_value=1, max_value=60, value=10)

initial_hot_metal = st.sidebar.number_input("초기 저선량 (ton)", min_value=0.0, value=3800.0, step=10.0)

prod_rate = st.sidebar.number_input("선철 생산속도 (ton/min)", min_value=0.0, value=8.9, step=0.1)

st.sidebar.markdown("### 출선속도 (각 출선구)")
tap1 = st.sidebar.number_input("출선구1 (ton/min)", min_value=0.0, value=2.0, step=0.1)
tap2 = st.sidebar.number_input("출선구2 (ton/min)", min_value=0.0, value=2.0, step=0.1)
tap3 = st.sidebar.number_input("출선구3 (ton/min)", min_value=0.0, value=2.0, step=0.1)
tap4 = st.sidebar.number_input("출선구4 (ton/min)", min_value=0.0, value=2.0, step=0.1)

total_tap_rate = tap1 + tap2 + tap3 + tap4

# --- 시간 생성 ---
now = datetime.combine(datetime.today(), start_time)
times = [now + timedelta(minutes=i*time_interval) for i in range(int(total_hours*60/time_interval))]

# --- 계산 ---
hot_metal = [initial_hot_metal]
for i in range(1, len(times)):
    delta = (prod_rate - total_tap_rate) * time_interval
    new_level = max(hot_metal[-1] + delta, 0)
    hot_metal.append(new_level)

# --- 데이터프레임 구성 ---
df = pd.DataFrame({
    "시간": times,
    "생산속도 (ton/min)": [prod_rate]*len(times),
    "출선속도 총합 (ton/min)": [total_tap_rate]*len(times),
    "저선량 (ton)": hot_metal
})

# --- 시각화 ---
st.subheader("📈 시간대별 저선량 변화")
st.line_chart(df.set_index("시간")["저선량 (ton)"])

# --- 테이블 출력 ---
st.subheader("📋 상세 데이터")
st.dataframe(df, use_container_width=True)

# --- 경고 출력 ---
if hot_metal[-1] < 150:
    st.error(f"🚨 경고: 최종 저선량이 {hot_metal[-1]:.1f}ton으로 150ton 미만입니다! 출선 종료 또는 Tap 전환 필요!")
else:
    st.success(f"✅ 최종 저선량은 {hot_metal[-1]:.1f}ton 입니다. 정상 범위입니다.")


