# Workflow Test Checklist (3개 독립 동작 검증)

아래는 각 워크플로우를 **단독 import + Manual Trigger 실행** 했을 때 검증 절차입니다.

## 0) 공통 사전점검

- 각 JSON 파일이 n8n에 개별 Import 되는지 확인
- Manual Trigger가 시작 노드인지 확인
- Authorization header가 fallback 형태인지 확인

자동 검증:

```bash
cd n8n-upstage-hf-paper-summarizer
npm run check
```

성공 기준: `All workflow validations passed` + `Fixture validation passed`

---

## 1) Basic

파일: `workflow.upstage-hf-paper-summarizer.json`

- `Prepare Input` 노드의 `urls` 확인
- Execute Workflow
- `Collect Summaries` 노드 결과 확인

기대 결과:
- `ok=true`
- `count>=1`
- `summaries[0].title/problem/method/results/limitations` 존재

---

## 2) Advanced

파일: `workflow.upstage-hf-paper-summarizer-advanced.json`

- `Set Input` 노드에서 `focus`,`feedback`,`urls` 확인
- Execute Workflow
- `Collect` 노드 결과 확인

기대 결과:
- `ok=true`
- `average_quality_score` 존재
- 각 item에 `final_summary`, `quality_score`, `improvement_notes`, `next_actions` 존재

---

## 3) Pro Orchestrator

파일: `workflow.research-orchestrator-pro.json`

- `Set Input` 노드에서 `items`(URL+텍스트 혼합) 확인
- Execute Workflow
- `Portfolio Synthesizer` 노드 결과 확인

기대 결과:
- `ok=true`
- `items` 배열과 `portfolio` 객체 존재
- `portfolio.top_opportunities/top_risks/next_experiments` 존재
