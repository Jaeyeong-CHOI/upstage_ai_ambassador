# Upstage × HuggingFace Paper Summarizer (n8n)

허깅페이스 논문 URL을 넣으면, 본문을 읽고 한국어 구조화 요약을 반환하는 n8n 워크플로우입니다.

## 왜 이 구성이 유용한가

- **Upstage Solar 장점 활용**: 한국어 요약 품질 + 안정적인 JSON 구조화 출력
- **리서치 워크플로우 최적화**: `문제-방법-결과-한계-액션아이템`으로 바로 정리
- **자동화 친화적**: Webhook 입력만 맞추면 Discord/Notion/Slack 연동 쉬움

---

## 포함 파일

- `workflow.upstage-hf-paper-summarizer.json` : 기본 워크플로우 (env 우선 + 하드코드 fallback)
- `workflow.upstage-hf-paper-summarizer-advanced.json` : 2단계 요약 + 피드백 반영 + 품질점수
- `workflow.research-orchestrator-pro.json` : URL/텍스트 혼합 입력 + 포트폴리오형 리서치 오케스트레이션
- `.env.example` : 환경변수 템플릿 (실제 키 제외)
- `blog-post.md` : 제작 과정을 정리한 블로그 포스트 초안

---

## 빠른 시작

## 1) n8n에 워크플로우 Import

n8n → Workflows → Import from File에서
원하는 json 파일 선택

## 2) API 키 환경변수 설정

n8n 실행 환경에 아래 변수 추가:

```bash
UPSTAGE_API_KEY=your_upstage_api_key
```

> 절대 깃허브에 실제 키를 커밋하지 마세요.

## 3) 테스트 호출

기본 버전:

```bash
curl -X POST "https://<YOUR_N8N_HOST>/webhook/hf-paper-summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "targetLanguage": "ko",
    "urls": [
      "https://huggingface.co/papers/2403.12345"
    ]
  }'
```

고급 버전(피드백 반영):

```bash
curl -X POST "https://<YOUR_N8N_HOST>/webhook/hf-paper-summarize-advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "targetLanguage": "ko",
    "focus": "method,ablation,limitations",
    "feedback": "수치와 실험 조건을 더 강조하고, 재현 난이도를 평가해줘",
    "urls": [
      "https://huggingface.co/papers/2403.12345",
      "https://huggingface.co/papers/2402.01234"
    ]
  }'
```

자유형 오케스트레이터(텍스트+URL 혼합):

```bash
curl -X POST "https://<YOUR_N8N_HOST>/webhook/research-orchestrator-pro" \
  -H "Content-Type: application/json" \
  -d '{
    "targetLanguage": "ko",
    "goal": "다음 주 실험 우선순위 정리",
    "feedback": "리스크/기회와 실험 아이디어를 강하게",
    "items": [
      "https://huggingface.co/papers/2403.12345",
      "https://huggingface.co/papers/2402.01234",
      "우리 팀은 현재 24GB GPU 환경에서만 재현 가능"
    ]
  }'
```

## 4) 응답 예시

```json
{
  "ok": true,
  "count": 1,
  "summaries": [
    {
      "source_url": "https://huggingface.co/papers/2403.12345",
      "title": "...",
      "one_line": "...",
      "problem": "...",
      "method": "...",
      "results": "...",
      "limitations": "...",
      "tags": ["LLM", "RAG"],
      "action_items": ["재현 실험", "우리 데이터셋 적용"]
    }
  ]
}
```

---

## 보안 체크리스트

- [ ] `.env` 파일은 `.gitignore`에 포함
- [ ] 코드/블로그/스크린샷에 API 키 마스킹
- [ ] 유출 의심 시 즉시 키 폐기 후 재발급

---

## GitHub 업로드 예시

```bash
cd n8n-upstage-hf-paper-summarizer
git init
git add .
git commit -m "feat: add upstage huggingface paper summarizer n8n workflow"
git branch -M main
git remote add origin https://github.com/<your-id>/n8n-upstage-hf-paper-summarizer.git
git push -u origin main
```
