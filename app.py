import streamlit as st
import os
import json
import datetime

# --- 1. 페이지 설정 & 디자인 ---
st.set_page_config(page_title="StarOOTD", page_icon="🌟", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1 { text-align: center !important; font-weight: 800 !important; color: #333 !important; padding-top: 0px; }
    .subtitle { text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 30px; }
    div[data-testid="stImage"] img { border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.3s; }
    div[data-testid="stImage"] img:hover { transform: scale(1.02); }
    .caption-style { font-size: 15px; color: #444; margin-top: 5px; }
    .tag-style { color: #0066cc; font-weight: bold; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 관리 ---
DATA_FILE = "ootd_data.json"
IMAGE_FOLDER = "images"

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def load_data():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

# --- 3. 화면 구성 ---
with st.sidebar:
    st.header("➕ New OOTD")
    uploaded_file = st.file_uploader("사진을 넣어주세요", type=['png', 'jpg', 'jpeg'])
    caption = st.text_input("📝 한줄 메모")
    tags_input = st.text_input("🏷️ 태그 입력", placeholder="#데이트 #여름")
    
    if st.button("✨ 기록 저장하기", type="primary", use_container_width=True):
        if uploaded_file is not None:
            file_path = os.path.join(IMAGE_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
            
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

st.title("🌟 Star OOTD")
st.markdown('<div class="subtitle">나만의 데일리 룩북 아카이브</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_query = st.text_input("🔍 검색", placeholder="태그나 메모 내용을 입력하세요")
st.markdown("---")

data = load_data()
data.reverse()

if search_query:
    filtered_data = [item for item in data if search_query in item['tags'] or search_query in item['caption']]
else:
    filtered_data = data

if not filtered_data:
    st.markdown("<br><h3 style='text-align: center; color: #aaa;'>저장된 코디가 없어요 ☁️</h3>", unsafe_allow_html=True)

cols = st.columns(4)
for i, item in enumerate(filtered_data):
    col = cols[i % 4]
    with col:
        img_path = os.path.join(IMAGE_FOLDER, item['filename'])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
            if item['tags']: st.markdown(f"<div class='tag-style'>{item['tags']}</div>", unsafe_allow_html=True)
            if item['caption']: st.markdown(f"<div class='caption-style'>{item['caption']}</div>", unsafe_allow_html=True)
            st.caption(f"{item['date']}")
            if st.button("삭제", key=f"del_{i}"):
                original_data = load_data()
                original_data = [d for d in original_data if d['filename'] != item['filename']]
                save_data(original_data)
                if os.path.exists(img_path): os.remove(img_path)
                st.rerun()