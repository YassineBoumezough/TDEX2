import string

def nombremots(texte): return len(texte.split())

def _tokens(t):
    return [w.strip(string.punctuation).lower() for w in t.split() if w.strip(string.punctuation)]

def occMots(texte):
    f={}
    for w in _tokens(texte): f[w]=f.get(w,0)+1
    return f

def longueurmoyen(text):
    mots=_tokens(text)
    if not mots: return [],0,0.0
    occ=occMots(text); mx=max(occ.values()); top=[k for k,v in occ.items() if v==mx]
    return top, mx, sum(len(m) for m in mots)/len(mots)

def mots_plus_moins_utilises(t):
    occ=occMots(t)
    if not occ: return [],0,[],0
    mx, mn = max(occ.values()), min(occ.values())
    return [k for k,v in occ.items() if v==mx], mx, [k for k,v in occ.items() if v==mn], mn

def palindromes(t):
    vus=set()
    return [w for w in _tokens(t) if w not in vus and not vus.add(w) and len(w)>=2 and w==w[::-1]]

def _phrases(t):
    p,cur=[], ""
    for ch in t.strip():
        cur+=ch
        if ch in ".!?": p.append(cur.strip()); cur=""
    if cur.strip(): p.append(cur.strip())
    return p

def nombre_phrases(t): return len(_phrases(t))
def longueurs_phrases_tokens(t): return [len(_tokens(p)) for p in _phrases(t)]
def types_ponctuation_utilises(t): return sorted({ch for ch in t if ch in string.punctuation})

# --- Types de mots (heuristique simple) ---
DET={"le","la","les","un","une","des","du","de","d","au","aux","ce","cet","cette","ces","l"}
PRON={"je","tu","il","elle","on","nous","vous","ils","elles","me","te","se","moi","toi","leur"}
PREP={"a","de","dans","en","sur","sous","chez","vers","pour","par","avec","sans","entre"}
CONJ={"et","ou","mais","car","donc","ni","que","si"}

def _classe(m):
    if m.isdigit(): return "nombre"
    if m in DET or (m.endswith("'") and m[:-1] in DET): return "det"
    if m in PRON: return "pronom"
    if m in PREP: return "preposition"
    if m in CONJ: return "conjonction"
    if m.endswith(("er","ir","re","e","es","ons","ez","ent","is","it")): return "verbe"
    return "nom"

def stats_type_de_mot(t):
    toks=_tokens(t); n=len(toks) or 1; s={}
    for m in toks: c=_classe(m); s[c]=s.get(c,0)+1
    return {k:(v, round(100*v/n,2)) for k,v in s.items()}

def top10_mots(t): return sorted(occMots(t).items(), key=lambda x:(-x[1],x[0]))[:10]
def phrases_les_plus_longues(t,n=3):
    L=[(p,len(_tokens(p))) for p in _phrases(t)]
    return sorted(L, key=lambda x:(-x[1],x[0]))[:n]
def diversite_vocabulaire(t):
    toks=_tokens(t)
    return (len(set(toks))/len(toks), len(set(toks)), len(toks)) if toks else (0.0,0,0)
def patterns_repetitifs(t,n=2,seuil=2,k=10):
    toks=_tokens(t); freq={}
    for i in range(len(toks)-n+1):
        g=tuple(toks[i:i+n]); freq[g]=freq.get(g,0)+1
    rep=[(g,c) for g,c in freq.items() if c>=seuil]
    return sorted(rep,key=lambda x:(-x[1],x[0]))[:k]

if __name__=="__main__":
    with open('data.txt','rt',encoding='utf-8') as f: data=f.read()

    print(f"nombre de mots est: {nombremots(data)}")
    print("La fréquence des mots est:", occMots(data))
    top, mx, moy = longueurmoyen(data)
    print(f"Les mots les plus utilisés sont {top} utilisés {mx} fois")
    print(f"Longueur moyenne des mots: {moy:.2f}")

    plus,fmax,moins,fmin = mots_plus_moins_utilises(data)
    print(f"Mots les plus utilisés (freq={fmax}): {plus}")
    print(f"Mots les moins utilisés (freq={fmin}): {moins}")
    print("Palindromes:", palindromes(data))

    lp = longueurs_phrases_tokens(data)
    print(f"Nombre de phrases: {nombre_phrases(data)}")
    print("Longueurs des phrases:", lp, f" | moyenne={sum(lp)/len(lp):.2f}" if lp else "")
    print("Ponctuation utilisée:", types_ponctuation_utilises(data))
    print("Stats type de mot:", stats_type_de_mot(data))

    print("Top 10 des mots:", top10_mots(data))
    print("Phrases les plus longues:", [(p[:80]+"…",n) if len(p)>80 else (p,n) for p,n in phrases_les_plus_longues(data)])
    ttr,u,tot = diversite_vocabulaire(data)
    print(f"Diversité vocabulaire (TTR)={ttr:.3f} (unique={u}, total={tot})")
    print("Bigrams répétés:", [" ".join(g)+f" ({c})" for g,c in patterns_repetitifs(data,2,2)])
    print("Trigrams répétés:", [" ".join(g)+f" ({c})" for g,c in patterns_repetitifs(data,3,2)])
