# GitHub Pages + Custom Domain

목표 도메인: `upstage-n8n.jaeyeong2026.com`

## 이미 적용된 것
- `site/CNAME` 파일 포함
- `.github/workflows/pages.yml`로 `site/` 자동 배포

## DNS 설정(jaeyeong2026.com 관리 콘솔에서 1회)

서브도메인 충돌 없이 별도 운영하려면 CNAME 레코드 1개만 추가:

- Type: `CNAME`
- Name: `upstage-n8n`
- Target: `<your-github-username>.github.io`
  - 현재 계정 기준: `Jaeyeong-CHOI.github.io`
- Proxy: DNS only (Cloudflare 사용 시)

## 확인
1. GitHub repo → Settings → Pages에서 custom domain 상태 확인
2. `https://upstage-n8n.jaeyeong2026.com` 접속 확인
3. 페이지에서 키 입력 후 `.filled.json` 다운로드 확인
