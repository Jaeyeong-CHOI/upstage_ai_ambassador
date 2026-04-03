---
name: upstage-academic-mail
description: >
  Korean academic email writer powered by Upstage Solar. Input bullet points
  of what to say + recipient context (교수님/동료/외부). Output polished Korean
  academic email with formal/casual variants.
version: 1.0.0
tags: [upstage, solar, korean, email, academic]
author: Jaeyeong CHOI
---

# upstage-academic-mail

한국어 학술 이메일 작성 스킬. 핵심 내용을 bullet point로 입력하면,
수신자 유형(교수님/동료/외부)과 톤(격식/캐주얼)에 맞는 완성된 이메일을 생성합니다.

Upstage Solar의 한국어 유창성을 활용하여 자연스럽고 예의 바른 학술 이메일을 작성합니다.

## Usage

```bash
# 교수님께 격식체 이메일
python3 scripts/run_academic_mail.py \
  --bullets "UGRP 중간보고 일정 확인 요청, 다음 주 수요일 가능 여부, 발표자료 사전 검토 부탁" \
  --recipient-type professor \
  --tone formal

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
| `--model` | — | `solar-pro-3` | Upstage 모델 |
| `--api-key` | — | env `UPSTAGE_API_KEY` | API 키 |
| `--output-dir` | — | `.` | 출력 디렉토리 |

## Output

- `academic_mail.mail.json` — 구조화된 JSON (subject, greeting, body, closing, full_text)
- `academic_mail.mail.txt` — 바로 붙여넣기 가능한 텍스트

## Notes

- Upstage API 키 필요: [console.upstage.ai](https://console.upstage.ai)
- 프롬프트 가이드: `references/prompt-guide.md`
