#!/usr/bin/env python3
import base64,os,re,zlib,sys,subprocess,time,marshal,hashlib
try:
    from Crypto.Cipher import AES,DES,ARC4
    from Crypto.Util.Padding import unpad
    _X=True
except:
    _X=False

def _b64(x):
    try:return base64.b64decode(x.strip()+'='*(4-len(x.strip())%4)if len(x.strip())%4 else x.strip()).decode('utf-8',errors='ignore')
    except:return None
def _b64r(x):
    try:return base64.b64decode((x[::-1]+'='*(4-len(x)%4)if len(x)%4 else x[::-1])).decode('utf-8',errors='ignore')
    except:return None
def _zr(x):
    try:return zlib.decompress(base64.b64decode((x[::-1]+'='*(4-len(x)%4)if len(x)%4 else x[::-1]))).decode('utf-8',errors='ignore')
    except:return None
def _zlib(x):
    try:return zlib.decompress(base64.b64decode(x+'='*(4-len(x)%4)if len(x)%4 else x)).decode('utf-8',errors='ignore')
    except:return None
def _hex(x):
    try:return bytes.fromhex(x).decode('utf-8',errors='ignore')
    except:return None
def _marshal(x):
    try:
        m=re.search(r"marshal\.loads\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)",x)
        if m:return marshal.loads(base64.b64decode(m.group(1)))
    except:pass
    return None
def _comp(x):
    try:
        m=re.search(r"eval\(compile\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\),.*?\)",x,re.DOTALL)
        if m:return base64.b64decode(m.group(1)).decode('utf-8',errors='ignore')
    except:pass
    return None
def _built(x):
    try:
        m=re.search(r"__import__\(['\"]builtins['\"]\)\.exec\(['\"]([^'\"]+)['\"]\)",x)
        if m:return m.group(1)
    except:pass
    return None
def _emoji(x):
    try:
        m=re.search(r'for x in\s*["\']([^"\']+)["\']',x)
        if not m:return None
        s=m.group(1)
        mp={':D':1,':P':2,':S':3,':(':4,'=)':5,'=/':6,':/':7,':{':8,';)':9,':)':0}
        mm=re.search(r'\{([^}]+)\}',x)
        if mm:
            ps=re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*(\d+)",mm.group(1))
            if ps:mp={k:int(v)for k,v in ps}
        parts=s.split('  ')
        r=[]
        for p in parts:
            if not p.strip():continue
            es=p.split()
            ns=''.join(str(mp[e])for e in es if e in mp)
            if ns:
                try:r.append(chr(int(ns)))
                except:pass
        d=''.join(r)
        if d and len(d)>5:return d
    except:pass
    return None
def _aes(x):
    if not _X:return None
    try:
        m=re.search(r"AES\.new\(b['\"]([a-fA-F0-9]+)['\"],\s*AES\.MODE_CBC,\s*b['\"]([a-fA-F0-9]+)['\"]\)\.decrypt\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)",x)
        if m:
            k,iv,ct=bytes.fromhex(m.group(1)),bytes.fromhex(m.group(2)),base64.b64decode(m.group(3))
            return unpad(AES.new(k,AES.MODE_CBC,iv).decrypt(ct),AES.block_size).decode('utf-8',errors='ignore')
    except:pass
    return None
def _des(x):
    if not _X:return None
    try:
        m=re.search(r"DES\.new\(b['\"]([a-fA-F0-9]+)['\"],\s*DES\.MODE_CBC,\s*b['\"]([a-fA-F0-9]+)['\"]\)\.decrypt\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)",x)
        if m:
            k,iv,ct=bytes.fromhex(m.group(1)),bytes.fromhex(m.group(2)),base64.b64decode(m.group(3))
            return unpad(DES.new(k,DES.MODE_CBC,iv).decrypt(ct),DES.block_size).decode('utf-8',errors='ignore')
    except:pass
    return None
def _rc4(x):
    if not _X:return None
    try:
        m=re.search(r"ARC4\.new\(b['\"]([a-fA-F0-9]+)['\"]\)\.decrypt\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)",x)
        if m:return ARC4.new(bytes.fromhex(m.group(1))).decrypt(base64.b64decode(m.group(2))).decode('utf-8',errors='ignore')
    except:pass
    return None
