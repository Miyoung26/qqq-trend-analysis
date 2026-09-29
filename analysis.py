from pathlib import Path
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
B=Path(__file__).parent; D=B/'data'/'qqq_daily.csv'; O=B/'images'; O.mkdir(exist_ok=True)
df=pd.read_csv(D); df.columns=[c.lower().replace(' ','_') for c in df.columns]
df['date']=pd.to_datetime(df['date'],errors='coerce')
for c in ['open','high','low','close','adj_close','volume']:
    if c in df: df[c]=pd.to_numeric(df[c],errors='coerce')
df=df.dropna(subset=['date','close']).drop_duplicates('date').sort_values('date').reset_index(drop=True)
assert len(df)>=100, f'100개 이상 필요, 현재 {len(df)}개'
df['ma20']=df.close.rolling(20).mean(); df['ma60']=df.close.rolling(60).mean(); df['ret']=df.close.pct_change(); df['vol20']=df.ret.rolling(20).std()*np.sqrt(252)*100; df['dd']=(df.close/df.close.cummax()-1)*100
monthly=df.set_index('date').close.resample('ME').last().pct_change()*100
fig,ax=plt.subplots(figsize=(12,5)); ax.plot(df.date,df.close,label='QQQ Close'); ax.plot(df.date,df.ma20,label='20-day MA'); ax.plot(df.date,df.ma60,label='60-day MA'); ax.set(title='QQQ Price and Moving Averages',xlabel='Date',ylabel='USD'); ax.legend(); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(O/'01_price_ma.png',dpi=170); plt.close(fig)
fig,ax=plt.subplots(figsize=(12,5)); ax.plot(df.date,df.vol20,color='purple'); ax.set(title='QQQ 20-Day Annualized Volatility',xlabel='Date',ylabel='%'); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(O/'02_volatility.png',dpi=170); plt.close(fig)
fig,ax=plt.subplots(figsize=(12,5)); ax.fill_between(df.date,df.dd,0,color='tomato'); ax.set(title='QQQ Drawdown',xlabel='Date',ylabel='%'); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(O/'03_drawdown.png',dpi=170); plt.close(fig)
fig,ax=plt.subplots(figsize=(12,5)); ax.bar(monthly.index,monthly.values,color=np.where(monthly>=0,'teal','tomato')); ax.set(title='QQQ Monthly Returns',xlabel='Month',ylabel='%'); ax.tick_params(axis='x',rotation=90,labelsize=7); fig.tight_layout(); fig.savefig(O/'04_monthly_returns.png',dpi=170); plt.close(fig)
s,e=df.iloc[0],df.iloc[-1]; best=df.loc[df.ret.idxmax()]; worst=df.loc[df.ret.idxmin()]; mdd=df.loc[df.dd.idxmin()]; total=(e.close/s.close-1)*100
report=f'''# QQQ 가격 트렌드 분석 리포트

> 학습 목적이며 투자 권유가 아닙니다.

## 1. 분석 주제 및 선정 이유
QQQ의 일별 가격으로 추세, 변동성, 하락 위험을 분석한다.

## 2. 분석 질문
1. 기간 전체 가격 흐름은 어떠한가?
2. 20일과 60일 이동평균은 어떤 추세를 보이는가?
3. 변동성과 최대 낙폭이 큰 시점은 언제인가?
4. 월간 수익률의 상승과 하락 패턴은 어떠한가?

## 3. 데이터 설명
- 기간: {s.date.date()} ~ {e.date.date()}
- 데이터 포인트: {len(df)}개
- 출처/수집: Yahoo Finance 시세를 yfinance로 수집
- 컬럼: Date, Open, High, Low, Close, Adj Close, Volume

## 4. 데이터 정제
날짜 정렬, 숫자형 변환, 날짜와 종가 결측 행 삭제, 중복 날짜 제거를 수행했다. 급등락은 실제 시장 움직임일 수 있어 임의로 삭제하지 않았다.

## 5. 분석 방법
20일 및 60일 이동평균, 일간 수익률, 20일 연율화 변동성, 누적 최고가 대비 낙폭, 월간 수익률을 적용했다.

## 6. 시각화
![가격 이동평균](images/01_price_ma.png)
![변동성](images/02_volatility.png)
![낙폭](images/03_drawdown.png)
![월간 수익률](images/04_monthly_returns.png)

## 7. 인사이트
### 인사이트 1
- 관찰: 시작 종가 ${s.close:.2f}, 종료 종가 ${e.close:.2f}, 단순 변화율 {total:.2f}%
- 해석: 전체 방향은 보이지만 중간 위험과 배당을 모두 설명하지 못한다.
- 행동: 이동평균, 변동성, 낙폭을 함께 본다.

### 인사이트 2
- 관찰: 최대 일간 상승은 {best.date.date()} {best.ret*100:.2f}%, 최대 하락은 {worst.date.date()} {worst.ret*100:.2f}%
- 해석: 일부 극단적 거래일이 위험에 큰 영향을 줄 수 있다.
- 행동: 해당 날짜 원인은 별도 신뢰 가능한 뉴스 출처로 검증한다.

### 인사이트 3
- 관찰: 최대 낙폭은 {mdd.date.date()} {mdd.dd:.2f}%
- 해석: 전체 수익률이 양수여도 보유 중 큰 하락을 경험할 수 있다.
- 행동: 기간을 바꿔 결론의 민감도를 확인한다.

## 8. 결론 및 한계
추세와 위험 지표를 함께 봐야 QQQ의 움직임을 균형 있게 설명할 수 있다. 단일 ETF만 분석했고 환율, 금리, 구성 종목 실적 등 외부 변수를 반영하지 않았다. 과거 데이터는 미래 성과를 보장하지 않는다.

## 9. AI 사용 로그
- 사용 작업: 코드 초안, 시각화 구성, 문장 구조화
- 사용 이유: 반복 작업 절감과 대안 탐색
- 검증 방법: 데이터 개수, 기간, 결측치, 계산 재실행, 이미지 4개 확인
'''
(B/'REPORT.md').write_text(report,encoding='utf-8'); print(f'완료: {len(df)}개')
