# Classification Scorecard (v0.5)

Score each dimension 0-2:
- Uncertainty (U)
- Risk impact (R)
- External dependency (E)
- Change surface (C)

Total = U + R + E + C

## Routing Thresholds
- 0-2 => L1
- 3-5 => L2
- 6-8 => L3

Jarvis must output:
```json
{
  "classification_rationale": {
    "U": 0,
    "R": 0,
    "E": 0,
    "C": 0,
    "total": 0,
    "class": "L1|L2|L3"
  }
}
```
