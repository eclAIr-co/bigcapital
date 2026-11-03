# eclAIr's wording over Bigcapital's English (Keith, 3 Nov 2026, route 2): writes src/lang/en/index.json in eclAIr's voice.
# Plain names for the main screens, sentence case for labels, no exclamation marks, short confirmations. Re-run after an update.
#   python3 word_pass.py <path to packages/webapp>
import json, re, sys
p = sys.argv[1] + '/src/lang/en/index.json'
d = json.load(open(p))
NAMES = {  # eclAIr's names, by key
    'accounts_chart': 'Chart of accounts', 'manual_journals': 'Journal entries', 'resource_manual_journal_plural': 'Journal entries',
    'profit_loss_sheet': 'Profit and loss', 'homepage': 'Home', 'sales_inventory': 'Sales and inventory', 'financial': 'Accounting',
    'back_to_list': 'Back to the list', 'there_is_no_results_in_the_table': 'Nothing here yet.', 'accounting_basis': 'Basis:',
    'customize_report': 'Change the report', 'table_views': 'Views', 'quick_new': 'New',
}
KEEP = {'VAT', 'USD', 'PDF', 'CSV', 'XLSX', 'A/R', 'A/P', 'ID', 'SKU', 'UPC', 'API', 'URL', 'SMS', 'GST', 'TIN', 'EIN', 'FAQ', 'IBAN',
        'Bigcapital', 'Stripe', 'Plaid', 'Lemon', 'Squeezy', 'Excel', 'Google', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday', 'I', 'eclAIr'}
def sentence(v):
    words = v.split(' ')
    if len(words) < 2 or len(words) > 6: return v
    caps = [w for w in words if w[:1].isupper()]
    if len(caps) < 2 or not all(w[:1].isupper() or not w[:1].isalpha() or w.lower() in ('a', 'an', 'and', 'as', 'of', 'to', 'the', 'in', 'on', 'for', 'or', 'by', 'with', '&') for w in words): return v
    out = [words[0]]
    for w in words[1:]:
        core = re.sub(r'[^A-Za-z/]', '', w)
        out.append(w if core in KEEP or (core.isupper() and len(core) > 1) else w[:1].lower() + w[1:])
    return ' '.join(out)
def done_line(v):
    # "The invoice has been created successfully." -> "Invoice created."
    m = re.fullmatch(r'(?:The |the )?(.+?) (?:has|have) been (\w+)(?: successfully)?\.?', v.strip())
    if m and 'successfully' in v: return m.group(1)[:1].upper() + m.group(1)[1:] + ' ' + m.group(2) + '.'
    return re.sub(r'\s*successfully', '', v)
n = 0
for k, v in list(d.items()):
    if not isinstance(v, str): continue
    w = NAMES.get(k, v)
    if k not in NAMES:
        w = done_line(w) if 'successfully' in w.lower() else w
        w = re.sub(r'!+\.?', '.', w)
        w = sentence(w)
    if w != v: d[k] = w; n += 1
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2)
print('lines reworded:', n)