def _xor(x):
    try:
        m=re.search(r"bytes\(\[ord\(c\)\s*\^\s*(\d+)\s*for\s+c\s+in\s+base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)\.decode\(\)\]\)",x)
        if m:
            k=int(m.group(1))
            return''.join(chr(ord(c)^k)for c in base64.b64decode(m.group(2)).decode())
    except:pass
    return None
def _caesar(x):
    try:
        m=re.search(r"['\"]([a-zA-Z]{10,})['\"]",x)
        if m:
            enc=m.group(1)
            for s in range(1,26):
                dec=''.join(chr((ord(c)-ord('a')-s)%26+ord('a'))if c.islower()else chr((ord(c)-ord('A')-s)%26+ord('A'))if c.isupper()else c for c in enc)
                if any(k in dec for k in['import','def ','print','class']):return dec
    except:pass
    return None
def _unb(fp):
    try:
        with open(fp,'r',errors='ignore')as f:d=f.read()
        s1=re.search(r"if self.(.+?) in open",d).group(1)
        s1s=s1.replace("15","12")
        s2=re.findall(r"{(.+?)}",d)
        src=d.replace(s1,s1s).replace("{"+s2[0]+"}","print").replace(",{"+s2[1]+"}()","")
        with open('__tmp_decode.py','w')as f:f.write(src)
        r=subprocess.run(["python3","__tmp_decode.py"],capture_output=True,text=True)
        os.unlink('__tmp_decode.py')
        return r.stdout if r.stdout else None
    except:return None
def _pln(x):
    if not x or len(x)<50:return False
    pi=['import ','from ','def ','class ','if __name__','print(','return ','True','False','None','os.','sys.','requests.']
    op=[r"exec\(\(_\)\(b'",r"exec\(_\(b'",r"_ = lambda __ :",r"b'[A-Za-z0-9+/=]{30,}'",r"_sparkle",r"base64\.b64decode",r"zlib\.decompress",r"lambda __ : __import__",r"codecs\.decode",r"marshal\.loads",r"compile\(.*?eval",r"AES\.new",r"ARC4\.new",r":D :P",r":\) :\("]
    hp=any(i in x for i in pi)
    ho=any(re.search(p,x)for p in op)
    ls=x.split('\n')
    hs=any(l.strip().startswith(('import','from','def','class'))for l in ls[:20])
    return(hp or hs)and not ho
def _rec(x,d=0,silent=True):
    ls=[]
    c=x
    while d<50:
        if _pln(c):
            if not silent:print(f"\033[92m[+]\033[0m Plain text at layer {d}")
            break
        dec=None;mt=None
        for fn,nm in[(_emoji,"emoji"),(_marshal,"marshal"),(_comp,"compile+eval"),(_built,"builtins_exec"),(_aes,"AES"),(_des,"DES"),(_rc4,"RC4"),(_xor,"XOR"),(_caesar,"caesar")]:
            if not dec:
                t=fn(c)
                if t:dec,mt=t,nm
        if not dec and'_ = lambda __ : __import__'in c and'zlib'in c:
            m=re.search(r"b'([A-Za-z0-9+/=]+)'",c)
            if m:
                t=_zr(m.group(1))
                if t:dec,mt=t,"lambda+zlib+rev"
        if not dec:
            m=re.search(r"exec\(zlib\.decompress\(base64\.b64decode\(['\"]{1,3}([A-Za-z0-9+/=]+)['\"]{1,3}\)\)\)",c,re.DOTALL)
            if m:
                t=_zlib(m.group(1))
                if t:dec,mt=t,"exec+zlib"
        if not dec:
            m=re.search(r"exec\(\(_\)\(b['\"]([A-Za-z0-9+/=]+)['\"]\)",c)
            if m:
                t=_zr(m.group(1))
                if not t:t=_b64r(m.group(1))
                if t:dec,mt=t,"lambda+b64+rev"
        if not dec and'codecs.decode'in c:
            m=re.search(r"codecs\.decode\(b'([a-fA-F0-9]+)'",c)
            if m:
                t=_hex(m.group(1))
                if t:dec,mt=t,"hex+codecs"
        if not dec and'Berserker'in c and'_sparkle'in c:
            tf=f'__tmp_{d}.py'
            with open(tf,'w')as f:f.write(c)
            r=_unb(tf)
            os.unlink(tf)
            if r:dec,mt=r,"unberserker"
        if not dec:
            m=re.search(r"b'([A-Za-z0-9+/=]{30,})'",c)
            if m:
                t=_zr(m.group(1))
                if not t:t=_b64r(m.group(1))
                if t:dec,mt=t,"zlib/b64+rev"
        if not dec and'base64.b64decode'in c and'zlib.decompress'in c:
            m=re.search(r"b64decode\(['\"]{1,3}([A-Za-z0-9+/=]+)['\"]{1,3}",c)
            if m:
                t=_zlib(m.group(1))
                if t:dec,mt=t,"b64+zlib"
        if not dec:break
        ls.append({'d':d,'m':mt,'l':len(dec)})
        if not silent:print(f"\033[93m[Layer {d}]\033[0m {mt} -> {len(dec)} chars")
        c=dec;d+=1
    return c,ls

