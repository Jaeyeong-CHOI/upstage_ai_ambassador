#!/usr/bin/env python3
"""Polish presentation scripts to natural spoken Korean using Upstage Solar.

Usage:
    python3 run_script_polisher.py --input draft_script.md --style academic
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
    "conversational": "대화형 (자연스러운 구어체, 청중과 소통하는 느낌)",
    "academic": "학술 발표 (격식 있되 읽는 느낌이 아닌 말하는 느낌)",
    "ted-talk": "TED Talk (스토리텔링, 감정 전달, 청중 몰입)",
}

SYSTEM_PROMPT = """\
당신은 발표 스크립트를 자연스러운 구어체 한국어로 다듬는 전문 스피치 코치입니다.

목표: 입력된 발표 스크립트를 실제로 말했을 때 자연스럽게 들리도록 수정합니다.

수정 원칙:
1. **문어체 → 구어체**: "~것이다" → "~거예요/겁니다", "~하였다" → "~했는데요" 등
2. **불필요한 군말 제거**: "어", "음", "그래서 이제" 등 불필요한 filler 정리
3. **호흡 단위 정리**: 한 문장이 너무 길면 끊어서 자연스럽게 쉴 수 있게
4. **강조 표현 추가**: 중요한 부분에 "여기서 주목할 점은", "핵심은" 등 화법 추가
5. **발음 힌트**: 어려운 용어나 숫자에 읽는 방법 힌트 제공 (예: "BLEU(블루)")
6. **전환 자연스럽게**: 슬라이드 전환 시 "자, 다음으로" 같은 자연스러운 멘트
7. **스타일 맞춤**: conversational/academic/ted-talk에 따라 톤 조절

변경 시 반드시:
- 원래 의미를 유지하면서 표현만 변경
- 기술적 정확성 훼손 금지
- 핵심 수치/결과는 그대로 유지
"""

JSON_SCHEMA = {
    "name": "polished_script",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "polished_full_text": {
                "type": "string",
                "description": "폴리싱된 전체 스크립트 텍스트",
            },
            "changes_summary": {
                "type": "string",
                "description": "주요 변경 사항 요약",
            },
            "pronunciation_hints": {
                "type": "array",
                "description": "발음 힌트 목록",
                "items": {
                    "type": "object",
                    "properties": {
                        "term": {
                            "type": "string",
                            "description": "용어/약어",
                        },
                        "pronunciation": {
                            "type": "string",
                            "description": "발음 가이드",
                        },
                    },
                    "required": ["term", "pronunciation"],
                    "additionalProperties": False,
                },
            },
            "speech_tips": {
                "type": "array",
                "description": "발표 팁 (속도, 강조, 제스처 등)",
                "items": {
                    "type": "string",
                },
            },
            "style_applied": {
                "type": "string",
                "description": "적용된 스타일 설명",
            },
        },
        "required": [
            "polished_full_text",
            "changes_summary",
            "pronunciation_hints",
            "speech_tips",
            "style_applied",
        ],
        "additionalProperties": False,
    },
}


def build_messages(script_text: str, style: str) -> list:
    style_desc = STYLE_DESCRIPTIONS.get(style, style)
    user_msg = f"""스타일: {style} ({style_desc})

아래 발표 스크립트를 자연스러운 구어체로 다듬어주세요.

---
{script_text[:12000]}
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
        "# 📝 Polished Presentation Script",
        "",
        f"**스타일:** {result['style_applied']}",
        "",
        "---",
        "",
        "## 스크립트",
        "",
        result["polished_full_text"],
        "",
        "---",
        "",
        "## 📋 변경 사항",
        "",
        result["changes_summary"],
        "",
    ]

    if result.get("pronunciation_hints"):
        lines.append("## 🔤 발음 가이드")
        lines.append("")
        lines.append("| 용어 | 발음 |")
        lines.append("|------|------|")
        for hint in result["pronunciation_hints"]:
            lines.append(f"| {hint['term']} | {hint['pronunciation']} |")
        lines.append("")

    if result.get("speech_tips"):
        lines.append("## 💡 발표 팁")
        lines.append("")
        for tip in result["speech_tips"]:
            lines.append(f"- {tip}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Polish scripts to natural spoken Korean (Upstage Solar)")
    parser.add_argument("--input", required=True, help="Path to script text file")
    parser.add_argument(
        "--style",
        default="academic",
        choices=["conversational", "academic", "ted-talk"],
        help="Polishing style",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Upstage model name")
    parser.add_argument("--api-key", default=None, help="Upstage API key (or UPSTAGE_API_KEY env)")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("UPSTAGE_API_KEY")
    if not api_key:
        print("[ERROR] API key required. Use --api-key or set UPSTAGE_API_KEY env var.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.input):
        print(f"[ERROR] File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        script_text = f.read().strip()

    if not script_text:
        print("[ERROR] Input script is empty.", file=sys.stderr)
        sys.exit(1)

    messages = build_messages(script_text, args.style)
    print(f"[INFO] Calling {args.model} for {args.style} polishing...", file=sys.stderr)
    result = call_api(api_key, args.model, messages)

    os.makedirs(args.output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(args.output_dir, f"polished_script_{ts}.polished.json")
    md_path = os.path.join(args.output_dir, f"polished_script_{ts}.polished.md")

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
