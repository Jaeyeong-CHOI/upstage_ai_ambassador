---
name: upstage-script-polisher
description: >
  Polish presentation scripts to sound natural in spoken Korean. Removes
  written-style stiffness, adds natural speech patterns, and provides
  pronunciation hints.
version: 1.0.0
tags: [upstage, solar, korean, presentation, speech, polish]
author: Jaeyeong CHOI
---

# upstage-script-polisher

발표 스크립트를 자연스러운 구어체 한국어로 다듬는 스킬.
문어체 딱딱함 제거, 발음 힌트, 불필요한 군말 정리, 강조 표현 추가.

## Usage

```bash
# 학술 발표 스타일로 폴리싱
python3 scripts/run_script_polisher.py \
  --input draft_script.md \
  --style academic

# TED Talk 스타일
python3 scripts/run_script_polisher.py \
  --input draft_script.md \
  --style ted-talk

# 대화형 (세미나/랩미팅)
python3 scripts/run_script_polisher.py \
  --input draft_script.md \
  --style conversational
```

## Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | ✅ | — | 입력 스크립트 파일 경로 |
| `--style` | — | `academic` | `conversational` \| `academic` \| `ted-talk` |
| `--model` | — | `solar-pro-3` | Upstage 모델 |
| `--api-key` | — | env `UPSTAGE_API_KEY` | API 키 |
| `--output-dir` | — | `.` | 출력 디렉토리 |

## Output

- `polished_script.polished.json` — 구조화된 JSON (원문 vs 수정본 비교, 변경 사항 설명)
- `polished_script.polished.md` — 바로 사용 가능한 폴리싱된 스크립트

## Pipeline

`upstage-paper-to-script` → `upstage-script-polisher` 순서로 사용하면
논문 → 발표 스크립트 → 자연스러운 구어체 스크립트를 한 번에 만들 수 있습니다.

## Notes

- 프롬프트 가이드: `references/prompt-guide.md`
