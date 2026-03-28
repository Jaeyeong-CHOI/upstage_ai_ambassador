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

## 🚀 미션 1: HuggingFace Daily Paper Digest

매일 HuggingFace Daily Papers에서 인기 논문을 자동 수집하고, **Upstage Solar**로 한국어 구조화 요약을 생성해 이메일로 발송하는 n8n 워크플로우.

### 핵심 기능

- **자동 수집**: HF Daily Papers API에서 매일 인기 논문 Top 10 자동 크롤링
- **구조화 요약**: Upstage Solar로 `문제-방법-결과-한계-액션아이템` 포맷 요약
- **이메일 Digest**: HTML 포맷의 깔끔한 데일리 뉴스레터로 발송
- **웹 다운로드**: [upstage-n8n.jaeyeong2026.com](https://upstage-n8n.jaeyeong2026.com)에서 API 키만 입력하면 바로 워크플로우 JSON 다운로드

### 왜 Upstage Solar인가

1. **한국어 요약 품질** — 영어 논문을 한국어로 일관되게 구조화
2. **JSON 구조화 출력** — `response_format` 스키마로 파싱 가능한 출력 강제
3. **실무형 프롬프트 내성** — 과장 금지, 수치 보존 등 지시를 안정적으로 따름

### 워크플로우 파일

| 파일 | 설명 |
|------|------|
| `workflow.upstage-daily-paper-digest.json` | ⭐ **Daily Digest** — 매일 HF 인기 논문 요약 → 이메일 발송 |
| `workflow.upstage-hf-paper-summarizer.json` | Basic — URL 입력 → 1단계 구조화 요약 |
| `workflow.upstage-hf-paper-summarizer-advanced.json` | Advanced — 2단계 요약 + 피드백 반영 + 품질 점수 |
| `workflow.research-orchestrator-pro.json` | Pro — URL/텍스트 혼합 입력 리서치 오케스트레이션 |

### 빠른 시작

#### 방법 1: 웹에서 다운로드 (권장)

1. [**upstage-n8n.jaeyeong2026.com**](https://upstage-n8n.jaeyeong2026.com) 접속
2. 워크플로우 선택 → API 키 입력 → JSON 다운로드
3. n8n에서 Import from File → 실행

> API 키는 브라우저에서만 처리되며 서버로 전송되지 않습니다.

#### 방법 2: 직접 Import

1. 이 레포에서 원하는 `workflow.*.json` 파일 다운로드
2. n8n → Workflows → Import from File
3. `UPSTAGE_API_KEY` 환경변수 설정 (또는 JSON 내 플레이스홀더 수동 교체)
4. Daily Digest 사용 시: SMTP 크레덴셜 설정 + 수신 이메일 주소 변경

> ⚠️ 절대 깃허브에 실제 API 키를 커밋하지 마세요.

### Daily Digest 워크플로우 구조

```
Schedule Trigger (매일 08:30)
  → HF Daily Papers API (인기 논문 Top 10 수집)
  → Jina Reader (논문 본문 추출)
  → Upstage Solar (구조화 요약)
  → HTML 이메일 생성 (논문별 요약 카드)
  → SMTP 발송
```

### 응답 예시

```json
{
  "ok": true,
  "summary": {
    "title": "Attention Is All You Need",
    "one_line": "셀프 어텐션만으로 시퀀스 변환을 수행하는 Transformer 아키텍처 제안",
    "problem": "기존 RNN/CNN 기반 인코더-디코더의 병렬화 한계와 장거리 의존성 문제",
    "method": "멀티헤드 셀프 어텐션 + 포지셔널 인코딩 기반 인코더-디코더 구조",
    "results": "WMT14 EN-DE BLEU 28.4, EN-FR BLEU 41.0 (SOTA)",
    "limitations": "긴 시퀀스에서 O(n²) 메모리, 고정 컨텍스트 윈도우",
    "tags": ["Transformer", "Attention", "NMT"],
    "action_items": ["우리 데이터셋 적용", "Efficient Attention 비교"]
  }
}
```

### 안정성

- HTTP 노드에 `onError: continueRegularOutput` 적용
- Parse 노드에서 에러 객체 구조화 반환
- 최종 집계에서 `success/failed` 카운트 제공
- Daily Papers가 없을 경우 전날 데이터로 자동 폴백

---

## 🗂 레포 구조

```
├── workflow.*.json          # n8n 워크플로우 (미션1)
├── missions/                # 미션 계획/진행/템플릿
│   ├── MISSION_BREAKDOWN.md
│   ├── ROADMAP.md
│   ├── STATUS.md
│   └── templates/
├── docs/                    # GitHub Pages (upstage-n8n.jaeyeong2026.com)
├── scripts/                 # 검증 스크립트
├── tests/                   # 테스트 fixture
├── TESTS.md                 # 테스트 체크리스트
└── .github/workflows/       # CI
```

---

## 🔗 링크

- **워크플로우 다운로드**: [upstage-n8n.jaeyeong2026.com](https://upstage-n8n.jaeyeong2026.com)
- **Upstage Console**: [console.upstage.ai](https://console.upstage.ai)
- **HF Daily Papers**: [huggingface.co/papers](https://huggingface.co/papers)

---

## 🔒 보안

- `.env` 파일은 `.gitignore`에 포함
- 워크플로우 내 API 키는 플레이스홀더(`REPLACE_WITH_YOUR_REAL_KEY`)
- 웹 다운로드 페이지에서 키는 브라우저 로컬에서만 처리

---

## 라이선스

MIT
