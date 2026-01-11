import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# 페이지 설정
st.set_page_config(page_title="현장 출퇴근 시스템", layout="centered")

# 구글 시트 연결 설정 (최신 인증 방식)
@st.cache_resource
def get_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Secrets에서 인증 정보 가져오기
    try:
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)
        
        # 시트 이름이 '출근현황'인지 확인
        return client.open("출근현황").get_worksheet(0)
    except Exception as e:
        st.error(f"인증 정보 읽기 실패: {e}")
        return None

# 시트 가져오기
sheet = get_sheet()

if sheet is None:
    st.error("구글 시트 연결에 실패했습니다. Secrets 설정을 확인해주세요.")
    st.stop()

# 직원 명단 (25명으로 채워주세요)
employees = {
    "101": "강민수", "102": "김지아", "103": "박준형", "104": "이현우", "105": "최윤서",
    "106": "정다은", "107": "홍길동", "108": "이미소", "109": "장우진", "110": "한결",
    # 필요하신 만큼 추가하세요
}

st.title("🏗️ 현장 출퇴근 기록기")
st.write("직원 번호를 입력하고 출근/퇴근을 선택하세요.")

emp_id = st.text_input("직원 번호 입력", type="password")

if emp_id:
    if emp_id in employees:
        name = employees[emp_id]
        st.success(f"확인되었습니다: {name} 님")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("☀️ 출근하기", use_container_width=True):
                now = datetime.now()
                sheet.append_row([now.strftime("%Y-%m-%d"), name, "출근", now.strftime("%H:%M:%S")])
                st.balloons()
                st.info(f"{name} 님 출근 기록 완료! ({now.strftime('%H:%M:%S')})")
        with col2:
            if st.button("🌙 퇴근하기", use_container_width=True):
                now = datetime.now()
                sheet.append_row([now.strftime("%Y-%m-%d"), name, "퇴근", now.strftime("%H:%M:%S")])
                st.warning(f"{name} 님 퇴근 기록 완료! ({now.strftime('%H:%M:%S')})")
    else:
        st.error("등록되지 않은 번호입니다.")