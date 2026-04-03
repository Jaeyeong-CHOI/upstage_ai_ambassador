# Script Polisher Prompt Guide

## 구어체 변환 가이드

### 문어체 → 구어체 변환 패턴

| 문어체 | 구어체 (academic) | 구어체 (ted-talk) |
|--------|-------------------|-------------------|
| ~것이다 | ~겁니다 | ~거예요 |
| ~하였다 | ~했는데요 | ~했어요 |
| ~함으로써 | ~하면서 | ~하면 |
| ~에 의하면 | ~에 따르면 | ~을 보면 |
| 수행하였다 | 수행했습니다 | 해봤는데요 |
| 관찰되었다 | 관찰할 수 있었습니다 | 볼 수 있었어요 |

### 스타일별 특성

#### conversational (대화형)
- "여러분" 호칭 사용
- 질문형 표현 다수 ("~하신 적 있으시죠?")
- 짧은 문장 위주
- 구어적 연결사 ("그래서", "근데", "자 그러면")

#### academic (학술)
- "여러분" 또는 청중 언급 최소화
- 논리적 연결사 ("따라서", "이를 바탕으로")
- 전문 용어 유지하되 설명 추가
- 적절한 문장 길이 유지

#### ted-talk (TED Talk)
- 스토리텔링 기법 활용
- 감정적 호소 ("놀라운 결과였습니다")
- 짧은 임팩트 문장 + 긴 설명 교차
- 청중 참여 유도 ("잠깐 생각해보세요")

### 발음 힌트 대상

- 영어 약어: BERT(버트), GPT(지피티), BLEU(블루)
- 숫자/통계: "28.4%" → "이십팔 점 사 퍼센트"
- 수식: O(n²) → "오 엔 제곱"
- 연도: "2024년" → "이천이십사 년"

### JSON 파이프라인 (`--from-json`)

`paper-to-script`의 JSON 출력을 직접 읽어서 폴리싱합니다:

```bash
# 완전한 논문 → 발표 파이프라인
python3 run_paper_to_script.py \
  --text-file paper.txt --style seminar \
  --audience-context "학부생 대상" \
  --output-dir out/

python3 run_script_polisher.py \
  --from-json "out/paper_script_*.script.json" \
  --style conversational \
  --output-dir out/
```

`--from-json`은 JSON에서 모든 섹션의 `script` 필드를 추출하고, `transition_note`와 `closing_remarks`도 포함하여 하나의 연속된 텍스트로 만든 뒤 폴리싱합니다.

glob 패턴 지원: 여러 파일이 매칭되면 가장 최근 파일을 사용합니다.

### stdin 파이핑 (`--input -`)

```bash
# 다른 도구의 출력을 파이프로 연결
cat generated_script.md | python3 run_script_polisher.py --input - --style academic
```

### Before/After 비교

마크다운 출력에 각 문단의 원문과 수정본을 나란히 보여줍니다:

```markdown
### 문단 1

**Before (원문):**
> 본 연구에서는 트랜스포머 아키텍처를 활용하여...

**After (수정):**
> 이번 연구에서는 트랜스포머 아키텍처를 활용했는데요...
```

이 비교를 통해 어떤 부분이 어떻게 수정되었는지 한눈에 확인할 수 있습니다.

### 처리 한도

- 입력 텍스트: 최대 16,000자 (초과 시 트리밍)
- max_tokens: 8192 (이전 4096에서 확장)
- 긴 스크립트도 충분히 상세하게 폴리싱 가능
