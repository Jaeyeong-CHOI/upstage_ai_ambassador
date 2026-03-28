# Upstage AI Ambassador 2026

Upstage AI Ambassador 활동 기록 및 미션 산출물을 관리하는 레포입니다.

---

## 📋 미션 개요

| # | 미션 | 마감 | 상태 |
|---|------|------|------|
| 1 | No Code 기반 자동화 워크플로우 | 2026-03-31 | ✅ 구현 완료 |
| 2 | Upstage API 활용 Skill 개발 | 2026-04-19 | ⬜ 미착수 |
| 3 | Upstage 제품 SNS 공유 | 2026-05-03 | ⬜ 미착수 |
| 4 | Upstage API 활용 프로젝트 개발 | 2026-05-22 | ⬜ 미착수 |

상세 계획: [`missions/`](./missions/) 참조

---

## 🚀 미션 1: HuggingFace Paper Summarizer (n8n)

허깅페이스 논문 URL을 넣으면, Upstage Solar로 한국어 구조화 요약을 반환하는 n8n 워크플로우.

### 왜 이 구성이 유용한가

- **Upstage Solar 장점 활용**: 한국어 요약 품질 + 안정적인 JSON 구조화 출력
- **리서치 워크플로우 최적화**: `문제-방법-결과-한계-액션아이템`으로 바로 정리
- **자동화 친화적**: Manual Trigger로 즉시 실행 가능, API형 확장 용이

### 워크플로우 파일

| 파일 | 설명 |
|------|------|
| `workflow.upstage-hf-paper-summarizer.json` | 기본 1단계 요약 |
| `workflow.upstage-hf-paper-summarizer-advanced.json` | 2단계 요약 + 피드백 반영 + 품질점수 |
| `workflow.research-orchestrator-pro.json` | URL/텍스트 혼합 입력 리서치 오케스트레이션 |

### 빠른 시작

1. **Import**: n8n → Workflows → Import from File
2. **API 키 설정**: `UPSTAGE_API_KEY` 환경변수 추가
3. **실행**: Execute Workflow → 결과 확인

> ⚠️ 절대 깃허브에 실제 키를 커밋하지 마세요.

### 응답 예시

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

### 안정성 개선

- HTTP 노드에 `onError: continueRegularOutput` 적용
- Parse 노드에서 에러 객체 구조화 반환 (`status`, `error_message`, `retry_after`)
- 최종 집계에서 `success/failed` 카운트 제공
- 긴 Expression을 Code 노드로 분리해 n8n 파서 오류 방지

---

## 🗂 레포 구조

```
├── workflow.*.json          # n8n 워크플로우 (미션1)
├── missions/                # 미션 계획/진행/템플릿
│   ├── MISSION_BREAKDOWN.md
│   ├── ROADMAP.md
│   ├── STATUS.md
│   └── templates/
├── docs/                    # GitHub Pages 웹앱 + 운영 문서
├── site/                    # Pages 소스
├── scripts/                 # 검증 스크립트
├── tests/                   # 테스트 fixture
├── blog-post.md             # 블로그 포스트 초안
├── TESTS.md                 # 테스트 체크리스트
└── .github/workflows/       # CI
```

---

## 🔒 보안 체크리스트

- [x] `.env` 파일은 `.gitignore`에 포함
- [x] 코드/블로그/스크린샷에 API 키 마스킹
- [ ] 유출 의심 시 즉시 키 폐기 후 재발급

---

## 라이선스

MIT
