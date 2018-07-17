import argparse
import datetime
import json
import pathlib
import requests


def log(message):
    t = datetime.datetime.utcnow()
    print('{} | {}'.format(t, message))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    return parser.parse_args()


def swag_code_box(user, code):
    url = 'http://www.swagbucks.com/'
    params = {'cmd': 'sb-gimme-jx'}
    data = {'hdnCmd': 'sb-gimme', 'pcode': code}
    cookies = {'__urqm': user.get('urqm')}
    r = requests.post(url, params=params, data=data, cookies=cookies)
    return r.json()[0]


def mobile_app(user, code):
    url = 'http://swagbucks.com/'
    params = {'cmd': 'apm-11'}
    data = {'appid': '6', 'pcode': code, 'sig': user.get('sig')}
    cookies = {'__urqm': user.get('urqm')}
    r = requests.post(url, params=params, data=data, cookies=cookies)
    return r.json()['message']


def swagbutton(user, code):
    url = 'http://www.swagbucks.com/'
    params = {'cmd': 'sb-gimme-jx', 'tbid': user.get('tbid')}
    data = {'hdnCmd': 'sb-gimme', 'pcode': code}
    cookies = {'__urqm': user.get('urqm')}
    r = requests.get(url, params=params, data=data, cookies=cookies)
    return r.json()[0]


def main():
    args = parse_args()
    log('Starting up.')
    log('Using config file at {}'.format(args.config))
    conf = {}
    conf_file = pathlib.Path(args.config).resolve()
    if not conf_file.parent.exists():
        conf_file.parent.mkdir(parents=True)
    if conf_file.exists():
        with conf_file.open() as f:
            conf = json.load(f)

    c = requests.get('http://sbcodez.com/')
    _, _, code = c.text.partition('<span class="code">')
    code, _, _ = code.partition('</span>')
    code = code.strip()

    if code == conf.get('last_code'):
        log('I already submitted the code {!r}.'.format(code))
    else:
        for name, user in conf.get('users', {}).items():
            response = swag_code_box(user, code)
            log('{}: {!r}: {}'.format(name, code, response))
            if 'Mobile App' in response:
                response = mobile_app(user, code)
                log('{}: {!r}: {}'.format(name, code, response))
            if 'SwagButton' in response:
                response = swagbutton(user, code)
                log('{}: {!r}: {}'.format(name, code, response))
        conf['last_code'] = code

    with conf_file.open('w') as f:
        json.dump(conf, f, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
