# eclAIr's Bigcapital theme (Keith, 3 Nov 2026): maps every colour variable in Bigcapital's _variables.scss to eclAIr's tokens by role,
# day and night, and writes src/style/eclair/_tokens.scss. Run again after a Bigcapital update.
#   python3 map_tokens.py <path to packages/webapp>
import re, sys, colorsys
root = sys.argv[1]
src = open(f'{root}/src/style/_variables.scss').read()
DAY = dict(paper='#fafaf8', card='#fefefe', ink='#1a1a1a', body='#333333', mute='#696969', rule='#e0e0dc', line='#c7c5bd',
           watch='#73879f', needed='#c06a3e', handled='#5a8a7a', needed_text='#9d5733', handled_text='#4a7164', watch_text='#5b6b7e')
NIGHT = dict(paper='#1d1c19', card='#25241f', ink='#ecebe5', body='#c9c7bf', mute='#a39f95', rule='#3a3832', line='#5c5950',
             watch='#a7b9cf', needed='#e0895c', handled='#7fae9e', needed_text='#e0895c', handled_text='#7fae9e', watch_text='#a7b9cf')
def parse(v):
    v = v.strip()
    m = re.fullmatch(r'#([0-9a-fA-F]{3,8})', v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4): h = ''.join(c * 2 for c in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)), a
    m = re.fullmatch(r'rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)', v)
    if m: return tuple(int(float(m.group(i))) for i in (1, 2, 3)), float(m.group(4) or 1)
    if v in ('#fff', 'white'): return (255, 255, 255), 1
    if v in ('#000', 'black'): return (0, 0, 0), 1
    return None
def hexa(t):
    return '#%02x%02x%02x' % t
def rgba(hx, a):
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    return hx if a >= 0.999 else f'rgba({r}, {g}, {b}, {a:.2f})'
def role(name, rgb, a, P, night):
    n = name.lower()
    r, g, b = (c / 255 for c in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    sat = s if 0.05 < l < 0.95 else 0
    # the sidebar: paper with ink words, never a dark navy band
    if 'sidebar' in n and 'overlay-backdrop' not in n:
        if 'background' in n or n.endswith('-focus-background'):
            if 'hover' in n or 'active' in n or 'focus' in n: return P['rule'] if not night else P['rule']
            return P['card']
        if 'scrollbar' in n: return P['line']
        if 'label' in n or 'toggle' in n: return P['mute']
        if 'border' in n or 'divider' in n: return P['rule']
        return P['ink']
    if sat > 0.25:
        hue = h * 360
        textish = 'text' in n or 'color' in n and 'background' not in n
        if hue < 15 or hue >= 330:  # red: no red as a signal
            if 'background' in n and l > 0.85: return P['card']
            return P['needed_text'] if textish else P['needed']
        if 15 <= hue < 55: return P['needed_text'] if textish else P['needed']      # orange and amber: needed
        if 75 <= hue < 170:  # green: handled
            if 'background' in n and l > 0.85: return P['card']
            return P['handled_text'] if textish else P['handled']
        # blues and purples, Bigcapital's brand: ink; pale blue fills become paper
        if 'background' in n and l > 0.8: return P['paper']
        if 'border' in n and l > 0.6: return P['line']
        return P['ink']
    # greys, by lightness, to the nearest eclAIr tone of the same job
    order = ['card', 'paper', 'rule', 'line', 'mute', 'body', 'ink'] if not night else ['ink', 'body', 'mute', 'line', 'rule', 'card', 'paper']
    tones = [(k, colorsys.rgb_to_hls(*(int(P[k][i:i + 2], 16) / 255 for i in (1, 3, 5)))[1]) for k in order]
    if night:  # night keeps the role: a light text stays light, a dark background stays dark
        pass
    best = min(tones, key=lambda t: abs(t[1] - l))[0]
    return P[best]
def block(sel_body, P, night):
    out = []
    for m in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+);', sel_body):
        name, val = m.group(1), m.group(2).strip()
        if 'var(' in val or 'gradient' in val: continue
        p = parse(val)
        if not p: continue
        rgb, a = p
        out.append(f'  {name}: {rgba(role(name, rgb, a, P, night), a)};')
    return out
day_body = src[src.index(':root {'):src.index('}', src.index(':root {'))]
i = src.index('body.bp4-dark'); night_body = src[i:src.index('\n}', i)]
day, night = block(day_body, DAY, False), block(night_body, NIGHT, True)
open(f'{root}/src/style/eclair/_tokens.scss', 'w').write(
    "// eclAIr's tokens over Bigcapital's colour variables, by role (written by eclair/map_tokens.py; run it again after an update).\n"
    "// Greys to the nearest eclAIr tone, reds to the deeper orange (no red), greens to sage, oranges to orange, blues to ink,\n"
    "// the sidebar to paper with ink words.\n"
    "html:root {\n" + '\n'.join(day) + "\n}\n\nhtml body.bp4-dark {\n" + '\n'.join(night) + "\n}\n")
print('day', len(day), 'night', len(night))
