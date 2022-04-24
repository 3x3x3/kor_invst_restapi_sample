# 한국투자증권 Restful API 샘플
- 모의투자가 아닌 주식 실계좌를 기준으로 만들어짐

## 초기화
1. config.ini.format 파일을 복사하고 파일명을 config.ini으로 수정
2. config.ini에 다음의 내용을 입력
   - Key
     - AppKey: 한국투자증권에서 발급받은 AppKey
     - AppSecret: 한국투자증권에서 발급받은 AppSecret
   - Account
     - HtsId: HTS에서 로그인시 사용하는 아이디
     - AccNo: 종합계좌번호(계좌번호의 앞 8자리)
     - AccCd: 계좌상품코드(계좌번호의 뒤 2자리)

## 파일 설명
- get_cur_prc.py: 현재가 조회
- get_balance.py: 잔고조회
- send_new_order.py: 신규주문
- get_realtime_prc.py: 실시간 체결 조회
- get_realtime_lob.py: 실시간 호가 조회
- get_realtime_filled.py: 실시간 주문 접수, 체결 응답
