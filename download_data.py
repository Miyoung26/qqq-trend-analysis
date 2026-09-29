from pathlib import Path
import yfinance as yf
out=Path(__file__).parent/'data'/'qqq_daily.csv'
df=yf.download('QQQ',start='2024-01-01',end='2026-01-01',auto_adjust=False,progress=False)
if df.empty: raise RuntimeError('다운로드 실패: 인터넷 연결을 확인하세요.')
if getattr(df.columns,'nlevels',1)>1: df.columns=df.columns.get_level_values(0)
df.reset_index().to_csv(out,index=False)
print(f'저장: {out}, {len(df)}개')