def _menu():
    print("""
\033[96m╔══════════════════════════════════════════╗
║   AUTO DECRYPTOOL BY B3RT1337            ║
║   OFFICIAL ON GITHUB: B3RT1337/DECRYPTOOL║
╚══════════════════════════════════════════╝\033[0m
\033[97m1.\033[0m Decrypt file
\033[97m2.\033[0m Decrypt from text (paste)
\033[97m3.\033[0m Exit""")

if __name__=='__main__':
    if len(sys.argv)>1:
        if sys.argv[1]=='-p':
            d=sys.stdin.read().strip()
            if d:r,_=_rec(d,silent=False);sys.stdout.write(r)
            sys.exit(0)
        fp=sys.argv[2]if sys.argv[1]=='-f'and len(sys.argv)>2 else sys.argv[1]
        if not os.path.exists(fp):
            print(f"\033[91m[-]\033[0m File not found: {fp}")
            sys.exit(1)
        r,ls,_=_rec(open(fp,'r',errors='ignore').read(),silent=False)
        print(f"\n\033[92m[+]\033[0m Layers: {len(ls)}")
        for l in ls:print(f"    \033[93mLayer {l['d']}\033[0m: {l['m']} ({l['l']} chars)")
        print(f"\n\033[96m{'='*55}\033[0m")
        sys.stdout.write(r)
        sys.exit(0)
    
    while True:
        _menu()
        c=input("\n\033[97mSelect:\033[0m ").strip()
        
        if c=='3':
            print("\033[91m[+]\033[0m Bye.")
            break
        
        if c=='1':
            fp=input("\033[97mFile path:\033[0m ").strip()
            if not os.path.exists(fp):
                print(f"\033[91m[-]\033[0m File not found: {fp}")
                continue
            content=open(fp,'r',errors='ignore').read()
            print(f"\033[96m[+]\033[0m File: {fp} ({len(content)} chars)\033[96m[+]\033[0m Decrypting...")
            
        elif c=='2':
            print("\033[97mPaste encoded text (Ctrl+D when done):\033[0m")
            content=sys.stdin.read().strip()
            if not content:
                print("\033[91m[-]\033[0m No input")
                continue
            print(f"\033[96m[+]\033[0m Input: {len(content)} chars\033[96m[+]\033[0m Decrypting...")
        else:
            print("\033[91m[-]\033[0m Invalid choice")
            continue
        
        time.sleep(0.3)
        r,ls=_rec(content,silent=False)
        
        print(f"\n\033[92m[+]\033[0m Total layers decoded: {len(ls)}")
        if ls:
            for l in ls:print(f"    \033[93mLayer {l['d']}\033[0m: {l['m']} ({l['l']} chars)")
        
        print(f"\n\033[96m{'='*55}\033[0m")
        print(f"\033[97mDECRYPTED OUTPUT:\033[0m")
        print(f"\033[96m{'='*55}\033[0m")
        
        if len(r)>2000:
            print(r[:2000])
            print(f"\n\033[93m... (truncated, {len(r)} total chars)\033[0m")
        else:
            print(r)
        
        sv=input(f"\n\033[97mSave to file? (y/n):\033[0m ").strip().lower()
        if sv=='y':
            out=input("\033[97mOutput filename:\033[0m ").strip()
            with open(out,'w')as f:f.write(r)
            print(f"\033[92m[+]\033[0m Saved to {out}")
        
        input(f"\n\033[90mPress Enter to continue...\033[0m")
