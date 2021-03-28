from flask import Flask, render_template, request
import pickle

model = pickle.load(open('final_model', 'rb'))
feature_scaler = pickle.load(open('feature_scaler', 'rb'))
print("***********I am loading initially only**********")

app = Flask(__name__)

common_tlds = ["com", "org", "net", "int", "edu", "gov", "mil"]
common_ctlds = ['.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.ao',
       '.ar', '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb',
       '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bm', '.bn',
       '.bo', '.br', '.bs', '.bt', '.bv', '.bw', '.by', '.bz', '.ca',
       '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm',
       '.cn', '.co', '.cr', '.cu', '.cv', '.cw', '.cx', '.cy', '.cz',
       '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.ee', '.eg',
       '.er', '.es', '.et', '.eu', '.fi', '.fj', '.fk', '.fm', '.fo',
       '.fr', '.ga', '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi',
       '.gl', '.gm', '.gn', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu',
       '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.id',
       '.ie', '.il', '.im', '.in', '.io', '.iq', '.ir', '.is', '.it',
       '.je', '.jm', '.jo', '.jp', '.ke', '.kg', '.kh', '.ki', '.km',
       '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc',
       '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma',
       '.mc', '.md', '.me', '.mg', '.mh', '.mk', '.ml', '.mm', '.mn',
       '.mo', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw',
       '.mx', '.my', '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni',
       '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.pa', '.pe',
       '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps',
       '.pt', '.pw', '.py', '.qa', '.re', '.ro', '.rs', '.ru', '.rw',
       '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj',
       '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.st', '.su', '.sv',
       '.sx', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj',
       '.tk', '.tl', '.tm', '.tn', '.to', '.tr', '.tt', '.tv', '.tw',
       '.tz', '.ua', '.ug', '.uk', '.us', '.uy', '.uz', '.va', '.vc',
       '.ve', '.vg', '.vi', '.vn', '.vu', '.wf', '.ws', '.ye', '.yt',
       '.za', '.zm', '.zw']

def generate_features_from_url(url):
    X = []

    https_token = 0
    if "http://" == url[0:7] :
        url = url[7:]
    if "https://" == url[0:8] :
        https_token = 1
        url = url[8:]

    url_len = len(url)
    X.append(url_len)

    temp = url.split("/", 1)
    host = temp[0]
    path = None
    if len(temp) == 2:
        path = temp[1]

    host_len = len(host)
    X.append(host_len)

    no_dots = 0
    no_hypens = 0
    no_at = 0
    no_qm = 0
    no_and = 0
    no_or = 0
    no_eq = 0
    no_plus = 0
    no_underscore = 0
    no_tilde = 0
    no_percent = 0
    no_slash = 0
    no_star = 0
    no_colon = 0
    no_comma = 0
    no_semicolon = 0
    no_dollar = 0
    no_space = 0
    no_digit = 0
    no_alphabet = 0

    for x in url:
        if x == '.':
            no_dots += 1 
        if x == '-':
            no_hypens += 1 
        if x == '@':
            no_at += 1 
        if x == '?':
            no_qm += 1 
        if x == '&':
            no_and += 1 
        if x == '|':
            no_or += 1 
        if x == '=':
            no_eq += 1 
        if x == '+':
            no_plus += 1 
        if x == '_':
            no_underscore += 1 
        if x == '~':
            no_tilde += 1 
        if x == '%':
            no_percent += 1 
        if x == '/':
            no_slash += 1 
        if x == '*':
            no_star += 1 
        if x == ':':
            no_colon += 1 
        if x == ',':
            no_comma += 1 
        if x == ';':
            no_semicolon += 1 
        if x == '$':
            no_dollar += 1 
        if x == ' ':
            no_space += 1
        if (x >= '0' and x <= '9'):
            no_digit += 1
        if((x >= 'a' and x <= 'z') or (x >= 'A' and x <= 'Z')):
            no_alphabet += 1

    X.append(no_dots)
    X.append(no_hypens)
    X.append(no_at)
    X.append(no_qm)
    X.append(no_and)
    X.append(no_or)
    X.append(no_eq)
    X.append(no_plus)
    X.append(no_underscore)
    X.append(no_tilde)
    X.append(no_percent)
    X.append(no_slash)
    X.append(no_star)
    X.append(no_colon)
    X.append(no_comma)
    X.append(no_semicolon)
    X.append(no_dollar)
    X.append(no_space)

    X.append(url.count("www."))
    X.append(url.count(".com"))
    X.append(url.count("//"))

    url_digit_ratio = no_digit/url_len
    url_alphabet_ratio = no_alphabet/url_len
    url_sp_char_ratio = (url_len - no_digit - no_alphabet)/url_len
    X.append(url_digit_ratio)
    X.append(url_alphabet_ratio)
    X.append(url_sp_char_ratio)

    port = ""
    port_flag = 0
    temp = host.split(":")
    if temp[0] != host and temp[1].isnumeric():
        host = temp[0]
        port = temp[1]
        port_flag = 1

    host_no_digit = 0
    for x in host:
        if (x >= '0' and x <= '9'):
            host_no_digit += 1
    host_digit_ratio = host_no_digit/host_len
    X.append(host_digit_ratio)

    X.append(https_token)
    X.append(port_flag)

    ## finding if host is a ip address
    ip = 0
    if ("." in host):
        elements_array = host.strip().split(".")
        if(len(elements_array) == 4):
            for i in elements_array:
                if (i.isnumeric() and int(i)>=0 and int(i)<=255):
                    ip = 1
                else:
                    ip = 0
                    break
    X.append(ip)

    #prefix-suffix in host
    X.append(host.count("-"))

    #splitting host into subdomains
    temp = host.split(".")
    no_subdomains = len(temp)    
    X.append(no_subdomains)

    #suspecious tld
    suspecious_tld = 1
    tld = temp[len(temp) - 1]
    if tld in common_ctlds:
        tld = temp[len(temp) - 2]
        if tld in common_tlds:
            suspecious_tld = 0
    elif tld in common_tlds:
        suspecious_tld = 0
    X.append(suspecious_tld)

    #http in path
    if path is None:
        X.append(0)
    else:
        X.append(path.count("http://") + path.count("https://"))
    
    return X

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    body = request.get_json()
    url = body["url"]
    features = generate_features_from_url(url)
    features = feature_scaler.transform([features])
    pred = model.predict(features)
    if pred == 0:
        return ({
            "judge": "Legitimate"
        })
    elif pred == 1:
        return ({
            "judge": "Phishing"
        })
    else:
        return ({
            "judge": "Error"
        })

if __name__ == '__main__':
    app.run(debug=True)