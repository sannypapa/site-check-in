import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="현장 출퇴근 기록기", layout="centered")

# 2. 구글 시트 연결 함수
@st.cache_resource
def get_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # 파일 대신 Streamlit의 '금고(Secrets)'에서 정보를 가져옵니다
    creds_info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("출근현황").get_worksheet(0)

# 3. 연결 시도
try:
    sheet = get_sheet()
except Exception as e:
    st.error(f"연결 실패! Secrets 설정을 확인하세요: {e}")
    st.stop()

# 4. 직원 명단 (여기서 성함을 수정하세요)
employees = {"101": "강민수", "102": "김지아", "103": "박준형", "104": "이현우", "105": "최윤서"}

# 5. 화면 구성
st.title("🏗️ 현장 출퇴근 기록기")
emp_id = st.text_input("직원 번호 입력", type="password")

if emp_id in employees:
    name = employees[emp_id]
    st.success(f"반갑습니다, {name} 님")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("☀️ 출근하기", use_container_width=True):
            now = datetime.now()
            sheet.append_row([now.strftime("%Y-%m-%d"), name, "출근", now.strftime("%H:%M:%S")])
            st.balloons()
    with col2:
        if st.button("🌙 퇴근하기", use_container_width=True):
            now = datetime.now()
            sheet.append_row([now.strftime("%Y-%m-%d"), name, "퇴근", now.strftime("%H:%M:%S")])
            st.snow()
elif emp_id:
    st.error("등록되지 않은 번호입니다.")