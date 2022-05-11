from flask import Flask, request
from bs4 import BeautifulSoup
from requests import get
import re

SITE_NAME = 'https://news.ycombinator.com/'
HTTPLST =['http','https']
additions = ['gif', 'png', 'ico', 'js', 'css']
#forumparts = ['submit', 'points', 'Search:', 'parent', 'minute']
forumparts = ['Search:']
tm = '&trade;'

def tmreplace(replacetm):
    if '™' in replacetm:
        tmartefact = replacetm.replace('™', '')
        print("!!!!!!!!!!!!!!!!!!!!!", replacetm.replace('™', ''))
        return tmartefact
    else:
        return replacetm

def replacer(repl):
    templist = repl.split()
    for i, a in enumerate(templist):
        if re.search(r'\b[a-zA-ZА-Яа-я]{6}\b', a) and a not in forumparts:
            print(a)
            a=tmreplace(a)

            res = re.findall(r'\w+', a)
            print(res,'###')
            if len(res) > 1:
                if not res[0] in HTTPLST:
                    for findsix in res:
                        print(findsix,'$$$')
                        if len(findsix) == 6:
                            templist[i] = a.replace(findsix,findsix+tm)
            else:
                templist[i] = a.replace(res[0],res[0]+tm)

#            if a[len(a) - 2:] == '),':
#                templist[i] = a[:-2] + tm + '),'
#            if len(a.split('.')) > 1:
#                templist[i] = a
##            if re.search(r'\W', a[-1]):
#                symb = a[-1]
#                templist[i] = a[:-1] + tm + symb
#            if len(a.split('-')) > 1 or len(a.split('\'')) > 1:
#                templist[i] = a
#            if len(a.split('`')) > 1:
#                templist[i] = a
#            if re.search(tm, a):
#                templist[i] = a+'shit'


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
    print(soup)
    aftersoup = []
    findtoure = soup.find_all(text=re.compile(r'\b[a-zA-ZА-Яа-я]{6}\b'))
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
