#!/usr/bin/env python3
"""Export canonical Markdown grid/meta as reproducible runtime JSON (stdlib only).

Run after any edit to either source Markdown, including notes/tables, because
source.sha256 identifies the whole source file. --check never writes files.
"""
import argparse
import hashlib
import json
import re
from check_layout import a0, upper_controls, hud_spec
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NAMES = ('lay_dao_uc_v1', 'lay_dao_uc_boss_v1')


def build(source):
    raw = source.read_bytes()
    text = raw.decode('utf-8')
    blocks = {}
    for name in ('layout', 'layout-meta'):
        found = re.search(rf'^```{name}[ \t]*\r?\n(.*?)^```[ \t]*\r?$', text, re.M | re.S)
        if not found:
            raise ValueError(f'{source}: missing {name} block')
        blocks[name] = found[1]
    rows = blocks['layout'].splitlines()  # do not strip any row or normalize its characters
    if not rows or len({len(row) for row in rows}) != 1:
        raise ValueError(f'{source}: nonrectangular grid')
    data = {'version': 1, 'source': {'file': source.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(raw).hexdigest()},
            'meta': json.loads(blocks['layout-meta']), 'rows': rows}
    kind=data['meta'].get('kind','field')
    data['hud']=dict(hud_spec()) if kind=='boss' else {'show_minimap':True}
    data['hud']['expected_top_rects']={str(width):upper_controls(width,a0(),kind) for width in [960,1200]}
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(); failures = 0
    for name in NAMES:
        source = ROOT/'design/maps'/f'{name}.md'
        target = ROOT/'prototype/dao_uc/layouts'/f'{name}.json'
        try:
            data = build(source)
            expected = (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
            if args.check:
                ok = target.is_file() and target.read_bytes() == expected
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(expected); ok = True
            failures += not ok
            print(f'{"OK" if ok else "FAIL"}: {target.relative_to(ROOT)}; rows={len(data["rows"])} cols={len(data["rows"][0])}; source_sha256={data["source"]["sha256"]}; {"check only" if args.check else "written"}')
        except (ValueError, OSError) as error:
            failures += 1; print('FAIL:',error)
    return 1 if failures else 0


if __name__ == '__main__': raise SystemExit(main())
