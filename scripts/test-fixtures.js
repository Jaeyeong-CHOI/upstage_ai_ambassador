const fs = require('fs');

const fixtures = [
  ['tests/fixtures/basic.request.json', ['targetLanguage', 'urls']],
  ['tests/fixtures/advanced.request.json', ['targetLanguage', 'focus', 'feedback', 'urls']],
  ['tests/fixtures/pro.request.json', ['targetLanguage', 'goal', 'feedback', 'items']],
  ['tests/fixtures/negative.empty_urls.request.json', ['targetLanguage', 'urls']],
];

let failed = false;
const assert = (cond, msg) => {
  if (!cond) {
    console.error('❌', msg);
    failed = true;
  } else {
    console.log('✅', msg);
  }
};

for (const [file, keys] of fixtures) {
  let json;
  try {
    json = JSON.parse(fs.readFileSync(file, 'utf8'));
    console.log(`\nFixture: ${file}`);
    console.log('✅ valid JSON parse');
  } catch (e) {
    console.error(`\nFixture: ${file}`);
    console.error('❌ invalid JSON parse', e.message);
    failed = true;
    continue;
  }

  keys.forEach((k) => assert(Object.prototype.hasOwnProperty.call(json, k), `${file}: contains '${k}'`));

  if (file.includes('basic') || file.includes('advanced') || file.includes('negative.empty_urls')) {
    assert(Array.isArray(json.urls), `${file}: urls is array`);
  }
  if (file.includes('pro')) {
    assert(Array.isArray(json.items), `${file}: items is array`);
  }
}

if (failed) {
  console.error('\nFixture validation FAILED');
  process.exit(1);
}

console.log('\n🎉 Fixture validation passed');
