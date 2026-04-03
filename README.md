# Upstage AI Ambassador 2026

Upstage AI Ambassador 활동 기록 및 미션 산출물 관리 레포.

---

## 📋 미션 개요

| # | 미션 | 마감 | 상태 |
|---|------|------|------|
| 1 | No Code 기반 자동화 워크플로우 | 2026-03-31 | ✅ 구현 완료 |
| 2 | Upstage API 활용 Skill 개발 | 2026-04-19 | 🔨 구현 완료 |
| 3 | Upstage 제품 SNS 공유 | 2026-05-03 | ⬜ 미착수 |
| 4 | Upstage API 활용 프로젝트 개발 | 2026-05-22 | ⬜ 미착수 |

---

## 🚀 미션 1: Daily Paper Digest

HuggingFace Daily Papers를 매일 자동 수집 → **Upstage Solar**로 한국어 구조화 요약 → 이메일 Digest.

3단계 워크플로우로 구성해, 필요한 수준에 맞게 선택할 수 있습니다.

### 워크플로우

| Step | 파일 | 설명 | Upstage API |
|------|------|------|:-----------:|
| **1** | `workflow.daily-paper-digest.json` | 📬 HF 인기 논문 Top 10 제목+링크 → 이메일 | 불필요 |
| **2** | `workflow.daily-paper-summary.json` | 📄 Top 10 논문 구조화 요약 (문제-방법-결과-한계) → 이메일 | ✅ 필요 |
| **3** | `workflow.research-briefing.json` | 🧠 Top 5 심층 분석 + 트렌드 종합 + 탐색 키워드 → 리서치 브리핑 이메일 | ✅ 필요 |

### 빠른 시작

#### 웹에서 다운로드 (권장)

1. [**upstage-n8n.jaeyeong2026.com**](https://upstage-n8n.jaeyeong2026.com) 접속
2. 워크플로우 선택 → (Step 2, 3만) API 키 입력 → JSON 다운로드
3. n8n → Import from File → SMTP 크레덴셜 설정 → 실행

> API 키는 [Upstage Console](https://console.upstage.ai)에서 무료 발급.
> 키는 브라우저에서만 처리되며 서버로 전송되지 않습니다.

#### 직접 Import

1. 원하는 `workflow.*.json` 파일 다운로드
2. n8n → Import from File
3. `UPSTAGE_API_KEY` 환경변수 설정 (Step 2, 3)
4. SMTP 크레덴셜 + 수신 이메일 주소 설정

> ⚠️ 절대 깃허브에 실제 API 키를 커밋하지 마세요.

### 파이프라인 구조

```
                    ┌─ Step 1: 제목+링크 목록 ─────────────────────── → 이메일
Schedule Trigger    │
  → HF Daily Papers ├─ Step 2: + Jina Reader + Upstage 요약 ────── → 이메일
    API (Top 10)    │
                    └─ Step 3: + 심층 분석 + 트렌드 종합 (2× LLM) ─ → 이메일
```

### 요약 출력 예시 (Step 2)

```json
{
  "title": "Attention Is All You Need",
  "one_line": "셀프 어텐션만으로 시퀀스 변환을 수행하는 Transformer 아키텍처 제안",
  "problem": "기존 RNN/CNN의 병렬화 한계와 장거리 의존성 문제",
  "method": "멀티헤드 셀프 어텐션 + 포지셔널 인코딩",
  "results": "WMT14 EN-DE BLEU 28.4 (SOTA)",
  "limitations": "O(n²) 메모리, 고정 컨텍스트 윈도우",
  "tags": ["Transformer", "Attention"],
  "action_items": ["우리 데이터셋 적용", "Efficient Attention 비교"]
}
```

---

## 🎓 미션 2: Korean Academic Toolkit (Upstage Solar Skills)

Upstage Solar(`solar-pro-3`, 102B MoE)의 한국어 능력을 활용한 학술 워크플로우 CLI 스킬 3종.

### 스킬 목록

| # | 스킬 | 설명 | 입력 → 출력 |
|---|------|------|-------------|
| 1 | `upstage-academic-mail` | ✉️ 한국어 학술 이메일 작성기 | bullet points → 완성된 이메일 |
| 2 | `upstage-paper-to-script` | 🎬 논문→발표 스크립트 생성기 | 논문 텍스트 → 타이밍 포함 스크립트 |
| 3 | `upstage-script-polisher` | 🎤 발표 스크립트 구어체 폴리싱 | 스크립트 → 자연스러운 발표 원고 |

### 파이프라인

```
논문 (PDF/텍스트)
  → upstage-paper-to-script (15분 세미나 스크립트 생성)
    → upstage-script-polisher (자연스러운 구어체로 폴리싱)
```

### 빠른 시작

```bash
# 1. 의존성 설치
pip install requests

# 2. API 키 설정
export UPSTAGE_API_KEY="up_xxxxxxxxxxxxxxx"

# 3. 교수님께 이메일 작성
python3 skills/upstage-academic-mail/scripts/run_academic_mail.py \
  --bullets "UGRP 중간보고 일정 확인, 발표자료 검토 요청" \
  --recipient-type professor --tone formal

# 4. 논문 → 발표 스크립트
python3 skills/upstage-paper-to-script/scripts/run_paper_to_script.py \
  --text-file paper.txt --duration 15 --style seminar

# 5. 스크립트 폴리싱
python3 skills/upstage-script-polisher/scripts/run_script_polisher.py \
  --input paper_script.script.md --style academic
```

### 스킬 다운로드

- **웹**: [Skills 페이지](https://upstage-n8n.jaeyeong2026.com/skills.html)
- **GitHub**: `skills/` 디렉토리에서 직접 다운로드

### 특징

- 🇰🇷 **한국어 특화**: Solar의 한국어 존칭/격식체 이해 활용
- 📊 **구조화된 출력**: JSON Schema로 일관된 결과 보장
- 🔗 **파이프라인**: 스킬 간 연결로 논문→발표 완전 자동화
- 🔑 **간편 설정**: `requests` 라이브러리만 필요, 복잡한 SDK 불필요

---

## 🗂 레포 구조

```
├── workflow.*.json          # n8n 워크플로우 3종 (미션 1)
├── skills/                  # Upstage Solar 스킬 3종 (미션 2)
│   ├── upstage-academic-mail/
│   ├── upstage-paper-to-script/
│   └── upstage-script-polisher/
├── missions/                # 미션 계획/진행/템플릿
├── docs/                    # GitHub Pages (upstage-n8n.jaeyeong2026.com)
├── scripts/                 # CI 검증 스크립트
├── tests/                   # 테스트 fixture
└── .github/workflows/       # CI + Pages 배포
```

---

## 🔗 링크

- **워크플로우 다운로드**: [upstage-n8n.jaeyeong2026.com](https://upstage-n8n.jaeyeong2026.com)
- **스킬 다운로드**: [upstage-n8n.jaeyeong2026.com/skills.html](https://upstage-n8n.jaeyeong2026.com/skills.html)
- **Upstage Console**: [console.upstage.ai](https://console.upstage.ai)
- **HF Daily Papers**: [huggingface.co/papers](https://huggingface.co/papers)

---

## 🔒 보안

- `.env` 파일은 `.gitignore`에 포함
- 워크플로우 내 API 키는 플레이스홀더 (`REPLACE_WITH_YOUR_REAL_KEY`)
- 웹 다운로드 시 키는 브라우저 로컬에서만 처리

---

## 라이선스

MIT
