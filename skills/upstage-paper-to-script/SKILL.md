---
name: upstage-paper-to-script
description: >
  Paper → Korean presentation script generator. Input paper text, output
  structured Korean presentation script with per-section timing notes.
  2-stage summarization for long papers, audience-aware adaptation, key figure emphasis.
version: 1.1.0
tags: [upstage, solar, korean, presentation, paper, script]
author: Jaeyeong CHOI
---

# upstage-paper-to-script

논문 텍스트를 입력하면 한국어 발표 스크립트를 자동 생성합니다.
섹션별 시간 배분, 발표 스타일(격식/세미나/랩미팅)에 맞는 스크립트를 제공합니다.

### 주요 특징
- **2단계 처리**: 10,000자 초과 논문은 먼저 구조적 요약 후 스크립트 생성 (정보 손실 최소화)
- **청중 맞춤** (`--audience-context`): 청중 특성에 맞게 설명 수준과 용어 난이도 자동 조절
- **핵심 Figure 강조** (`--key-figures`): 특정 Figure/Table을 스크립트에서 중점적으로 다룸
- **확장된 출력**: `max_tokens` 8192로 더 상세한 스크립트 생성

## Usage

```bash
# 파일에서 논문 텍스트 입력
python3 scripts/run_paper_to_script.py \
  --text-file paper.txt \
  --duration 15 \
  --style seminar

# 비전공자 포함 청중 대상
python3 scripts/run_paper_to_script.py \
  --text-file paper.txt \
  --duration 20 \
  --style seminar \
  --audience-context "비전공자 포함, 학부 3-4학년 수준"

# 특정 Figure/Table 강조
python3 scripts/run_paper_to_script.py \
  --text-file paper.txt \
  --duration 15 \
  --style formal \
  --key-figures "Figure 2,Table 1,Figure 5"

# stdin으로 입력
cat paper.txt | python3 scripts/run_paper_to_script.py \
  --duration 10 \
  --style lab-meeting

# 격식 발표 (학회) + 청중 맞춤
python3 scripts/run_paper_to_script.py \
  --text-file paper.txt \
  --duration 20 \
  --style formal \
  --audience-context "NLP 전문가, ACL 참석자"
```

## Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--text-file` | △ | stdin | 논문 텍스트 파일 경로 |
| `--duration` | — | `15` | 발표 시간 (분) |
| `--style` | — | `seminar` | `formal` \| `seminar` \| `lab-meeting` |
| `--audience-context` | — | — | 청중 특성 설명 (예: "비전공자 포함", "NLP 전문가") |
| `--key-figures` | — | — | 강조할 Figure/Table 번호 (쉼표 구분) |
| `--model` | — | `solar-pro-3` | Upstage 모델 |
| `--api-key` | — | env `UPSTAGE_API_KEY` | API 키 |
| `--output-dir` | — | `.` | 출력 디렉토리 |

## Output

- `paper_script.script.json` — 구조화된 JSON (sections, timing, transitions)
- `paper_script.script.md` — 마크다운 스크립트 (타이밍 마커 포함)

## 2-Stage Processing

논문 텍스트가 10,000자를 초과하면 자동으로 2단계로 처리됩니다:

1. **Stage 1 — 구조적 요약**: Solar가 논문을 문제/방법/결과/핵심 Figure/한계 구조로 ~3000자 요약
2. **Stage 2 — 스크립트 생성**: 요약을 바탕으로 발표 스크립트 생성

10,000자 이하면 원문을 직접 사용합니다.

## Notes

- 프롬프트 가이드: `references/prompt-guide.md`
