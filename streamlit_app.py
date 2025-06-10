import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="고로 출선작업 계산기", layout="centered")
st.title("고로 출선작업 계산기 🔥")

# --- 출선구 설정 ---
st.header("① 출선구 설정")
lead_phi = st.number_input("선행 출선구 비트경 (Φ, mm)", min_value=30.0, value=45.0, step=1.0)
follow_phi = st.number_input("후행 출선구 비트경 (Φ, mm)", min_value=30.0, value=45.0, step=1.0)

# --- 출선 조건 입력 ---
st.header("② 출선 조건 입력")
tap_amount = st.number_input("1회 출선량 (ton)", min_value=0.0, value=1358.0, step=1.0)
wait_time = st.number_input("출선 간격 (분)", min_value=0.0, value=15.0, step=1.0)

# --- 출선 시작시각 입력 ---
st.header("③ 출선 시작 시각 입력")
tap_start_time = st.time_input("출선 시작 시각", value=datetime.time(10, 0))

# --- 현재 출선속도 입력 ---
st.header("④ 현재 출선속도 입력")
lead_current_speed = st.number_input("선행 출선속도 (ton/min)", min_value=0.0, value=8.0)
follow_current_speed = st.number_input("후행 출선속도 (ton/min)", min_value=0.0, value=8.0)

# --- 고로 조업 입력 ---
st.header("⑤ 고로 조업 입력")
ore_coke_ratio = st.number_input("Ore/Coke 비율", min_value=0.0, step=0.01)
air_flow = st.number_input("풍량 (Nm³/min)", min_value=0.0)
air_pressure = st.number_input("풍압 (kg/cm²)", min_value=0.0)
furnace_pressure = st.number_input("노정압 (kg/cm²)", min_value=0.0)
furnace_temperature = st.number_input("용선온도 (°C)", min_value=0.0)
oxygen_injection = st.number_input("산소부화량 (Nm³/hr)", min_value=0.0)
moisture_content = st.number_input("조습량 (g/Nm³)", value=0.0)
tfe_percent = st.number_input("T.Fe (%)", min_value=0.0, value=58.0)
daily_production = st.number_input("일일생산량 (ton)", min_value=0.0)
raw_material_granulation = st.number_input("원료 입도 (mm)", min_value=0.0)
furnace_lifetime = st.number_input("고로 수명 (년)", min_value=0, value=0, step=1)
ore_charge = st.number_input("1회 Ore 장입량 (ton)", value=165.0)
coke_charge = st.number_input("1회 Coke 장입량 (ton)", value=33.0)
daily_charge = st.number_input("일일 Charge 수", value=126)
charge_per_hour = st.number_input("시간당 평균 Charge 횟수 (ch/h)", min_value=0.0, value=5.25)
iron_speed = st.number_input("선철 생성속도 (ton/min)", value=9.0)
slag_ratio = st.number_input("출선비 (용선:슬래그)", value=2.25)
pcr = st.number_input("PCR (분탄 주입률, kg/T-P)", value=150)
carbon_rate = st.number_input("C.R (탄소 소비율, kg/T-P)", value=480)

# --- 보정 회수율 및 속도 계산 ---
base_recovery_rate = 0.75
recovery_rate = base_recovery_rate * (tfe_percent / 58.0)
recovery_rate *= (1 + (pcr / 200 - 0.75) * 0.1)
recovery_rate *= (1 + (carbon_rate - 450) / 1000 * 0.05)
recovery_rate = min(recovery_rate, 0.90)

base_k_lead = lead_current_speed / (lead_phi ** 2) if lead_phi > 0 else 0
base_k_follow = follow_current_speed / (follow_phi ** 2) if follow_phi > 0 else 0
k_boost = 1.0 + (oxygen_injection / 5000) * 0.1 + (air_flow / 3000) * 0.05
calc_K_lead = base_k_lead * k_boost
calc_K_follow = base_k_follow * k_boost

lead_speed_est = calc_K_lead * lead_phi ** 2
follow_speed_est = calc_K_follow * follow_phi ** 2
dual_speed_est = lead_speed_est + follow_speed_est

lead_time_est = tap_amount / lead_speed_est if lead_speed_est > 0 else 0
follow_time_est = tap_amount / follow_speed_est if follow_speed_est > 0 else 0
dual_time_est = tap_amount / dual_speed_est if dual_speed_est > 0 else 0

# --- 출선 종료 시각 계산 ---
tap_start_dt = datetime.datetime.combine(datetime.date.today(), tap_start_time)
lead_end_time = tap_start_dt + datetime.timedelta(minutes=lead_time_est)
follow_start_time = lead_end_time + datetime.timedelta(minutes=3)

# --- 결과 출력 ---
st.header("⑥ 출선 시간 예측 결과")
st.write(f"🔹 선행 출선속도: {lead_speed_est:.2f} ton/min → 출선시간: {lead_time_est:.1f} 분")
st.write(f"🔹 후행 출선속도: {follow_speed_est:.2f} ton/min → 출선시간: {follow_time_est:.1f} 분")
st.write(f"✅ 2공 동시 출선 예상시간: {dual_time_est:.2f} 분")
st.write(f"⏱ 선행 출선 종료시각: {lead_end_time.strftime('%H:%M:%S')}")
st.write(f"⏱ 권장 후행 출선 시작시각: {follow_start_time.strftime('%H:%M:%S')}")
