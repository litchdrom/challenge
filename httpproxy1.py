from flask import Flask, request
from bs4 import BeautifulSoup
from requests import get
import re

SITE_NAME = 'https://news.ycombinator.com/'
HTTPLST = ['http', 'https']
CONTENT = ['gif', 'png', 'ico', 'js', 'css']
FORUMPARTS = ['Search:']
# TM = '&trade;'
TM = u"\u2122"
SITE = 'https://news.ycombinator.com'

def replacer(repl):
    flist = re.findall(r'\w+|™', repl)
    for val in set(flist):
        valtm = val + TM
        if val == '™':
            print(val)
            repl = re.sub(val,valtm[:-2], repl, count=0, flags=0)
        if len(val) == 6:
            print(val)
            repl = re.sub(val, valtm, repl, count=0, flags=0)

    return repl


def switcher(spath):
    findf = spath.split(".")
    if len(findf) > 1:
        if findf[-1] in CONTENT:
            return None
    else:
        return spath


def soupbrew(mad):
    soupu = BeautifulSoup(mad, 'lxml')
    findurll = soupu.find_all('a', href=True)
    for turl in findurll:
        if SITE in turl['href']:
            turl['href'] = request.host_url
    soup = soupu
    findtoure = soup.find_all(text=re.compile(r'\b[a-zA-ZА-Яа-я]{6}\b'), recursive=True)
    for tmword in findtoure:
        fixed_text = replacer(tmword)
        tmword.replace_with(fixed_text)
    soupb = str(soup).encode()

    return soupb


def argfix(fix):
    argurl = ['?', ]
    if len(fix) > 0:
        i = 0
        lf = len(fix)
        for key, value in fix.items():
            i += 1
            argurl.append(key + '=' + value)
            if i < lf:
                argurl.append('&')
        fixurl = ''.join(map(str, argurl))
    else:
        fixurl = ''
    return fixurl


app = Flask('__main__')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    addurl = argfix(request.args.to_dict(flat=True))
    sw = switcher(f'{path}')
    if sw is None:
        mad = get(f'{SITE_NAME}{path}' + addurl).content
        htanswer = get(f'{SITE_NAME}{path}' + addurl).status_code
        return mad, htanswer
    else:
        mad = get(f'{SITE_NAME}{path}' + addurl).text
        htanswer = get(f'{SITE_NAME}{path}' + addurl).status_code
        soupswitch = soupbrew(mad)

        return soupswitch, htanswer


app.run(host='0.0.0.0', port=8232)
