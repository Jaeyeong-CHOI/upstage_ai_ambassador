const workflowSelect = document.getElementById('workflow');
const apiKeyInput = document.getElementById('apiKey');
const downloadBtn = document.getElementById('downloadBtn');

const TEMPLATE_BASE = './templates';

function escapeRegExp(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

downloadBtn.addEventListener('click', async () => {
  const key = apiKeyInput.value.trim();
  const selected = workflowSelect.value;

  if (!key) {
    alert('API 키를 입력해줘.');
    return;
  }

  try {
    const url = `${TEMPLATE_BASE}/${selected}`;
    const template = await fetch(url, { cache: 'no-store' }).then(r => {
      if (!r.ok) throw new Error(`템플릿 로드 실패: ${r.status}`);
      return r.text();
    });

    const token = 'REPLACE_WITH_YOUR_REAL_KEY';
    const replaced = template.replace(new RegExp(escapeRegExp(token), 'g'), key);

    const blob = new Blob([replaced], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = selected.replace('.json', '.filled.json');
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(a.href);
  } catch (e) {
    alert(`오류: ${e.message}`);
  }
});
