---
name: upstage-academic-mail
description: >
  Korean academic email writer powered by Upstage Solar. Input bullet points
  of what to say + recipient context (교수님/동료/외부). Output polished Korean
  academic email with formal/casual variants. Supports reply-to mode, context
  weaving, and CC notes.
version: 1.1.0
tags: [upstage, solar, korean, email, academic, reply]
author: Jaeyeong CHOI
---

# upstage-academic-mail

한국어 학술 이메일 작성 스킬. 핵심 내용을 bullet point로 입력하면,
수신자 유형(교수님/동료/외부)과 톤(격식/캐주얼)에 맞는 완성된 이메일을 생성합니다.

Upstage Solar의 한국어 유창성을 활용하여 자연스럽고 예의 바른 학술 이메일을 작성합니다.

### 주요 특징
- **답장 모드** (`--reply-to`): 이전 이메일 파일을 참조하여 맥락에 맞는 답장 작성
- **맥락 주입** (`--context`): 만남 경위, 배경 정보를 이메일에 자연스럽게 반영
- **CC 안내** (`--cc-note`): CC 수신자에 대한 안내 문구 자동 포함
- **구체적 제목 생성**: "문의드립니다" 같은 generic 제목 대신 핵심 키워드 포함 제목
- **상황별 톤 조절**: 첫 연락/후속/리마인더 상황을 자동 감지하여 공손함 수준 조절

## Usage

```bash
# 교수님께 격식체 이메일
python3 scripts/run_academic_mail.py \
  --bullets "졸업논문 피드백 미팅 요청, 다음 주 가능 여부 확인, 발표자료 사전 검토 부탁" \
  --recipient-type professor \
  --tone formal

# 이전 이메일에 대한 답장
python3 scripts/run_academic_mail.py \
  --bullets "미팅 일정 확인, 목요일 오후 2시 가능, 발표자료 사전 첨부" \
  --recipient-type professor \
  --tone formal \
  --reply-to previous_email.txt

# 맥락 추가 (학회에서 만난 외부 연구자에게)
python3 scripts/run_academic_mail.py \
  --bullets "공동연구 제안, 데이터셋 공유 요청, 다음 달 방문 가능 여부" \
  --recipient-type external \
  --tone formal \
  --context "EMNLP 2025에서 만남, Poster Session에서 유사 연구 주제 논의"

# CC 안내 문구 포함
python3 scripts/run_academic_mail.py \
  --bullets "프로젝트 중간 보고, 다음 단계 계획 공유" \
  --recipient-type professor \
  --tone formal \
  --cc-note "공동지도교수님께도 진행 상황 공유 드립니다"

# 동료에게 캐주얼 이메일
python3 scripts/run_academic_mail.py \
  --bullets "논문 리뷰 피드백 감사, 2장 수정 완료, 내일 미팅에서 논의" \
  --recipient-type colleague \
  --tone casual

# 외부 연구자에게 영문 이메일
python3 scripts/run_academic_mail.py \
  --bullets "collaboration proposal, shared interest in NLP, request for meeting" \
  --recipient-type external \
  --tone formal \
  --lang en
```

## Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--bullets` | ✅ | — | 이메일 핵심 내용 (쉼표 또는 줄바꿈 구분) |
| `--recipient-type` | ✅ | — | `professor` \| `colleague` \| `external` |
| `--tone` | — | `formal` | `formal` \| `casual` |
| `--lang` | — | `ko` | 출력 언어 (`ko` \| `en`) |
| `--reply-to` | — | — | 답장할 이전 이메일 텍스트 파일 경로 |
| `--context` | — | — | 추가 맥락 (예: "EMNLP에서 만남", "3월 미팅 후속") |
| `--cc-note` | — | — | CC 수신자에 대한 안내 문구 |
| `--model` | — | `solar-pro-3` | Upstage 모델 |
| `--api-key` | — | env `UPSTAGE_API_KEY` | API 키 |
| `--output-dir` | — | `.` | 출력 디렉토리 |

## Output

- `academic_mail.mail.json` — 구조화된 JSON (subject, greeting, body, closing, full_text)
- `academic_mail.mail.txt` — 바로 붙여넣기 가능한 텍스트

## Notes

- Upstage API 키 필요: [console.upstage.ai](https://console.upstage.ai)
- 프롬프트 가이드: `references/prompt-guide.md`
