---
name: upstage-script-polisher
description: >
  Polish presentation scripts to sound natural in spoken Korean. Removes
  written-style stiffness, adds natural speech patterns, pronunciation hints,
  and before/after comparison. Supports JSON pipeline input from paper-to-script.
version: 1.1.0
tags: [upstage, solar, korean, presentation, speech, polish, pipeline]
author: Jaeyeong CHOI
---

# upstage-script-polisher

발표 스크립트를 자연스러운 구어체 한국어로 다듬는 스킬.
문어체 딱딱함 제거, 발음 힌트, 불필요한 군말 정리, 강조 표현 추가.

### 주요 특징
- **JSON 파이프라인** (`--from-json`): paper-to-script의 JSON 출력을 직접 입력으로 받아 자동 추출·폴리싱
- **stdin 지원** (`--input -`): 파이프라인 연결 가능
- **Before/After 비교**: 마크다운 출력에 각 문단의 원문 vs 수정본 비교 포함
- **확장된 처리**: 16,000자까지 입력 지원, `max_tokens` 8192

## Usage

```bash
# 학술 발표 스타일로 폴리싱
python3 scripts/run_script_polisher.py \
  --input draft_script.md \
  --style academic

# paper-to-script JSON 출력에서 직접 폴리싱 (파이프라인)
python3 scripts/run_script_polisher.py \
  --from-json out/paper_script_*.script.json \
  --style conversational

# stdin 파이핑
cat draft_script.md | python3 scripts/run_script_polisher.py \
  --input - \
  --style ted-talk

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
| `--input` | △ | — | 입력 스크립트 파일 경로, 또는 `-`로 stdin |
| `--from-json` | △ | — | paper-to-script JSON 출력 경로 (glob 패턴 지원) |
| `--style` | — | `academic` | `conversational` \| `academic` \| `ted-talk` |
| `--model` | — | `solar-pro-3` | Upstage 모델 |
| `--api-key` | — | env `UPSTAGE_API_KEY` | API 키 |
| `--output-dir` | — | `.` | 출력 디렉토리 |

> `--input` 또는 `--from-json` 중 하나 필수. `--from-json` 사용 시 `--input` 불필요.

## Output

- `polished_script.polished.json` — 구조화된 JSON (원문 vs 수정본 비교, 변경 사항 설명)
- `polished_script.polished.md` — 바로 사용 가능한 폴리싱된 스크립트 + Before/After 비교

## Pipeline

`upstage-paper-to-script` → `upstage-script-polisher` 순서로 사용하면
논문 → 발표 스크립트 → 자연스러운 구어체 스크립트를 한 번에 만들 수 있습니다.

```bash
# 완전한 파이프라인 예시
python3 run_paper_to_script.py \
  --text-file paper.txt --duration 15 --style seminar \
  --audience-context "학부생 대상" \
  --output-dir out/

python3 run_script_polisher.py \
  --from-json "out/paper_script_*.script.json" \
  --style conversational \
  --output-dir out/
```

## Notes

- 프롬프트 가이드: `references/prompt-guide.md`
