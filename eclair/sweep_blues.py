# eclAIr's Bigcapital theme: Bigcapital's brand blues, written straight into its style files and a few components, become eclAIr's
# ink (dark and mid blues) or line tone (pale blues), so no blue is left to read as someone else's brand. Re-run after an update.
#   python3 sweep_blues.py <path to packages/webapp>
import re, sys, os, colorsys
root = sys.argv[1] + '/src'
HEX = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
def blue(h):
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return 190 <= hh * 360 <= 265 and s > 0.35 and 0.08 < l < 0.97, l
changed = 0
for d, _, fs in os.walk(root):
    if '/style/eclair' in d: continue
    for f in fs:
        p = os.path.join(d, f)
        if f == '_variables.scss': continue
        if not (f.endswith('.scss') or f.endswith('.tsx') or f.endswith('.ts')): continue
        s = open(p).read()
        def sub(m):
            global changed
            is_blue, l = blue(m.group(1))
            if not is_blue: return m.group(0)
            if f.endswith('.tsx') or f.endswith('.ts'):
                # only inside string literals that are clearly colours
                return m.group(0)
            changed += 1
            return 'var(--e-line)' if l > 0.75 else 'var(--e-ink)'
        # a Sass variable or a colour function needs a real colour, so those lines keep theirs
        t = '\n'.join(l if re.match(r'\s*\$', l) or re.search(r'(darken|lighten|rgba|mix|transparentize|fade-out|fade-in|adjust-hue|saturate|desaturate)\(', l) else HEX.sub(sub, l) for l in s.split('\n'))
        if f.endswith(('.tsx', '.ts')):
            for k in ('#0052cc', '#0052CC', '#0069ff', '#0066ff'):
                if k in t: changed += t.count(k); t = t.replace(k, 'var(--e-ink)')
        if t != s: open(p, 'w').write(t)
print('blues swept:', changed)
