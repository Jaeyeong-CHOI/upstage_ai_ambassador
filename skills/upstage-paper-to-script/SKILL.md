---
name: upstage-paper-to-script
description: >
  Paper → Korean presentation script generator. Input paper text, output
  structured Korean presentation script with per-section timing notes.
version: 1.0.0
tags: [upstage, solar, korean, presentation, paper, script]
author: Jaeyeong CHOI
---

# upstage-paper-to-script

논문 텍스트를 입력하면 한국어 발표 스크립트를 자동 생성합니다.
섹션별 시간 배분, 발표 스타일(격식/세미나/랩미팅)에 맞는 스크립트를 제공합니다.

## Usage

```bash
# 파일에서 논문 텍스트 입력
python3 scripts/run_paper_to_script.py \
  --text-file paper.txt \
  --duration 15 \
  --style seminar

# stdin으로 입력
cat paper.txt | python3 scripts/run_paper_to_script.py \
  --duration 10 \
  --style lab-meeting

# 격식 발표 (학회 등)
python3 scripts/run_paper_to_script.py \
  --text-file paper.txt \
  --duration 20 \
  --style formal
```

## Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--text-file` | △ | stdin | 논문 텍스트 파일 경로 |
| `--duration` | — | `15` | 발표 시간 (분) |
| `--style` | — | `seminar` | `formal` \| `seminar` \| `lab-meeting` |
| `--model` | — | `solar-pro-3` | Upstage 모델 |
| `--api-key` | — | env `UPSTAGE_API_KEY` | API 키 |
| `--output-dir` | — | `.` | 출력 디렉토리 |

## Output

- `paper_script.script.json` — 구조화된 JSON (sections, timing, transitions)
- `paper_script.script.md` — 마크다운 스크립트 (타이밍 마커 포함)

## Notes

- 논문 전체 텍스트가 너무 길면 abstract + introduction + method + results 위주로 발췌 권장
- 프롬프트 가이드: `references/prompt-guide.md`
