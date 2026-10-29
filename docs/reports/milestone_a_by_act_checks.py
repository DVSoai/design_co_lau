"""Run from any directory; compare the actual working tree with local main."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def base(path):
    return git('show', f'main:{path}')


def section(data, heading):
    start = data.index(heading)
    match = re.search(rb'^## ', data[start + len(heading):], re.M)
    return data[start:] if match is None else data[:start + len(heading) + match.start()][start:]


freeze = (ROOT / 'docs/11_design_freeze.md').read_bytes()
text = freeze.decode()
previous = base('docs/11_design_freeze.md')
parts = {}
for name in ['A1', 'A2', 'A3', 'A4', 'A5', 'B', 'C']:
    parts[name] = section(freeze, f'## Mốc {name} —'.encode()).decode()
checked = sum(len(re.findall(r'^- \[x\]', parts[f'A{i}'], re.M)) for i in range(1, 6))
print(f'A1–A5: - [x] = {checked}')
assert checked == 3
for name, part in parts.items():
    count = len(re.findall(r'^- \[ \]', part, re.M))
    print(f'{name}: - [ ] = {count}')

for heading in ['## Mốc A0 —', '## Mốc C —', '## Quyết định đã chốt']:
    assert section(previous, heading.encode()) == section(freeze, heading.encode()), heading
    print(f'PASS: {heading} unchanged byte-for-byte')
signoff = b'28/10/2026 \xe2\x80\x94 \xc4\x90\xc3\xa3 qua m\xe1\xbb\x91c A0.'
old_signoff = next(line for line in previous.splitlines(keepends=True) if line.startswith(signoff))
assert old_signoff in freeze.splitlines(keepends=True)
print('PASS: original A0 signoff unchanged byte-for-byte')
decisions = section(previous, '## Quyết định đã chốt'.encode()).decode()
print(f'Historical decision bullets preserved: {len(re.findall(r"^- ", decisions, re.M))} (request described 8)')

old_a = section(previous, ('## Mốc ' + 'A —').encode()).decode()
old_checked = re.findall(r'^- \[x\].*$', old_a, re.M)
assert re.findall(r'^- \[x\].*$', parts['A1'], re.M) == old_checked
assert all(not re.search(r'^- \[x\]', parts[f'A{i}'], re.M) for i in range(2, 6))
old_log = base('docs/05_log.md')
new_log = (ROOT / 'docs/05_log.md').read_bytes()
assert new_log.startswith(old_log)
diff_log = git('diff', 'main', '--', 'docs/05_log.md').decode()
assert not any(line.startswith('-') and not line.startswith('---') for line in diff_log.splitlines())
print('PASS: three checked conditions and notes unchanged; log is byte-prefix plus additions only')

changed = git('diff', '--name-only', 'main').decode().splitlines()
untracked = git('ls-files', '--others', '--exclude-standard').decode().splitlines()
assert all(p in ['README.md', 'AGENTS.md'] or p.startswith('docs/') for p in changed + untracked)
print('PASS: all changed/untracked files are within README.md, AGENTS.md, docs/')

supporting = [p for p in changed if p.startswith('docs/') and p not in
              ['docs/02_asset_list.md', 'docs/05_log.md', 'docs/11_design_freeze.md']
              and not p.startswith('docs/reports/')]


def numeric_literals(s):
    # Milestone names and document paths are identifiers, not gameplay quantities.
    s = re.sub(r'(?<!\w)A[1-5](?!\w)', 'A', s)
    s = re.sub(r'(?:docs/)?\d{2}_[\w]+\.md', 'DOCUMENT', s)
    return re.findall(r'\d+(?:[.,]\d+)*', s)


for p in supporting:
    assert numeric_literals(base(p).decode()) == numeric_literals((ROOT / p).read_text()), p
print('PASS: all numeric literals in supporting specifications unchanged (excluding milestone/document identifiers)')
old_tables = [line for line in base('docs/GDD.md').decode().splitlines() if line.startswith('|')]
new_tables = [line for line in (ROOT / 'docs/GDD.md').read_text().splitlines() if line.startswith('|')]
assert len(old_tables) == len(new_tables)
assert all(numeric_literals(a) == numeric_literals(b) for a, b in zip(old_tables, new_tables))
print('PASS: every GDD table retains its rows and numeric values')

asset = (ROOT / 'docs/02_asset_list.md').read_text()
old_asset = base('docs/02_asset_list.md').decode()
assert re.findall(r'^## Giai đoạn.*$', asset, re.M) == re.findall(r'^## Giai đoạn.*$', old_asset, re.M)
print('PASS: production stage headings/order unchanged')

report = (ROOT / 'docs/reports/milestone_a_by_act_mapping.md').read_text()
mapping = re.findall(r'^\| (\d{2}) \| (.*?) \|', report, re.M)
old_checks = re.findall(r'^- \[[ x]\].*$', old_a, re.M)
assert len(mapping) == len(old_checks) == 39
for i, (index, original) in enumerate(mapping, 1):
    assert int(index) == i and original.replace('\\|', '|') == old_checks[i - 1]
anchors = dict(re.findall(r'<a id="(a[1-5]-\d+)"></a>\s*\n(- \[[ x]\].*)', text))
targets = re.findall(r'\[A[1-5]-\d+\]\(\.\./11_design_freeze\.md#(a[1-5]-\d+)\): (.*?)(?=<br>| \|)', report)
assert set(anchors) == {anchor for anchor, _ in targets}
for anchor, line in targets:
    assert line.replace('\\|', '|') == anchors[anchor], anchor
print(f'PASS: mapping covers all 39 original checkboxes and all {len(anchors)} target checkboxes; links/text agree')

map_source = (ROOT / 'docs/08_map_layout.md').read_text()
map_ids = {name for line in map_source.splitlines() if line.startswith('- `lay_')
           for name in re.findall(r'`lay_(\w+)`', line)}
assigned = set()
for part in list(parts.values())[:5]:
    for line in part.splitlines():
        if line.startswith('- [ ] Cảnh nền và tileset:'):
            ids = set(re.findall(r'`(\w+)`', line))
            assert not assigned.intersection(ids), ids
            assigned.update(ids)
assert map_ids == assigned and len(map_ids) == 29, (map_ids - assigned, assigned - map_ids)
print('PASS: all 29 named map IDs assigned once for background/tilesets')

for i in range(2, 6):
    assert '- [ ] GDD.md khớp với docs/06–docs/14 cho phần của hồi đó.' in parts[f'A{i}']
assert parts['B'].splitlines()[2] == '- [ ] Đã qua A1–A5.'
assert all(f'"Đã qua mốc A{i}"' in text for i in range(1, 6))
print('PASS: per-act GDD checks, first B condition and five signoff templates present')

subprocess.run(['git', '-C', str(ROOT), 'diff', '--check'], check=True)
print('PASS: git diff --check')
