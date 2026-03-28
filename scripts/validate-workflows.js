const fs = require('fs');

const files = [
  'workflow.upstage-hf-paper-summarizer.json',
  'workflow.upstage-hf-paper-summarizer-advanced.json',
  'workflow.research-orchestrator-pro.json',
  'workflow.upstage-daily-paper-digest.json',
];

const requiredTopKeys = ['name', 'nodes', 'connections', 'active', 'settings'];
let failed = false;

function assert(cond, msg) {
  if (!cond) {
    console.error('❌', msg);
    failed = true;
  } else {
    console.log('✅', msg);
  }
}

for (const file of files) {
  console.log(`\n--- Validating ${file} ---`);
  let wf;
  try {
    wf = JSON.parse(fs.readFileSync(file, 'utf8'));
    console.log('✅ valid JSON parse');
  } catch (e) {
    console.error('❌ invalid JSON:', e.message);
    failed = true;
    continue;
  }

  for (const k of requiredTopKeys) {
    assert(Object.prototype.hasOwnProperty.call(wf, k), `${file}: has top-level key '${k}'`);
  }

  assert(Array.isArray(wf.nodes) && wf.nodes.length > 0, `${file}: has nodes`);

  const nodeNames = new Set(wf.nodes.map(n => n.name));
  assert(nodeNames.size === wf.nodes.length, `${file}: node names are unique`);

  const manualTriggerNodes = wf.nodes.filter(n => n.type === 'n8n-nodes-base.manualTrigger');
  assert(manualTriggerNodes.length >= 1, `${file}: contains at least one manual trigger`);

  const webhookNodes = wf.nodes.filter(n => n.type === 'n8n-nodes-base.webhook');
  assert(webhookNodes.length === 0, `${file}: does not include webhook trigger`);

  const hasAuthHeader = wf.nodes.some(n => {
    if (n.type !== 'n8n-nodes-base.httpRequest') return false;
    const ps = n.parameters?.headerParameters?.parameters || [];
    return ps.some(p => p.name === 'Authorization' && String(p.value || '').includes('Bearer'));
  });
  assert(hasAuthHeader, `${file}: has Bearer auth on at least one HTTP node`);

  const hasFallback = wf.nodes.some(n => {
    if (n.type !== 'n8n-nodes-base.httpRequest') return false;
    const ps = n.parameters?.headerParameters?.parameters || [];
    return ps.some(p => p.name === 'Authorization' && String(p.value || '').includes('REPLACE_WITH_YOUR_REAL_KEY'));
  });
  assert(hasFallback, `${file}: has hardcode fallback placeholder`);

  const connKeys = Object.keys(wf.connections || {});
  for (const n of connKeys) {
    assert(nodeNames.has(n), `${file}: connection key node '${n}' exists in nodes`);
  }
}

if (failed) {
  console.error('\nValidation FAILED');
  process.exit(1);
} else {
  console.log('\n🎉 All workflow validations passed');
}
