# QQQ 과제 실행 가이드

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python download_data.py
python analysis.py
```

## 체크 순서
1. data/qqq_daily.csv가 100행 이상인지 확인
2. images에 PNG 4개가 생성됐는지 확인
3. REPORT.md에 실제 기간과 수치가 채워졌는지 확인
4. GitHub에 폴더 내부 전체 업로드
5. GitHub의 REPORT.md에서 이미지 4개 확인
