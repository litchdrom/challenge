from flask import Flask, request
from bs4 import BeautifulSoup
from requests import get
import re

SITE_NAME = 'https://news.ycombinator.com/'
additions = ['gif', 'png', 'ico', 'js', 'css']
forumparts = ['submit', 'points', 'Search:', 'parent', 'minute']
tm = '&trade;'


def replacer(repl):
    templist = repl.split()
    for i, a in enumerate(templist):
        if re.search(r'\b[a-zA-Z]{6}\b', a) and a not in forumparts:
            templist[i] = a + tm
            if a[len(a) - 2:] == '),':
                templist[i] = a[:-2] + tm + '),'
            if len(a.split('.')) > 1:
                templist[i] = a
            if re.search(r'\W', a[-1]):
                symb = a[-1]
                templist[i] = a[:-1] + tm + symb
            if len(a.split('-')) > 1 or len(a.split('\'')) > 1:
                templist[i] = a
            if len(a.split('`')) > 1:
                templist[i] = a

    listtostr = ' '.join(map(str, templist))
    return listtostr


def switcher(spath):
    findf = spath.split(".")
    if len(findf) > 1:
        if findf[-1] in additions:
            return None
    else:
        return spath


def soupbrew(mad):
    soup = BeautifulSoup(mad, 'lxml')
    aftersoup = []
    findtoure = soup.find_all(text=re.compile(r'\b[a-zA-Z]{6}\b[^-]'))
    for tmword in findtoure:
        fixed_text = replacer(tmword)
        tmword.replace_with(fixed_text)
        aftersoup.append(fixed_text)
    soupb = str(soup.prettify(formatter=None))
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
        return get(f'{SITE_NAME}{path}' + addurl).content
    else:
        mad = get(f'{SITE_NAME}{path}' + addurl).text
        soupswitch = soupbrew(mad)
        return soupswitch


app.run(host='0.0.0.0', port=8232)
