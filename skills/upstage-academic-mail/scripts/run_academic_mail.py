#!/usr/bin/env python3
"""Korean academic email writer powered by Upstage Solar.

Usage:
    python3 run_academic_mail.py \
        --bullets "졸업논문 피드백 미팅 요청, 다음 주 가능 여부 확인" \
        --recipient-type professor --tone formal

    # Reply to a previous email
    python3 run_academic_mail.py \
        --bullets "미팅 일정 확인, 목요일 오후 가능" \
        --recipient-type professor --tone formal \
        --reply-to previous_email.txt

    # With additional context
    python3 run_academic_mail.py \
        --bullets "공동연구 제안, 데이터셋 공유 요청" \
        --recipient-type external --tone formal \
        --context "EMNLP 2025에서 만남, 유사 연구 주제 논의"

    # With CC note
    python3 run_academic_mail.py \
        --bullets "프로젝트 진행 상황 보고" \
        --recipient-type professor --tone formal \
        --cc-note "공동지도교수님께도 진행 상황 공유 드립니다"
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

고급 규칙:
6. **암묵적 긴급성 감지**: bullet point에 "급히", "오늘 내", "마감" 등이 있으면 긴급한 톤으로, "여유 있을 때", "편하실 때" 등이 있으면 여유로운 톤으로 조정합니다.
7. **상황별 공손함 조절**:
   - 첫 연락: 자기소개 포함, 배경 설명 충분히, 최대 공손
   - 후속 연락/팔로업: "지난번 말씀드린 건으로" 식의 간결한 연결
   - 리마인더: 정중하되 명확한 요청 ("혹시 확인해 주셨는지 여쭙니다")
8. **제목 구체화**: "문의드립니다" 같은 generic 제목 절대 금지. 핵심 키워드를 제목에 넣어 수신자가 한눈에 용건을 파악하도록 합니다. 예: "[미팅 요청] 졸업논문 3장 피드백 관련", "[데이터셋 공유 요청] EMNLP 발표 후속"
9. **답장 모드**: 이전 이메일이 주어지면 그 이메일의 톤과 맥락을 분석하여 자연스러운 답장을 작성합니다. 이전 이메일에서 언급된 주제를 참조하고, 새로운 내용을 자연스럽게 이어갑니다.
10. **CC 안내**: CC 대상이 있으면 이메일 첫 부분이나 끝에 CC 대상을 왜 포함했는지 간결하게 안내합니다.
11. **맥락 반영**: 추가 맥락(만남 경위, 공유 배경 등)이 주어지면 이메일 도입부에 자연스럽게 녹여 넣습니다.
"""

SYSTEM_PROMPT_EN = """\
You are an expert assistant helping graduate students write academic emails.
Based on the user's bullet points, compose a complete, polished email matching
the recipient type and tone.

Rules:
1. Match formality to recipient type (professor=most formal, colleague=friendly professional, external=business formal).
2. Structure: greeting → intro (if needed) → body → closing → name placeholder.
3. Cover all bullet points naturally without being verbose.

Advanced rules:
4. **Detect implied urgency**: If bullets mention deadlines, "ASAP", "urgent", adopt a more urgent but still polite tone. If relaxed language is used, match it.
5. **Situation-aware politeness**:
   - First contact: include introduction, background, maximum courtesy.
   - Follow-up: brief reference to previous communication, concise.
   - Reminder: polite but clear request.
6. **Specific subject lines**: Never use generic subjects like "Inquiry". Include key topic keywords so the recipient immediately understands the purpose.
7. **Reply mode**: If a previous email is provided, analyze its tone and context to write a natural reply that references the previous discussion.
8. **CC note**: If CC recipients are mentioned, briefly explain why they're included.
9. **Context weaving**: If additional context is provided (e.g., where you met, shared background), weave it naturally into the opening.
"""

JSON_SCHEMA = {
    "name": "academic_email",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
                "description": "이메일 제목 / Email subject line (구체적으로, generic 금지)",
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


def build_messages(
    bullets: str,
    recipient_type: str,
    tone: str,
    lang: str,
    reply_to_text: str | None = None,
    context: str | None = None,
    cc_note: str | None = None,
) -> list:
    system = SYSTEM_PROMPT_KO if lang == "ko" else SYSTEM_PROMPT_EN
    recipient_desc = RECIPIENT_LABELS.get(recipient_type, recipient_type)

    user_parts = [f"수신자 유형: {recipient_desc}", f"톤: {tone}", f"언어: {lang}"]

    if reply_to_text:
        user_parts.append(f"\n--- 이전 이메일 (답장 대상) ---\n{reply_to_text[:6000]}\n--- 이전 이메일 끝 ---")
        user_parts.append("\n위 이메일에 대한 **답장**을 작성해주세요.")

    if context:
        user_parts.append(f"\n추가 맥락: {context}")

    if cc_note:
        user_parts.append(f"\nCC 안내 문구: {cc_note}")

    user_parts.append(f"\n핵심 내용:\n{bullets}")
    user_parts.append("\n위 내용을 바탕으로 완성된 이메일을 작성해주세요.")

    user_msg = "\n".join(user_parts)

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
    parser.add_argument(
        "--reply-to",
        default=None,
        help="Path to a previous email text file to reply to",
    )
    parser.add_argument(
        "--context",
        default=None,
        help="Additional context to weave into the email (e.g., 'EMNLP에서 만남')",
    )
    parser.add_argument(
        "--cc-note",
        default=None,
        help="Polite note explaining why CC recipients are included",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("UPSTAGE_API_KEY")
    if not api_key:
        print("[ERROR] API key required. Use --api-key or set UPSTAGE_API_KEY env var.", file=sys.stderr)
        sys.exit(1)

    if not args.bullets.strip():
        print("[ERROR] --bullets cannot be empty.", file=sys.stderr)
        sys.exit(1)

    # Read reply-to file if provided
    reply_to_text = None
    if args.reply_to:
        if not os.path.isfile(args.reply_to):
            print(f"[ERROR] Reply-to file not found: {args.reply_to}", file=sys.stderr)
            sys.exit(1)
        with open(args.reply_to, "r", encoding="utf-8") as f:
            reply_to_text = f.read().strip()
        if not reply_to_text:
            print("[ERROR] Reply-to file is empty.", file=sys.stderr)
            sys.exit(1)
        print(f"[INFO] Reply mode: referencing {args.reply_to}", file=sys.stderr)

    messages = build_messages(
        args.bullets,
        args.recipient_type,
        args.tone,
        args.lang,
        reply_to_text=reply_to_text,
        context=args.context,
        cc_note=args.cc_note,
    )

    mode = "reply" if reply_to_text else "compose"
    print(f"[INFO] Calling {args.model} for {args.recipient_type}/{args.tone} email ({mode})...", file=sys.stderr)
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
