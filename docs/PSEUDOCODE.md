# Pseudocode

## Signature Matching
```
function scan(file):
  hash = sha256(file)
  matches = []
  for sig in signatures:
    if sig.type == 'hash' and sig.sha256 == hash:
      matches.append(sig)
  if is_text(file):
    text = read_text(file)
    for sig in signatures:
      if sig.type == 'pattern' and regex_search(sig.pattern, text):
        matches.append(sig)
  return {hash, matches, pe_info(file)}
```

## Feature Extraction
```
function extract_features(report):
  duration = log1p(report.duration)
  stdout_chars = sum(len(e.data) for e in report.events if e.type == 'stdout')
  num_file = count(e for e in report.events if e.type == 'file_open')
  num_net = count(e for e in report.events if e.type == 'net_connect')
  exit_nonzero = any(e for e in report.events if e.type == 'process_exit' and e.code != 0)
  return [duration, log1p(stdout_chars), num_file, num_net, float(exit_nonzero)]
```

## On-Chain Validation (Mock)
```
function publish_signature(meta):
  entry = { id, name, sha256|pattern, publisher, ts=now, votes=0 }
  db.signatures.append(entry)
  return entry

function vote(id, up):
  s = db.find(id)
  s.votes += (1 if up else -1)
  return s

function accepted_signatures():
  return [s for s in db.signatures if s.votes >= THRESHOLD]
```
