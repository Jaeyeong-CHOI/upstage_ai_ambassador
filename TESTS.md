# Workflow Test Checklist (3개 독립 동작 검증)

아래는 각 워크플로우를 **단독 import** 했을 때의 검증 절차입니다.

## 0) 공통 사전점검

- 각 JSON 파일이 n8n에 개별 Import 되는지 확인
- Webhook path 충돌이 없는지 확인
- Authorization header가 fallback 형태인지 확인

자동 검증 스크립트:

```bash
cd n8n-upstage-hf-paper-summarizer
npm run check
```

(내부적으로 `scripts/validate-workflows.js` + `scripts/test-fixtures.js` 실행)

성공 기준: `All workflow validations passed` + `Fixture validation passed`

---

## 1) Basic: `workflow.upstage-hf-paper-summarizer.json`

Webhook: `/webhook/hf-paper-summarize`

```bash
curl -X POST "https://<N8N_HOST>/webhook/hf-paper-summarize" \
  -H "Content-Type: application/json" \
  -d '{"targetLanguage":"ko","urls":["https://huggingface.co/papers/2403.12345"]}'
```

기대 결과:
- `ok=true`
- `count>=1`
- `summaries[0].title/problem/method/results/limitations` 존재

---

## 2) Advanced: `workflow.upstage-hf-paper-summarizer-advanced.json`

Webhook: `/webhook/hf-paper-summarize-advanced`

```bash
curl -X POST "https://<N8N_HOST>/webhook/hf-paper-summarize-advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "targetLanguage":"ko",
    "focus":"method,ablation,limitations",
    "feedback":"수치와 실험 조건을 더 강조",
    "urls":["https://huggingface.co/papers/2403.12345"]
  }'
```

기대 결과:
- `ok=true`
- `average_quality_score` 존재
- 각 item에 `final_summary`, `quality_score`, `improvement_notes`, `next_actions` 존재

---

## 3) Pro Orchestrator: `workflow.research-orchestrator-pro.json`

Webhook: `/webhook/research-orchestrator-pro`

```bash
curl -X POST "https://<N8N_HOST>/webhook/research-orchestrator-pro" \
  -H "Content-Type: application/json" \
  -d '{
    "targetLanguage":"ko",
    "goal":"다음 주 실험 우선순위",
    "feedback":"리스크/기회 중심으로",
    "items":[
      "https://huggingface.co/papers/2403.12345",
      "우리 팀은 24GB GPU에서만 재현 가능"
    ]
  }'
```

기대 결과:
- `ok=true`
- `items` 배열과 `portfolio` 객체 존재
- `portfolio.top_opportunities/top_risks/next_experiments` 존재

---

## 문제 발생 시 체크

1. n8n가 최신 버전인지 (노드 typeVersion 호환)
2. Webhook URL이 test/production 혼동 없는지
3. Upstage 키 권한/쿼터 문제 없는지
4. URL 원문 fetch 실패 시(원본 사이트 차단) 텍스트 입력 모드로 우회
