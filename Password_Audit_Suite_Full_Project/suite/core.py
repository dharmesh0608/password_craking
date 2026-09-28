"""Bounded, offline classroom demonstrations. No live authentication or host acquisition."""
import csv
import hashlib
import html
import itertools
import math
import re
from pathlib import Path

COMMON = {'password', 'password123', '123456', 'qwerty', 'admin', 'welcome', 'letmein', 'iloveyou', 'abc123'}
LEET = str.maketrans({'a':'@','e':'3','i':'1','o':'0','s':'$'})
MAX_WORDS = 5000
MAX_ATTEMPTS = 100000


def variants(seed, limit=100):
    """Generate bounded classroom guesses without writing secrets to disk."""
    if not seed or len(seed) > 40 or not 1 <= limit <= MAX_WORDS:
        raise ValueError('Seed must be 1-40 characters; limit 1-5000')
    base = seed.strip().lower()
    candidates = (v for stem in (base, base.title(), base.upper(), base.translate(LEET))
                  for v in (stem, stem+'1', stem+'123', stem+'2026', stem+'!'))
    return list(itertools.islice(dict.fromkeys(candidates), limit))


def analyze(password):
    if not password:
        raise ValueError('Password cannot be empty')
    classes = sum(bool(re.search(p, password)) for p in (r'[a-z]',r'[A-Z]',r'\d',r'[^\w\s]'))
    alphabet = sum(n for p,n in ((r'[a-z]',26),(r'[A-Z]',26),(r'\d',10),(r'[^\w\s]',32)) if re.search(p,password))
    naive_bits = len(password)*math.log2(max(alphabet,1))
    reasons = []
    folded = password.lower()
    if len(password)<12: reasons.append('fewer than 12 characters')
    if classes<3: reasons.append('limited character variety')
    if any(w in folded for w in COMMON if len(w)>=5): reasons.append('contains a common password')
    if re.search(r'(.)\1\1|1234|qwerty|abcd',folded): reasons.append('predictable sequence or repetition')
    return {'length':len(password),'classes':classes,'naive_entropy_bits':round(naive_bits,1),
            'rating':'weak' if reasons else 'stronger', 'reasons':reasons,
            'note':'Entropy assumes uniform random selection and overstates human-created passwords.'}


def inspect_hash(line):
    """Classify synthetic hash examples. Never read OS credential stores."""
    value=line.strip()
    if value.startswith('$6$'): kind='sha512-crypt'
    elif value.startswith('$5$'): kind='sha256-crypt'
    elif value.startswith('$1$'): kind='md5-crypt'
    elif value.startswith('$y$'): kind='yescrypt'
    elif re.fullmatch(r'[0-9a-fA-F]{32}',value): kind='32-hex digest (ambiguous: MD5 or NT hash)'
    elif value in ('!','*','!!'): kind='locked account marker'
    else: kind='unknown'
    return {'format':kind,'salted':kind.endswith('-crypt') or kind=='yescrypt', 'input_redacted':True}


def inspect_shadow_fixture(path):
    """Inspect an explicitly supplied synthetic shadow-format fixture, without returning hashes."""
    rows=[]
    with Path(path).open(encoding='utf-8-sig') as source:
        for number, line in enumerate(source, 1):
            if not line.strip() or line.startswith('#'):
                continue
            parts=line.rstrip('\n').split(':')
            if len(parts)!=9 or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]{0,31}',parts[0]):
                raise ValueError(f'Invalid fixture line {number}')
            rows.append({'account':parts[0], **inspect_hash(parts[1])})
    return rows


def simulate(target, candidates, max_attempts=1000):
    """Compare SHA-256 digests of locally supplied lab values with a firm attempt cap."""
    if not 1<=max_attempts<=MAX_ATTEMPTS: raise ValueError('Attempts must be 1-100000')
    digest=hashlib.sha256(target.encode()).digest()
    tries=0
    for candidate in itertools.islice(candidates,max_attempts):
        tries+=1
        if hashlib.sha256(candidate.encode()).digest()==digest:
            return {'attempts':tries,'matched':True,'candidate':candidate,'mode':'local SHA-256 teaching demo'}
    return {'attempts':tries,'matched':False,'candidate':None,'mode':'local SHA-256 teaching demo'}


def estimate(length, alphabet_size, guesses_per_second):
    if not 1<=length<=128 or not 1<=alphabet_size<=100 or guesses_per_second<=0:
        raise ValueError('Positive parameters required')
    space=alphabet_size**length
    return {'search_space':space,'average_seconds':space/(2*guesses_per_second),
            'assumption':'Uniform random password; fixed illustrative rate, no rate limiting.'}


def audit_csv(path):
    """CSV contains disposable sample passwords; report omits plaintext."""
    rows=[]
    with Path(path).open(newline='',encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            if row is None:
                continue
            if 'label' not in row or 'password' not in row:
                raise ValueError('CSV needs label,password columns')
            label = (row.get('label') or '').strip()
            password = (row.get('password') or '').strip()
            if not label or not password:
                continue
            result=analyze(password)
            rows.append({'label':label[:80], 'length':result['length'],
                         'rating':result['rating'],'reasons':result['reasons']})
    return rows


def report_html(report):
    """Build a standalone escaped HTML report from redacted audit data."""
    rows=''.join('<tr><td>'+html.escape(str(x['label']))+'</td><td>'+str(x['length'])+
                 '</td><td>'+html.escape(str(x['rating']))+'</td><td>'+
                 html.escape(', '.join(x['reasons']) or 'No basic flags')+'</td></tr>'
                 for x in report['results'])
    advice=''.join('<li>'+html.escape(x)+'</li>' for x in report['recommendations'])
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Password audit</title>'
            '<style>body{font:16px system-ui;max-width:950px;margin:3rem auto;color:#172536}'
            'h1{color:#075c9a}table{border-collapse:collapse;width:100%}td,th{padding:12px;'
            'border:1px solid #cad4e0;text-align:left}th{background:#e9f3fc}</style>'
            '<h1>Password audit lab report</h1><p>Disposable samples: '+str(report['sample_count'])+
            ' | Weak findings: '+str(report['weak_count'])+'</p><table><thead><tr>'
            '<th>Label</th><th>Length</th><th>Rating</th><th>Reasons</th></tr></thead><tbody>'+
            rows+'</tbody></table><h2>Recommendations</h2><ul>'+advice+'</ul>'
            '<p>Heuristic teaching report. No plaintext passwords are included.</p></html>')
