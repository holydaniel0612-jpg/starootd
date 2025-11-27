import streamlit as st
import os
import json
import datetime

# --- 1. 페이지 설정 & 디자인 ---
st.set_page_config(page_title="StarOOTD", page_icon="🌟", layout="wide")

# CSS: 디자인을 예쁘게 꾸며주는 코드
st.markdown("""
    <style>
    /* 전체 배경색 */
    .stApp {
        background-color: #f8f9fa; /* 연한 회색 배경 */
        color: #333;
    }
    
    /* 상단바 컨테이너 (메뉴 - 로고 - 설정) */
    .st-emotion-cache-z5rd5b { /* Streamlit 메인 헤더 컨테이너 ID (버전마다 다를 수 있음) */
        width: 100%;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between; /* 양쪽 끝 정렬 */
        align-items: center;
        background-color: #ffffff; /* 흰색 상단바 배경 */
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        position: sticky;
        top: 0;
        z-index: 1000;
        margin-bottom: 20px; /* 상단바 아래 여백 */
    }

    /* 로고 이미지 스타일 */
    .header-logo {
        display: flex;
        justify-content: center; /* 로고 이미지 자체도 중앙 정렬 */
        flex-grow: 1; /* 로고가 중앙에 오도록 공간 차지 */
    }
    .header-logo img {
        max-width: 80px; /* 로고 크기 확실히 작게 조절 */
        height: auto;
        border-radius: 15px; /* 로고 둥근 모서리 */
        box-shadow: none; /* 그림자 제거 */
    }

    /* 사이드바 토글 (메뉴 아이콘) 위치 조정 */
    .st-emotion-cache-x43p6n { /* 사이드바 토글 버튼 ID (버전마다 다를 수 있음) */
        position: absolute; /* 절대 위치로 상단바 안에 배치 */
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 1001; /* 로고보다 위 */
    }

    /* 설정 아이콘 (오른쪽 상단 Streamlit 기본 메뉴) */
    .st-emotion-cache-163m4l { /* Streamlit 기본 메뉴 버튼 ID (버전마다 다를 수 있음) */
        position: absolute; /* 절대 위치로 상단바 안에 배치 */
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 1001; /* 로고보다 위 */
    }

    /* 검색창 컨테이너 */
    .search-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 30px; /* 검색창 아래 여백 */
    }
    .search-container input {
        width: 60%; /* 검색창 너비 */
        max-width: 500px;
        padding: 10px 15px;
        border: 1px solid #ddd;
        border-radius: 20px;
        font-size: 1rem;
        text-align: center; /* 검색창 플레이스홀더 텍스트 중앙 정렬 */
    }

    /* 메인 제목 숨기기 (로고만 쓸 때) */
    h1 {
        display: none; /* h1 제목은 사용하지 않으므로 숨김 */
    }
    /* 부제목도 숨기기 (로고만 쓸 때) */
    .subtitle {
        display: none; /* 부제목도 사용하지 않으므로 숨김 */
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

# [메인 화면] 로고와 검색 (상단바 스타일)
logo_path = os.path.join(IMAGE_FOLDER, "logo_white.png")

# 상단바 중앙에 로고만 표시
st.markdown(f"""
    <div class="header-logo">
        <img src="data:image/png;base64,{st.image(logo_path, use_column_width=False).image_data.decode('utf-8')}" alt="StarOOTD Logo">
    </div>
""", unsafe_allow_html=True)

# 검색창
st.markdown('<div class="search-container"><input type="text" placeholder="검색어를 입력하세요" /></div>', unsafe_allow_html=True)

st.markdown("---")

# [갤러리] 사진 보여주기
data = load_data()
data.reverse() # 최신순

# 검색 필터
# (검색창 연동은 나중에 기능 추가할 때 진행, 지금은 디자인만)
search_query = "" # 현재 검색 기능은 비활성화 상태

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