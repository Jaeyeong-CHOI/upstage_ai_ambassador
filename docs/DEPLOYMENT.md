# DEPLOYMENT (Production)

## 1) Import 정책
- 한 번에 1개 워크플로우만 import
- workflow 이름과 webhook path가 충돌하지 않는지 확인

## 2) 키 주입
- 권장: `UPSTAGE_API_KEY` 환경변수 사용
- fallback 하드코드는 테스트 용도로만 사용

## 3) 운영 체크
- 활성화 전 Test URL로 검증
- 활성화 후 Production URL로 smoke test
- 실패 시 n8n execution 로그에서 fetch/LLM 단계 분리 확인

## 4) 롤백
- 이전 커밋의 workflow json으로 재-import
- webhook path 유지 시 다운타임 최소화

## 5) 권장 보안
- 저장소는 private 유지 권장
- 키 유출 의심 시 revoke & rotate
- 블로그/문서에는 키 절대 노출 금지
