import os
import re
import sys
import requests
ROOT = os.getcwd()
# 初始化代理和数据地址
def init(sets):
    if "PROXY" in sets and sets['PROXY']:
        os.environ['http_proxy']='http://'+sets["PROXY"].replace("http://",'http://').strip()
        os.environ['https_proxy']='http://'+sets["PROXY"].replace("http://",'http://').strip()
    os.environ['SNAP']=ROOT
    os.environ['SNAP_USER_DATA']=ROOT
#解析 set.ini
def parse_init():
    settings = {}
    file = os.path.join(ROOT, 'set.ini')
    if os.path.exists(file):
        with open(file, 'r', encoding="utf-8") as f:
            # 遍历.ini文件中的每个section
            for it in f.readlines():
                it = it.strip()
                if it.startswith(';') or it.startswith('#'):
                    continue
                key,value = it.split('=', 1)
                # 遍历每个section中的每个option
                key = key.strip()
                value = value.strip()
                if re.match(r'^\d+$', value):
                    settings[key] = int(value)
                elif value.lower() == 'true':
                    settings[key] = True
                elif value.lower() == 'false':
                    settings[key] = False
                else:
                    tmp = str(value.lower()).replace('，',',')
                    settings[key]=tmp
    return settings
settings=parse_init()
init(settings)

def testgithub():
    # 判断能否连通 raw.githubusercontent.com
    # 如果存在 index.json则视为连通, 也就是仅需第一次下载模式使用代理，其他情况下可无需代理
    path=os.path.join(ROOT,'.local/cache/argos-translate')
    os.makedirs(path,exist_ok=True)
    cache=os.path.join(path,'index.json')
    if os.path.exists(cache) and os.path.getsize(cache)>0:
        return True
    try:
        print("测试下载模型")
        proxy=None
        server=settings['PROXY']
        if server:
            proxy={
                "http":server,
                "https":server
            }
        print(f'代理: {"无" if not proxy else server}')
        res=requests.get("https://raw.githubusercontent.com/argosopentech/argospm-index/main/index.json", proxies=proxy)
        if res.status_code!=200:
            raise Exception(f"status_code={res.status_code}")
        with open(cache,'w',encoding='utf-8') as f:
            f.write(res.text)
    except Exception as e:
        msg='第一次启动需要下载模型，请设置代理地址' if not settings['PROXY'] else f'你设置的代理地址不正确:{settings["PROXY"]},请正确设置代理，以便下载模型'
        print(f"\n=======\n无法下载模型，{msg}\n\n{e}\n\n")
        return False
    print('测试通过，准备下载模型，模型可能较大，确保网络稳定')
    return True


def run():
    try:
        sys.argv.extend(["--host",settings['HOST'],"--port",str(settings['PORT']),"--load-only",settings['LANG'],"--update"])
        # 不存在 index.json 并且无法连接 raw.githubusercontent.com，则停止执行
        if not testgithub():
            return
        from libretranslate.main import main
        main()
    except Exception as e:
        err=str(e)
        if re.search(r'download error',err,re.I):
            msg='第一次启动需要下载模型，请设置代理地址' if not settings['PROXY'] else f'你设置的代理地址不正确:{settings["PROXY"]},请正确设置代理，以便下载模型'
            print(f"\n=======\n无法下载模型，{msg}\n{err}\n\n")
        else:
            print(err)
        sys.exit()


if __name__=='__main__':
    run()