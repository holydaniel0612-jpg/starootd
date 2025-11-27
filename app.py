<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>starootd</title>
    <style>
        /* --- 전체적인 스타일 --- */
        body {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background-color: #fafafa; /* 아주 연한 회색 배경 */
            margin: 0;
            padding: 20px;
            color: #333;
        }

        /* --- 헤더 (제목과 검색창) --- */
        header {
            text-align: center;
            margin-bottom: 40px;
        }

        h1 {
            font-size: 3em;
            color: #2c3e50; /* 짙은 남색 계열 */
            margin-bottom: 20px;
            letter-spacing: 2px;
            font-weight: 300;
        }

        .search-container input {
            padding: 12px 20px;
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 25px; /* 둥근 검색창 */
            outline: none;
            font-size: 14px;
            transition: border-color 0.3s;
        }

        .search-container input:focus {
            border-color: #3498db; /* 포커스 시 파란색 테두리 */
        }

        /* --- 업로드 섹션 --- */
        .upload-section {
            background: #fff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            max-width: 500px;
            margin: 0 auto 40px auto; /* 가운데 정렬 */
            text-align: center;
        }

        .upload-section h2 {
            margin-top: 0;
            color: #2c3e50;
            font-size: 1.5em;
        }

        .upload-section input[type="text"],
        .upload-section input[type="file"] {
            width: 80%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box;
        }

        .upload-section button {
            background-color: #3498db;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        .upload-section button:hover {
            background-color: #2980b9;
        }

        /* --- 카드 그리드 레이아웃 --- */
        .masonry-container {
            display: grid;
            /* 화면 크기에 따라 컬럼 수 자동 조절, 최소 250px 너비 유지 */
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            grid-gap: 25px; /* 카드 사이 간격 */
            max-width: 1200px;
            margin: 0 auto;
        }

        /* --- 개별 카드 디자인 --- */
        .card {
            background-color: #fff;
            border-radius: 16px; /* 둥근 모서리 */
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); /* 부드러운 그림자 */
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        /* 마우스 올렸을 때 효과 */
        .card:hover {
            transform: translateY(-5px); /* 살짝 위로 떠오름 */
            box-shadow: 0 8px 25px rgba(0,0,0,0.15); /* 그림자 진하게 */
        }

        .card img {
            width: 100%;
            height: 280px; /* 이미지 높이 고정 */
            object-fit: cover; /* 비율 유지하며 꽉 채우기 */
            display: block;
        }

        .card .info {
            padding: 20px;
        }

        .card .tags {
            margin-bottom: 12px;
        }

        /* 태그 스타일 */
        .card .tag {
            display: inline-block;
            background-color: #f0f2f5;
            color: #555;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            margin-right: 6px;
            margin-bottom: 6px;
            font-weight: 500;
        }

        .card .date {
            display: block;
            color: #999;
            font-size: 0.8em;
            margin-bottom: 10px;
            text-align: right; /* 날짜 오른쪽 정렬 */
        }

        .card .memo {
            font-size: 0.95em;
            line-height: 1.5;
            color: #444;
            margin: 0;
        }
    </style>
</head>
<body>

    <header>
        <h1>starootd</h1>
        <div class="search-container">
            <input type="text" placeholder="태그나 내용으로 검색해보세요...">
        </div>
    </header>

    <section class="upload-section">
        <h2>오늘의 스타일 기록하기</h2>
        <input type="file">
        <input type="text" placeholder="#태그 입력 (예: #출근룩 #OOTD)">
        <input type="text" placeholder="간단한 메모를 남겨주세요">
        <button>업로드</button>
    </section>

    <div class="masonry-container">
        <div class="card">
            <img src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bW9kZWx8ZW58MHx8MHx8fDA%3D" alt="코디 사진 1">
            <div class="info">
                <span class="date">24.05.15</span>
                <div class="tags">
                    <span class="tag">#출근룩</span><span class="tag">#린넨셔츠</span>
                </div>
                <p class="memo">지쳐 보이는 날 ㅋㅋㅋ 편한 게 최고!</p>
            </div>
        </div>

        <div class="card">
            <img src="https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fG1vZGVsfGVufDB8fDB8fHww" alt="코디 사진 2">
            <div class="info">
                <span class="date">24.01.10</span>
                <div class="tags">
                    <span class="tag">#겨울코디</span><span class="tag">#코트</span>
                </div>
                <p class="memo">역시 겨울엔 롱코트가 최고. 따뜻하고 멋스러움.</p>
            </div>
        </div>

        <div class="card">
            <img src="https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8ZmFzaGlvbnxlbnwwfHwwfHx8MA%3D%3D" alt="코디 사진 3">
            <div class="info">
                <span class="date">24.04.02</span>
                <div class="tags">
                    <span class="tag">#데이트룩</span><span class="tag">#원피스</span>
                </div>
                <p class="memo">벚꽃 보러 간 날. 날씨가 너무 좋았다.</p>
            </div>
        </div>
          <div class="card">
            <img src="https://images.unsplash.com/photo-1509631179647-0177331693ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGZhc2hpb258ZW58MHx8MHx8fDA%3D" alt="코디 사진 4">
            <div class="info">
                <span class="date">24.03.15</span>
                <div class="tags">
                    <span class="tag">#캐주얼</span><span class="tag">#데님</span>
                </div>
                <p class="memo">활동성 좋은 데님 셋업. 주말 나들이에 딱!</p>
            </div>
        </div>
    </div>

</body>
</html>