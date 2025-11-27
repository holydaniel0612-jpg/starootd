import streamlit as st
import os
import json
import datetime
import base64

# --- 1. 페이지 설정 & 디자인 ---
st.set_page_config(page_title="StarOOTD", page_icon="🌟", layout="wide")

# CSS: 디자인을 예쁘게 꾸며주는 코드 (상단바, 로고, 검색창 중심으로 재구성)
st.markdown("""
    <style>
    /* 전체 배경색 */
    .stApp {
        background-color: #f8f9fa; /* 연한 회색 배경 */
        color: #333;
    }
    
    /* Streamlit 기본 헤더/푸터 숨기기 (깔끔하게 직접 배치하기 위해) */
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* Streamlit 사이드바 기본 스타일 조정 */
    .st-emotion-cache-1ldb789 { /* 사이드바 컨테이너 ID (버전마다 다를 수 있음) */
        background-color: #ffffff; /* 사이드바 배경색 흰색 */
        box-shadow: 2px 0 10px rgba(0,0,0,0.05); /* 그림자 */
    }
    .st-emotion-cache-1kyxreqx { /* 사이드바 헤더 (New OOTD) */
        color: #2c3e50;
        font-size: 1.5em;
        font-weight: bold;
        padding-bottom: 20px;
        border-bottom: 1px solid #eee;
        margin-bottom: 20px;
    }

    /* 메인 컨텐츠 상단 로고 및 검색바 컨테이너 */
    .main-header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px 0 40px 0; /* 상단 여백, 하단 여백 */
        background-color: #ffffff; /* 로고/검색창 배경도 흰색으로 */
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 30px; /* 메인 컨텐츠와 구분선 */
        border-radius: 10px; /* 컨테이너 모서리 둥글게 */
    }
    .main-header-logo {
        max-width: 100px; /* 로고 크기 조절 */
        height: auto;
        margin-bottom: 15px; /* 로고 아래 간격 */
        border-radius: 15px; /* 로고 둥근 모서리 */
    }

    /* 검색창 스타일 */
    .stTextInput > div > div > input {
        text-align: center; /* 플레이스홀더 중앙 정렬 */
        border-radius: 25px; /* 둥근 모서리 */
        padding: 10px 15px;
        width: 80%; /* 검색창 너비 조정 */
        max-width: 400px;
        border: 1px solid #ddd;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3498db; /* 포커스 시 색상 */
        box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
    }
    
    /* 이미지 카드 스타일 (기존 유지) */
    div[data-testid="stImage"] img {
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    div[data-testid="stImage"] img:hover {
        transform: scale(1.02);
    }
    
    /* 캡션과 태그 텍스트 (기존 유지) */
    .caption-style {
        font-size: 15px;
        color: #444;
        margin-top: 5px;
    }
    .tag-style {
        color: #0066cc;
        font-weight: bold;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 세션 상태 초기화 (사이드바 열림/닫힘 상태 관리) ---
if 'sidebar_state' not in st.session_state:
    st.session_state['sidebar_state'] = 'expanded' # 기본으로 열린 상태

# --- 2. 데이터 관리 (저장소) ---
DATA_FILE = "ootd_data.json"
IMAGE_FOLDER = "images"

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 3. 화면 구성 ---

# 사이드바 열림/닫힘 버튼 (Streamlit의 기본 토글을 사용하도록 유도)
# st.set_page_config의 initial_sidebar_state를 이용하거나,
# st.sidebar.button 등으로 컨트롤 가능. 여기서는 Streamlit 기본 동작에 맡김.

# [사이드바] 업로드 기능
with st.sidebar:
    st.header("➕ New OOTD")
    uploaded_file = st.file_uploader("사진을 넣어주세요", type=['png', 'jpg', 'jpeg'])
    
    # 입력창들
    caption = st.text_input("📝 한줄 메모")
    tags_input = st.text_input("🏷️ 태그 입력", placeholder="#데이트 #여름")
    
    # 저장 버튼 (빨간색)
    if st.button("✨ 기록 저장하기", type="primary", use_container_width=True):
        if uploaded_file is not None:
            # 1. 이미지 파일 저장
            file_path = os.path.join(IMAGE_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. 글 내용 저장
            new_entry = {
                "filename": uploaded_file.name,
                "caption": caption,
                "tags": tags_input,
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            
            current_data = load_data()
            current_data.append(new_entry)
            save_data(current_data)
            
            st.success("저장 완료!")
            st.rerun()
        else:
            st.warning("사진을 먼저 선택해주세요!")

# [메인 화면] 상단 로고 및 검색바 (가운데 정렬)
logo_path = os.path.join(IMAGE_FOLDER, "logo_white.png")
logo_base64 = ""

if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode("utf-8")

st.markdown(f"""
    <div class="main-header-container">
        <img src="data:image/png;base64,{logo_base64}" class="main-header-logo" alt="StarOOTD Logo">
        <input type="text" placeholder="태그나 메모 내용을 입력하세요" class="stTextInput_input" style="width: 80%; max-width: 400px; text-align: center;">
    </div>
""", unsafe_allow_html=True)


st.markdown("---") # 구분선

# [갤러리] 사진 보여주기
data = load_data()
data.reverse() # 최신순

# 검색 필터
# (검색창 연동은 나중에 기능 추가할 때 진행, 지금은 디자인만)
search_query = "" # 현재 검색 기능은 비활성화 상태 (상단 검색창은 HTML로 임시 배치)

if search_query:
    filtered_data = [item for item in data if search_query in item['tags'] or search_query in item['caption']]
else:
    filtered_data = data

# 결과 없음 표시
if not filtered_data:
    st.markdown("<br><h3 style='text-align: center; color: #aaa;'>저장된 코디가 없어요 ☁️</h3>", unsafe_allow_html=True)

# 4열 그리드로 배치
cols = st.columns(4)

for i, item in enumerate(filtered_data):
    col = cols[i % 4]
    with col:
        # 이미지
        img_path = os.path.join(IMAGE_FOLDER, item['filename'])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
            
            # 텍스트 예쁘게 보여주기
            if item['tags']:
                st.markdown(f"<div class='tag-style'>{item['tags']}</div>", unsafe_allow_html=True)
            if item['caption']:
                st.markdown(f"<div class='caption-style'>{item['caption']}</div>", unsafe_allow_html=True)
            
            st.caption(f"{item['date']}")
            
            # 삭제 버튼
            if st.button("삭제", key=f"del_{i}"):
                original_data = load_data()
                # 파일명으로 찾아서 삭제
                original_data = [d for d in original_data if d['filename'] != item['filename']]
                save_data(original_data)
                
                # 실제 파일도 삭제
                if os.path.exists(img_path):
                    os.remove(img_path)
                st.rerun()