"""Optional Tkinter desktop interface for disposable classroom inputs."""
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from suite.core import analyze, audit_csv, inspect_hash, inspect_shadow_fixture, report_html, simulate, variants

BG='#101928'; FG='#f1f5fa'; BLUE='#0a84ff'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Password Audit Suite | Lab')
        self.geometry('900x650')
        self.configure(bg=BG)
        style=ttk.Style(self);style.theme_use('clam')
        style.configure('TNotebook',background=BG)
        style.configure('TNotebook.Tab',padding=(18,9))
        self.tabs=ttk.Notebook(self);self.tabs.pack(fill='both',expand=True,padx=18,pady=18)
        self.output=tk.Text(self,bg='#1c2940',fg=FG,insertbackground=FG,font=('Consolas',11),height=10)
        self.output.pack(fill='both',expand=True,padx=18,pady=(0,18))
        self.build()

    def page(self,name):
        frame=tk.Frame(self.tabs,bg=BG);self.tabs.add(frame,text=name);return frame

    def field(self,frame,label,secret=False):
        tk.Label(frame,text=label,bg=BG,fg=FG,font=('Arial',11)).pack(anchor='w',padx=20,pady=(16,3))
        value=tk.Entry(frame,width=62,show='*' if secret else '',font=('Arial',12))
        value.pack(anchor='w',padx=20);return value

    def button(self,frame,label,action):
        tk.Button(frame,text=label,command=lambda:self.run(action),bg=BLUE,fg='white',font=('Arial',11),padx=12,pady=7).pack(anchor='w',padx=20,pady=20)

    def run(self,action):
        try:
            result=action()
            self.output.delete('1.0','end')
            self.output.insert('end',json.dumps(result,indent=2,ensure_ascii=False))
        except (ValueError,OSError) as exc:
            messagebox.showerror('Input error',str(exc))

    def build(self):
        p=self.page('Analyze')
        password=self.field(p,'Disposable sample password',True)
        def assess():
            value=password.get();password.delete(0,'end')
            return analyze(value)
        self.button(p,'Analyze sample',assess)

        p=self.page('Dictionary')
        seed=self.field(p,'Sample seed word')
        self.button(p,'Generate bounded variants',lambda:{'words':variants(seed.get(),100)})

        p=self.page('Simulate')
        target=self.field(p,'Disposable target',True)
        stem=self.field(p,'Candidate seed word')
        def check():
            value=target.get();target.delete(0,'end')
            result=simulate(value,variants(stem.get()),100)
            result.pop('candidate',None)
            return result
        self.button(p,'Run local demo',check)

        p=self.page('Inspect')
        hash_value=self.field(p,'Synthetic hash format or lock marker')
        def identify():
            value=hash_value.get();hash_value.delete(0,'end')
            return inspect_hash(value)
        self.button(p,'Identify format',identify)
        def fixture():
            path=filedialog.askopenfilename(title='Open synthetic shadow fixture')
            return {'accounts':inspect_shadow_fixture(path)} if path else {}
        self.button(p,'Open sample fixture',fixture)

        p=self.page('Audit report')
        tk.Label(p,text='Choose a CSV with label,password columns. Use disposable data only.',bg=BG,fg=FG).pack(anchor='w',padx=20,pady=18)
        def report():
            path=filedialog.askopenfilename(title='Choose lab CSV',filetypes=[('CSV','*.csv')])
            if not path:return {}
            rows=audit_csv(path)
            data={'scope':'Synthetic lab samples','sample_count':len(rows),
                  'weak_count':sum(x['rating']=='weak' for x in rows),'results':rows,
                  'recommendations':['Use unique passwords and a password manager','Enable MFA',
                                     'Rate limit online authentication','Use salted adaptive hashes for storage']}
            destination=filedialog.asksaveasfilename(title='Save redacted HTML report',defaultextension='.html')
            if destination:
                with open(destination,'w',encoding='utf-8') as output:output.write(report_html(data))
            return data
        self.button(p,'Open CSV and create report',report)

if __name__=='__main__':
    App().mainloop()
