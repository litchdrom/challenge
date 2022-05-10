from flask import Flask,request,redirect,Response
from bs4 import BeautifulSoup
from requests import get
import re


additions=['gif','png','ico','js','css']
forumparts=['submit','points','Search:']

def replacer(repl):
    print(repl)
    templist=repl.split()
    for i,a in enumerate(templist):
        if re.search(r'\b[a-zA-Z]{6}\b',a):
            if a not in forumparts:
                templist[i]=a+'&trade;'
                if a[-1]==')':
                    templist[i]=a[:-1]+'&trade;)'
    listtostr=' '.join(map(str, templist))
    return listtostr


def switcher(spath):
#        findf=spath
        findf=spath.split(".")
        if len(findf) > 1:
            if findf[-1] in additions:
                return None
        else:
            return spath
    


app = Flask('__main__')
SITE_NAME = 'https://news.ycombinator.com/'
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    if f'{path}'=='item':
#    if request.args:
        print('request_args',request.args)
        print('item')
        print('path is', path)
        print('request arg is',request.args.get('id'))
        return get(f'{SITE_NAME}{path}'+'?id='+request.args.get('id')).content
    if request.method=='GET':
        print('GET')
        print('path is', path)
        print('method is',request.method)
        print('request is',request.data)
        print('request arg is',request.args)
        print('url is ',f'{SITE_NAME}{path}','file is',f'{path}')
#        findfiles=(f'{path}')
#        findfiles=findfiles.split(".")
        sw=switchder(f'{path}')
        if sw == f'{path}':
       #     if findfiles[-1] in additions:
            #    pass
            pass
        else:
            mad=get(f'{SITE_NAME}{path}').text
            soup = BeautifulSoup(mad, 'lxml')
         #   print(soup.text)
            fixed_comments = []
            #findtoure = soup.find_all(text = re.compile(r'^[a-zA-Z]{6}$'))
            #findtoure = soup.find_all(text = re.compile(r'\s|^[a-zA-Z]{6}\s|$'))
            findtoure = soup.find_all(text = re.compile(r'\b[a-zA-Z]{6}\b'))
            for tmword in findtoure:

                fixed_text = replacer(tmword)
                #fixed_text = tmword.replace(tmword,tmword+'666')
                tmword.replace_with(fixed_text)
                print('replace this -',tmword,'on this', fixed_text)
                fixed_comments.append(fixed_text)
       #     print(soup)
            print(type(get(f'{SITE_NAME}{path}').content))
    #        soupb=str(soup.prettify(formatter="html"))
            soupb=str(soup.prettify(formatter=None))
#            soupb=soupb.encode('utf-8')
            print(soupb)
   #         soupb.mimetype = 'text/plain'
            return soupb

          #      print('!!!!!!!',tmword)
#            print(get(f'{SITE_NAME}{path}').text)
#            for a in mad:
#                print(a)




#        mad=get(f'{SITE_NAME}{path}').content
#        print('###############type of this',type(mad))
#        if f'{SITE_NAME}{path}' == SITE_NAME:
            #mad.decode('utf-8')
   #         soup = BeautifulSoup(request.text, 'lxml')
# #           mad.decode('')
#            for a in mad:
#            print(soup)

    return get(f'{SITE_NAME}{path}').content
#    print(response.get_data())

app.run(host='0.0.0.0', port=8080)
