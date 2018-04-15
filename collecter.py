#!/usr/local/bin/python3

import sys
import urllib.request
import urllib.parse
import json
import http.cookiejar
import ssl
import config

#Set-Cookie: STAREIG=050e9c6dee6f7f798536aa357967f77b78b3bce1; Path=/
cookies = {
    '_ga':'GA1.2.458867458.1518151427',
    '_ntes_nnid':'be9c2e14e0700f538ce3d9bb71413349,1521724353346',
    '_ntes_nuid':'be9c2e14e0700f538ce3d9bb71413349',
    '_ngd_tid':'TYfVXzMwZrx6Obu5ap9MHaQdfeMtnJbE',
    # session
    #'NTES_YD_SESS':'the session cookie',
    }
host = 'https://star.8.163.com'
user_agent = 'Mozilla/5.0 (Linux; Android 8.0.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv)'


def collect_star_coins(person, session):
    cookie_header = ''
    context = ssl.SSLContext()
    cookiejar = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookiejar)
    https_handler = urllib.request.HTTPSHandler(context=context)
    opener = urllib.request.build_opener(https_handler)
    # check in
    # req = urllib.request.Request(host +'/api/starUser/checkIn',
    #                              data=json.dumps(form_data).encode(),
    #                              method='POST')
    # req.add_header('Content-Type', 'application/json;charset=UTF-8')
    # req.add_header('user-agent', 'okhttp/3.9.1')
    # resp = opener.open(req)
    # content = resp.read().decode()
    # print('登录成功')

    # get cookie
    # req = urllib.request.Request(host + '/api/starUser/getCookie' , data=json.dumps(form_data).encode(),
    #                              method='POST')
    # req.add_header('user-agent', user_agent)
    # req.add_header('Content-Type', 'application/json;charset=UTF-8')
    # resp = opener.open(req)
    # content = resp.read().decode()
    # print(content)

    # # update app and get cookie
    # req = urllib.request.Request(host + '/api/home/updateApp', data=json.dumps(form_data).encode(),
    #                              method='POST')
    # req.add_header('user-agent', user_agent)
    # req.add_header('cookie', '{}={}'.format('_gat', cookies['_gat']))
    # resp = opener.open(req)
    # content = resp.read().decode()
    # print('update app success')
    
    # get home
    req = urllib.request.Request(host + '/api/home/index', method='POST')
    req.add_header('user-agent', user_agent)

    cookies['NTES_YD_SESS'] = session
    for name, val in cookies.items():
        cookie_header += '{}={}; '.format(name, val)
    req.add_header('Cookie', cookie_header)

    resp = opener.open(req)
    content = resp.read().decode()
    print(content)
    json_data = json.loads(content)
    if json_data['code'] == 200:
        data = json_data['data']
        collect_coin_list = data['collectCoins']
        collect_count = 0
        for collect_coin in collect_coin_list:
            form_data = {'id': collect_coin['id']}
            req = urllib.request.Request(host + '/api/starUserCoin/collectUserCoin',
                                        data=json.dumps(form_data).encode(),
                                        method='POST')
            req.add_header('user-agent', user_agent)
            req.add_header('Cookie', cookie_header)
            req.add_header('Content-Type', 'application/json;charset=UTF-8')
            resp = opener.open(req)
            jd = json.loads(resp.read().decode())
            if jd['code'] == 200:

                collect_count += 1
            else:
                print('collect coin error')
        print('collect coin {} of {} successful'.format(collect_count, person))
    else:
        print('error code')

if __name__ == '__main__':
    for person, session in config.sessions.items():
        collect_star_coins(person, session)
