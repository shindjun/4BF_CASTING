import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(page_title="BlastTap: 고로 출선 매니저", layout="centered")
st.title("🔥 BlastTap: 고로 출선 매니저 🔥")

# ① 출선구 설정
st.header("① 출선구 설정")
lead_phi = st.number_input("선행 출선구 비트경 (Φ, mm)", min_value=30.0, value=45.0)
follow_phi = st.number_input("후행 출선구 비트경 (Φ, mm)", min_value=30.0, value=45.0)

# ② 출선조건 입력
st.header("② 출선 조건 입력")
tap_amount = st.number_input("1회 출선량 (ton)", value=1215.0)
wait_time = st.number_input("출선 간격 (분)", value=15.0)

# ③ 출선 시작시각 입력
st.header("③ 출선 시작 시각 입력")
tap_start_time = st.time_input("출선 시작 시각", value=datetime.time(10, 0))

# ④ 현장 실측 조업 데이터 입력
st.header("④ 현장 실측 조업 데이터 입력")
ore_charge = st.number_input("1회 Ore 장입량 (ton)", value=165.1)
coke_charge = st.number_input("1회 Coke 장입량 (ton)", value=33.5)
daily_charge = st.number_input("일일 Charge 수", value=126)
tfe_percent = st.number_input("T.Fe (%)", value=58.0)
daily_production = st.number_input("일일생산량 (ton)", value=12500.0)
reduction_ratio_actual = st.number_input("R.R (풍구앞, kg/T-P)", value=499.4)
carbon_rate_actual = st.number_input("C.R (풍구앞, kg/T-P)", value=338.9)
pcr_actual = st.number_input("PCR (kg/T-P)", value=167.6)
slag_ratio = st.number_input("출선비 (용선:슬래그)", value=2.25)
iron_speed_actual = st.number_input("실측 출선속도 (ton/min)", value=4.80)
air_flow_actual = st.number_input("풍량 (Nm³/min)", value=7189.0)
oxygen_injection_actual = st.number_input("산소부화량 (Nm³/hr)", value=36926.0)

# --- 실측 교정된 K값 적용
k_calibrated = iron_speed_actual / (lead_phi ** 2)
calc_K_lead = k_calibrated
calc_K_follow = k_calibrated

lead_speed_est = calc_K_lead * lead_phi ** 2
follow_speed_est = calc_K_follow * follow_phi ** 2
dual_speed_est = lead_speed_est + follow_speed_est

lead_time_est = tap_amount / lead_speed_est
follow_time_est = tap_amount / follow_speed_est
dual_time_est = tap_amount / dual_speed_est

# 선행출선 종료시각 (150분 고정)
tap_start_dt = datetime.datetime.combine(datetime.date.today(), tap_start_time)
lead_end_time = tap_start_dt + datetime.timedelta(minutes=150)
recommended_delay = 12
follow_start_time = lead_end_time + datetime.timedelta(minutes=recommended_delay)

# 저선량 및 환원제비 계산
total_ore = ore_charge * daily_charge
total_fe_input = total_ore * (tfe_percent / 100)
reduction_ratio_calc = daily_production / total_fe_input if total_fe_input > 0 else 0

slag_amount = daily_production / slag_ratio
furnace_total = daily_production + slag_amount
current_residual = furnace_total * 0.05

if current_residual >= 60:
    next_follow_recommend = "저선량 과다 → 즉시 후행출선 권장"
else:
    next_follow_recommend = f"선행출선속도 5ton/min 근접시 또는 최소 {recommended_delay}분 후 진행 권장"

# ⑤ 결과 출력
st.header("⑤ 출선 예측 결과")
st.write(f"선행 출선속도: {lead_speed_est:.2f} ton/min → 출선시간: {lead_time_est:.1f} 분")
st.write(f"후행 출선속도: {follow_speed_est:.2f} ton/min → 출선시간: {follow_time_est:.1f} 분")
st.write(f"출선 Lap 타임: {dual_time_est:.2f} 분")
st.write(f"선행 종료시각: {lead_end_time.strftime('%H:%M:%S')}")
st.write(f"후행 추천시각: {follow_start_time.strftime('%H:%M:%S')}")

st.header("⑥ 저선량 및 환원제비 분석")
st.write(f"총 예상 저선량: {current_residual:.1f} ton")
st.write(f"예상 용선량: {daily_production:.1f} ton")
st.write(f"예상 슬래그량: {slag_amount:.1f} ton")
st.write(f"계산 환원제비 (R.R): {reduction_ratio_calc:.3f}")
st.write(f"실측 환원제비 (R.R): {reduction_ratio_actual/1000:.3f}")
st.write(f"탄소소비율 (C.R): {carbon_rate_actual/1000:.3f} ton/T-P")
st.write(f"분탄주입율 (PCR): {pcr_actual/1000:.3f} ton/T-P")

st.success(next_follow_recommend)
