#!/usr/bin/env python3
"""Korean academic email writer powered by Upstage Solar.

Usage:
    python3 run_academic_mail.py \
        --bullets "졸업논문 피드백 미팅 요청, 다음 주 가능 여부 확인" \
        --recipient-type professor --tone formal
"""

import argparse
import json
import os
import sys
from datetime import datetime

import requests

API_URL = "https://api.upstage.ai/v1/chat/completions"
DEFAULT_MODEL = "solar-pro-3"

RECIPIENT_LABELS = {
    "professor": "교수님 (지도교수/학과 교수 등 상위자)",
    "colleague": "동료 연구자/대학원생",
    "external": "외부 연구자/기관 담당자",
}

SYSTEM_PROMPT_KO = """\
당신은 한국 대학원생이 학술 이메일을 작성하는 것을 돕는 전문 어시스턴트입니다.
사용자가 제공하는 bullet point를 기반으로, 수신자 유형과 톤에 맞는 완성된 한국어 이메일을 작성합니다.

규칙:
1. 수신자 유형에 따라 적절한 존칭과 호칭을 사용합니다.
   - professor: "교수님" 호칭, 최대 경어체 (-습니다/-겠습니다)
   - colleague: 친근하지만 예의 있는 표현 (-요/-습니다)
   - external: 격식 있는 비즈니스 한국어
2. tone이 formal이면 격식체, casual이면 약간 부드러운 톤으로 작성합니다.
3. 이메일 구조: 인사 → 자기소개(필요 시) → 본문 → 마무리 인사 → 이름
4. 핵심 내용을 빠뜨리지 않되, 자연스럽게 연결합니다.
5. 과도한 미사여구 없이 간결하고 명확하게 작성합니다.
"""

SYSTEM_PROMPT_EN = """\
You are an expert assistant helping graduate students write academic emails.
Based on the user's bullet points, compose a complete, polished email matching
the recipient type and tone.

Rules:
1. Match formality to recipient type (professor=most formal, colleague=friendly professional, external=business formal).
2. Structure: greeting → intro (if needed) → body → closing → name placeholder.
3. Cover all bullet points naturally without being verbose.
"""

JSON_SCHEMA = {
    "name": "academic_email",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
                "description": "이메일 제목 / Email subject line",
            },
            "greeting": {
                "type": "string",
                "description": "인사말 / Greeting line",
            },
            "body": {
                "type": "string",
                "description": "본문 / Main body text",
            },
            "closing": {
                "type": "string",
                "description": "마무리 인사 및 서명 / Closing and signature placeholder",
            },
            "full_text": {
                "type": "string",
                "description": "전체 이메일 텍스트 (바로 붙여넣기 가능) / Complete email ready to paste",
            },
            "tone_used": {
                "type": "string",
                "description": "사용된 톤 설명 / Description of tone applied",
            },
        },
        "required": ["subject", "greeting", "body", "closing", "full_text", "tone_used"],
        "additionalProperties": False,
    },
}


def build_messages(bullets: str, recipient_type: str, tone: str, lang: str) -> list:
    system = SYSTEM_PROMPT_KO if lang == "ko" else SYSTEM_PROMPT_EN
    recipient_desc = RECIPIENT_LABELS.get(recipient_type, recipient_type)

    user_msg = f"""수신자 유형: {recipient_desc}
톤: {tone}
언어: {lang}

핵심 내용:
{bullets}

위 내용을 바탕으로 완성된 이메일을 작성해주세요."""

    return [
        {"role": "system", "content": system},
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
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    if resp.status_code != 200:
        detail = resp.text[:500]
        print(f"[ERROR] API returned {resp.status_code}: {detail}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def main():
    parser = argparse.ArgumentParser(description="Korean academic email writer (Upstage Solar)")
    parser.add_argument("--bullets", required=True, help="Bullet points of email content")
    parser.add_argument(
        "--recipient-type",
        required=True,
        choices=["professor", "colleague", "external"],
        help="Recipient type",
    )
    parser.add_argument("--tone", default="formal", choices=["formal", "casual"], help="Tone")
    parser.add_argument("--lang", default="ko", choices=["ko", "en"], help="Output language")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Upstage model name")
    parser.add_argument("--api-key", default=None, help="Upstage API key (or UPSTAGE_API_KEY env)")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("UPSTAGE_API_KEY")
    if not api_key:
        print("[ERROR] API key required. Use --api-key or set UPSTAGE_API_KEY env var.", file=sys.stderr)
        sys.exit(1)

    if not args.bullets.strip():
        print("[ERROR] --bullets cannot be empty.", file=sys.stderr)
        sys.exit(1)

    messages = build_messages(args.bullets, args.recipient_type, args.tone, args.lang)
    print(f"[INFO] Calling {args.model} for {args.recipient_type}/{args.tone} email...", file=sys.stderr)
    result = call_api(api_key, args.model, messages)

    os.makedirs(args.output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(args.output_dir, f"academic_mail_{ts}.mail.json")
    txt_path = os.path.join(args.output_dir, f"academic_mail_{ts}.mail.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"제목: {result['subject']}\n\n")
        f.write(result["full_text"])

    print(f"[OK] JSON: {json_path}", file=sys.stderr)
    print(f"[OK] Text: {txt_path}", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
