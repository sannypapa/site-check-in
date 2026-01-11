import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 페이지 설정 (모바일에서 보기 좋게)
st.set_page_config(page_title="현장 출퇴근 시스템", layout="centered")

# 구글 시트 연결 (한 번만 실행되도록 설정)
@st.cache_resource
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    return client.open("출근현황").get_worksheet(0)

sheet = get_sheet()

# 직원 명단
# 기존 5명에서 25명으로 확장 예시
employees = {
    "101": "강민수", "102": "김지아", "103": "박준형", "104": "이현우", "105": "최윤서", "106": "정다은", "107": "홍길동", "108": "이미소", "109": "장우진", "110": "한결",
   }

st.title("🏗️ 현장 출퇴근 기록기")
st.write("직원 번호를 입력하고 출근/퇴근을 선택하세요.")

# 입력창 및 버튼
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
                st.balloons() # 축하 효과
                st.info("출근 기록 완료!")
        with col2:
            if st.button("🌙 퇴근하기", use_container_width=True):
                now = datetime.now()
                sheet.append_row([now.strftime("%Y-%m-%d"), name, "퇴근", now.strftime("%H:%M:%S")])
                st.warning("퇴근 기록 완료!")
    else:
        st.error("등록되지 않은 번호입니다.")