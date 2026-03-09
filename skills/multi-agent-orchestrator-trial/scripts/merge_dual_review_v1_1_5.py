#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def has_hard_gate(r):
    blockers = r.get('release_blockers', [])
    security_fail = any('fail' in str(x).lower() for x in r.get('security_check', []))
    accept_fail = any(': fail' in str(x).lower() for x in r.get('acceptance_check', []))
    return bool(blockers) or security_fail or accept_fail


def main():
    if len(sys.argv) < 4:
        print('Usage: merge_dual_review_v1_1_5.py <primary.json> <secondary.json> <out.json>')
        return 2

    p = load(sys.argv[1])
    s = load(sys.argv[2])
    out = Path(sys.argv[3])

    conflicts = []
    if has_hard_gate(p) or has_hard_gate(s):
        merged = 'fail'
        conflicts.append('hard_gate_triggered')
    else:
        pv, sv = p.get('verdict'), s.get('verdict')
        pt = p.get('scores', {}).get('total', 0)
        st = s.get('scores', {}).get('total', 0)
        if pv != sv:
            conflicts.append(f'verdict_mismatch:{pv}!={sv}')
        if abs(pt - st) > 3:
            conflicts.append(f'score_delta_gt_3:{pt}-{st}')

        if conflicts:
            merged = 'pass_with_risk' if ('pass_with_risk' in (pv, sv)) else 'fail'
        else:
            merged = 'pass' if pv == 'pass' and sv == 'pass' else 'pass_with_risk'

    payload = {
        'task_id': p.get('task_id') or s.get('task_id') or 'UNKNOWN',
        'schema_version': 'dual_review.v1',
        'dual_review': {
            'primary': {'verdict': p.get('verdict'), 'scores': p.get('scores', {})},
            'secondary': {'verdict': s.get('verdict'), 'scores': s.get('scores', {})},
            'merged_verdict': merged,
            'conflicts': conflicts,
            'arbiter_note': 'auto-merged by merge_dual_review_v1_1_5.py'
        }
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(str(out))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
