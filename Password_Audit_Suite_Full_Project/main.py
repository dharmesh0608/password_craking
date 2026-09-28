import argparse
import json
from pathlib import Path
from suite.core import analyze, audit_csv, estimate, inspect_hash, inspect_shadow_fixture, report_html, simulate, variants


def main():
    p=argparse.ArgumentParser(description='Offline credential security teaching lab')
    sub=p.add_subparsers(dest='command',required=True)
    d=sub.add_parser('dictionary'); d.add_argument('seed'); d.add_argument('--limit',type=int,default=100)
    a=sub.add_parser('analyze'); a.add_argument('password',nargs='?',help='Only use disposable examples. Omit for interactive input.')
    h=sub.add_parser('inspect'); h.add_argument('sample',help='Synthetic hash or account lock marker')
    f=sub.add_parser('fixture'); f.add_argument('path',help='Instructor-provided synthetic shadow-format file')
    s=sub.add_parser('simulate'); s.add_argument('target',help='Disposable lab password'); s.add_argument('seed'); s.add_argument('--max-attempts',type=int,default=1000)
    e=sub.add_parser('estimate'); e.add_argument('length',type=int); e.add_argument('alphabet_size',type=int); e.add_argument('guesses_per_second',type=float)
    r=sub.add_parser('report'); r.add_argument('csv'); r.add_argument('--out',default='outputs/audit_report.json'); r.add_argument('--html',default=None,help='Optional standalone HTML report path')
    args=p.parse_args()
    if args.command=='dictionary': out={'words':variants(args.seed,args.limit)}
    elif args.command=='analyze':
        import getpass
        out=analyze(args.password if args.password is not None else getpass.getpass('Disposable sample password: '))
    elif args.command=='inspect': out=inspect_hash(args.sample)
    elif args.command=='fixture': out={'accounts':inspect_shadow_fixture(args.path)}
    elif args.command=='simulate': out=simulate(args.target,variants(args.seed),args.max_attempts)
    elif args.command=='estimate': out=estimate(args.length,args.alphabet_size,args.guesses_per_second)
    else:
        rows=audit_csv(args.csv)
        out={'scope':'Synthetic, disposable lab samples only','sample_count':len(rows),
             'weak_count':sum(x['rating']=='weak' for x in rows),'results':rows,
             'recommendations':['Use long unique passwords and a password manager',
                                'Require MFA for important accounts','Rate limit online sign-in attempts',
                                'Store passwords with salted adaptive hashes such as Argon2id']}
        path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
        print(f'Report saved: {path}')
        if args.html:
            page=Path(args.html);page.parent.mkdir(parents=True,exist_ok=True)
            page.write_text(report_html(out),encoding='utf-8')
            print(f'HTML report saved: {page}')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    try: main()
    except (ValueError,OSError) as exc:
        raise SystemExit(f'Error: {exc}')
