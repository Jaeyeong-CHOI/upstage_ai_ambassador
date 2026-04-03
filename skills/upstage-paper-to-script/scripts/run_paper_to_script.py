#!/usr/bin/env python3
"""Paper → Korean presentation script generator powered by Upstage Solar.

Usage:
    python3 run_paper_to_script.py --text-file paper.txt --duration 15 --style seminar
    cat paper.txt | python3 run_paper_to_script.py --duration 10 --style lab-meeting
"""

import argparse
import json
import os
import sys
from datetime import datetime

import requests

API_URL = "https://api.upstage.ai/v1/chat/completions"
DEFAULT_MODEL = "solar-pro-3"

STYLE_DESCRIPTIONS = {
    "formal": "학회/컨퍼런스 발표 (격식체, 청중: 전문 연구자)",
    "seminar": "연구실 세미나 (반격식, 청중: 같은 분야 연구자)",
    "lab-meeting": "랩미팅 (캐주얼, 청중: 연구실 동료)",
}

SYSTEM_PROMPT = """\
당신은 학술 논문을 한국어 발표 스크립트로 변환하는 전문가입니다.

목표: 주어진 논문 텍스트를 읽고, 발표 시간과 스타일에 맞는 한국어 발표 스크립트를 작성합니다.

규칙:
1. 발표 구조: 도입(배경/동기) → 관련 연구 → 방법론 → 실험/결과 → 결론/향후 연구 → Q&A 안내
2. 각 섹션에 예상 소요 시간(분)을 배분합니다. 총합이 지정된 발표 시간과 일치해야 합니다.
3. 각 섹션의 발표 스크립트는 실제로 말할 수 있는 자연스러운 한국어여야 합니다.
4. 슬라이드 전환 cue를 포함합니다 (예: "[다음 슬라이드]").
5. 핵심 수치/결과는 반드시 포함합니다.
6. 발표 스타일에 따라 어투를 조절합니다:
   - formal: "-습니다" 체, 전문 용어 유지
   - seminar: "-요/-습니다" 혼용, 부연 설명 추가
   - lab-meeting: 편한 어투, 디스커션 유도 표현 포함
7. 각 섹션에 transition_note(다음 섹션으로 넘어가는 멘트)를 포함합니다.
"""

JSON_SCHEMA = {
    "name": "presentation_script",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "발표 제목",
            },
            "total_duration_min": {
                "type": "number",
                "description": "총 발표 시간(분)",
            },
            "style": {
                "type": "string",
                "description": "발표 스타일",
            },
            "sections": {
                "type": "array",
                "description": "발표 섹션 목록",
                "items": {
                    "type": "object",
                    "properties": {
                        "section_title": {
                            "type": "string",
                            "description": "섹션 제목",
                        },
                        "duration_min": {
                            "type": "number",
                            "description": "이 섹션 예상 소요 시간(분)",
                        },
                        "script": {
                            "type": "string",
                            "description": "실제 발표 스크립트 텍스트",
                        },
                        "slide_cues": {
                            "type": "string",
                            "description": "슬라이드 전환/강조 cue",
                        },
                        "transition_note": {
                            "type": "string",
                            "description": "다음 섹션으로 넘어가는 멘트",
                        },
                    },
                    "required": [
                        "section_title",
                        "duration_min",
                        "script",
                        "slide_cues",
                        "transition_note",
                    ],
                    "additionalProperties": False,
                },
            },
            "closing_remarks": {
                "type": "string",
                "description": "마무리 멘트 (감사 인사, Q&A 안내)",
            },
            "key_points_summary": {
                "type": "string",
                "description": "핵심 포인트 요약 (발표자 참고용)",
            },
        },
        "required": [
            "title",
            "total_duration_min",
            "style",
            "sections",
            "closing_remarks",
            "key_points_summary",
        ],
        "additionalProperties": False,
    },
}


def read_paper_text(args) -> str:
    if args.text_file:
        if not os.path.isfile(args.text_file):
            print(f"[ERROR] File not found: {args.text_file}", file=sys.stderr)
            sys.exit(1)
        with open(args.text_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    elif not sys.stdin.isatty():
        return sys.stdin.read().strip()
    else:
        print("[ERROR] Provide paper text via --text-file or stdin.", file=sys.stderr)
        sys.exit(1)


def build_messages(paper_text: str, duration: int, style: str) -> list:
    style_desc = STYLE_DESCRIPTIONS.get(style, style)
    user_msg = f"""발표 시간: {duration}분
발표 스타일: {style} ({style_desc})

아래 논문 텍스트를 기반으로 발표 스크립트를 작성해주세요.

---
{paper_text[:12000]}
---"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]


def call_api(api_key: str, model: str, messages: list) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "response_format": {
            "type": "json_schema",
            "json_schema": JSON_SCHEMA,
        },
        "temperature": 0.7,
        "max_tokens": 4096,
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)

    if resp.status_code != 200:
        detail = resp.text[:500]
        print(f"[ERROR] API returned {resp.status_code}: {detail}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def result_to_markdown(result: dict) -> str:
    lines = [
        f"# {result['title']}",
        "",
        f"**발표 시간:** {result['total_duration_min']}분 | **스타일:** {result['style']}",
        "",
        "---",
        "",
    ]
    for i, sec in enumerate(result["sections"], 1):
        lines.append(f"## {i}. {sec['section_title']}  ⏱ {sec['duration_min']}분")
        lines.append("")
        if sec.get("slide_cues"):
            lines.append(f"🖥 _{sec['slide_cues']}_")
            lines.append("")
        lines.append(sec["script"])
        lines.append("")
        if sec.get("transition_note"):
            lines.append(f"> 💬 전환: {sec['transition_note']}")
            lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## 마무리")
    lines.append("")
    lines.append(result["closing_remarks"])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### 📌 핵심 포인트 (발표자 참고)")
    lines.append("")
    lines.append(result["key_points_summary"])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Paper → Korean presentation script (Upstage Solar)")
    parser.add_argument("--text-file", default=None, help="Path to paper text file")
    parser.add_argument("--duration", type=int, default=15, help="Presentation duration in minutes")
    parser.add_argument(
        "--style",
        default="seminar",
        choices=["formal", "seminar", "lab-meeting"],
        help="Presentation style",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Upstage model name")
    parser.add_argument("--api-key", default=None, help="Upstage API key (or UPSTAGE_API_KEY env)")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("UPSTAGE_API_KEY")
    if not api_key:
        print("[ERROR] API key required. Use --api-key or set UPSTAGE_API_KEY env var.", file=sys.stderr)
        sys.exit(1)

    paper_text = read_paper_text(args)
    if not paper_text:
        print("[ERROR] Paper text is empty.", file=sys.stderr)
        sys.exit(1)

    messages = build_messages(paper_text, args.duration, args.style)
    print(f"[INFO] Calling {args.model} for {args.duration}min {args.style} script...", file=sys.stderr)
    result = call_api(api_key, args.model, messages)

    os.makedirs(args.output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(args.output_dir, f"paper_script_{ts}.script.json")
    md_path = os.path.join(args.output_dir, f"paper_script_{ts}.script.md")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    md_content = result_to_markdown(result)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[OK] JSON: {json_path}", file=sys.stderr)
    print(f"[OK] Markdown: {md_path}", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
