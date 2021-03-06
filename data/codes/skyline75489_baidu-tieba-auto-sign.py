# -*- coding: utf-8 -*-import urllibimport urllib2import cookielibimport reimport hashlibimport jsonimport threadingimport platformimport os

def _setup_cookie(my_cookie):    cookie = cookielib.CookieJar()    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))    urllib2.install_opener(opener)    opener.addheaders = [('User-agent', 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352'),                         ('Cookie', my_cookie), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]

def _fetch_like_tieba_list(): print u'ing...' if system_env else 'ing...'    page_count = 1    find_like_tieba = [] while True:        like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_count        req = urllib2.Request(like_tieba_url)        resp = urllib2.urlopen(req).read()        resp = resp.decode('gbk').encode('utf8')        re_like_tieba = '<a href="\/f\?kw=.*?" title="(.*?)">.+?<\/a>'        temp_like_tieba = re.findall(re_like_tieba, resp) if not temp_like_tieba: break if not find_like_tieba:            find_like_tieba = temp_like_tieba else:            find_like_tieba += temp_like_tieba        page_count += 1
 return find_like_tieba

def _fetch_tieba_info(tieba):    tieba_wap_url = "http://tieba.baidu.com/mo/m?kw=" + tieba    wap_resp = urllib2.urlopen(tieba_wap_url).read()
 if not wap_resp: return    re_already_sign = '<td style="text-align:right;"><span[ ]>(.*?)<\/span><\/td><\/tr>'    already_sign = re.findall(re_already_sign, wap_resp)
    re_fid = '<input type="hidden" name="fid" value="(.+?)"\/>'    _fid = re.findall(re_fid, wap_resp)    fid = _fid and _fid[0] or None
    re_tbs = '<input type="hidden" name="tbs" value="(.+?)"\/>'    _tbs = re.findall(re_tbs, wap_resp)
    tbs = _tbs and _tbs[0] or None return already_sign, fid, tbs

def _decode_uri_post(postData): SIGN_KEY = "tiebaclient!!!"    s = ""    keys = postData.keys()    keys.sort() for i in keys:        s += i + '=' + postData[i]    sign = hashlib.md5(s + SIGN_KEY).hexdigest().upper()    postData.update({'sign': str(sign)}) return postData

def _make_sign_request(tieba, fid, tbs, BDUSS):    sign_url = 'http://c.tieba.baidu.com/c/c/forum/sign'    sign_request = {"BDUSS": BDUSS, "_client_id": "03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36", "_client_type": "4", "_client_version": "1.2.1.17", "_phone_imei": "540b43b59d21b7a4824e1fd31b08e9a6", "fid": fid, "kw": tieba, "net_type": "3", 'tbs': tbs}
    sign_request = _decode_uri_post(sign_request)    sign_request = urllib.urlencode(sign_request)
    sign_request = urllib2.Request(sign_url, sign_request)    sign_request.add_header( "Content-Type", "application/x-www-form-urlencoded") return sign_request

def _handle_response(sign_resp):    sign_resp = json.load(sign_resp)    error_code = sign_resp['error_code']    sign_bonus_point = 0 try: # Don't know why but sometimes this will trigger key error.        sign_bonus_point = int(sign_resp['user_info']['sign_bonus_point']) except KeyError: pass if error_code == '0': print u",+%d" % sign_bonus_point if system_env else ",+%d" % sign_bonus_point else:        error_msg = sign_resp['error_msg'] if error_msg == u'': print u'' if system_env else '' else: print u'' if system_env else '' print "Error:" + unicode(error_code) + " " + unicode(error_msg)

def _sign_tieba(tieba, BDUSS):    already_sign, fid, tbs = _fetch_tieba_info(tieba) if not already_sign: print tieba.decode('utf-8') + u'......' if system_env else tieba + '......' else: if already_sign[0] == "": print tieba.decode('utf-8') + u"......" if system_env else tieba + "......" return
 if not fid or not tbs: print u"" if system_env else "" return
    sign_request = _make_sign_request(tieba, fid, tbs, BDUSS)    sign_resp = urllib2.urlopen(sign_request, timeout=5)    _handle_response(sign_resp)

def sign(my_cookie, BDUSS):    _setup_cookie(my_cookie)    _like_tieba_list = _fetch_like_tieba_list() if len(_like_tieba_list) == 0: print u"CookieBDUSS" if system_env else "CookieBDUSS" return    thread_list = [] for tieba in _like_tieba_list:        t = threading.Thread(target=_sign_tieba, args=(tieba, BDUSS))        thread_list.append(t)        t.start()  for t in thread_list:        t.join(2)

def main():    my_cookie = "Cookie" BDUSS = "BDUSS"    sign(my_cookie, BDUSS)
if __name__ == "__main__":    system_env = True if platform.system()=='Windows' else False    main()    os.system("date /T >> tieba_log.log") if system_env else os.system("date >> tieba_log.log")