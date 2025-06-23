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
