from flask import Flask, request
from bs4 import BeautifulSoup
from requests import get
import re

SITE_NAME = 'https://news.ycombinator.com/'
HTTPLST =['http','https']
CONTENT = ['gif', 'png', 'ico', 'js', 'css']
FORUMPARTS = ['Search:']
TM = '&trade;'
SITE='https://news.ycombinator.com'

def tmreplace(replacetm):
    if '™' in replacetm:
        tmartefact = replacetm.replace('™', '')
#        print("!!!!!!!!!!!!!!!!!!!!!", replacetm.replace('™', ''))
        return tmartefact
    else:
        return replacetm

def replacer(repl):
    templist = repl.split()
    for i, a in enumerate(templist):
        if re.search(r'\b[a-zA-ZА-Яа-я]{6}\b', a) and a not in FORUMPARTS:
            a=tmreplace(a)
            res = re.findall(r'\w+', a)
            if len(res) > 1:
                if not res[0] in HTTPLST:
                    for findsix in res:
                        if len(findsix) == 6:
                            templist[i] = a.replace(findsix,findsix+TM)
            else:
                templist[i] = a.replace(res[0],res[0]+TM)

    listtostr = ' '.join(map(str, templist))
    return listtostr

def switcher(spath):
    findf = spath.split(".")
    if len(findf) > 1:
        if findf[-1] in CONTENT:
            return None
    else:
        return spath


def soupbrew(mad):
    soup = BeautifulSoup(mad, 'lxml')
    soupu = BeautifulSoup(mad, 'html.parser')
    aftersoup = []
    tempurl = ''
    findtoure = soup.find_all(text=re.compile(r'\b[a-zA-ZА-Яа-я]{6}\b'))
    for tmword in findtoure:
        fixed_text = replacer(tmword)
        tmword.replace_with(fixed_text)
        aftersoup.append(fixed_text)
    soupb = str(soup.prettify(formatter=None))

    soupu = BeautifulSoup(soupb, 'html.parser')
    findurll = soupu.find_all('a', href=True)
    for turl in findurll:
        if SITE in turl['href']:
            turl['href'] = request.base_url
    findurll = str(soupu.prettify(formatter=None))
    return findurll


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
        htanswer=get(f'{SITE_NAME}{path}' + addurl).status_code
        return mad,htanswer
    else:
        mad = get(f'{SITE_NAME}{path}' + addurl).text
        htanswer = get(f'{SITE_NAME}{path}' + addurl).status_code
        soupswitch = soupbrew(mad)

        return soupswitch, htanswer


app.run(host='0.0.0.0', port=8232)
