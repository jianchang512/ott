[简体中文](./README.md)

# Offine-Text-Translate Local Offline Text Translation

Supports multi-language local offline text translation Api tool

>
>
> This project is a re-encapsulation based on [Open Source Project LibreTranslate](https://github.com/LibreTranslate/LibreTranslate), the purpose is to provide a translation Api service that can be easily directly deployed on local machines without the need for docker, and provide Windows precompiled exe package, no need to deploy, can be used by double-clicking, convenient for beginners and non-tech savvy users.
>
> The first launch needs to download the model, and subsequent operation can be offline.
>
> If you want to use the original LibreTranslate project or want to deploy on docker, please visit https://github.com/LibreTranslate/LibreTranslate
>

![image](https://github.com/jianchang512/ott/assets/3378335/2965176e-8f03-49bb-803e-2fdefbadfe7e)


## Windows precompiled exe Download and Use

1. [Click to download the Windows precompiled package](https://github.com/jianchang512/ott), unzip to an English directory without spaces, and double-click start.exe.

2. After the first launch, the model will be automatically downloaded. If you can't open `https://raw.githubusercontent.com`, you must set the proxy address in `PROXY=` in set.ini, otherwise, it can't be downloaded. Of course, you can also choose to download the packaged model from Baidu network disk, unzip and overwrite the **.local** folder inside to the root directory of this software, [click to download the model from Baidu network disk](https://pan.baidu.com/s/1h5upbQIQw3LmUU6-3-YRbw?pwd=72bj).


3. You can write your own program to request this Api service, to implement Baidu translation and other functions, or fill in some software that needs translation functions. If you want to use it in [video translation dubbing software](https://github.com/jianchang512/pyvideotrans) , fill in the server address and port in OTT in the software menu. The default address is `http://127.0.0.1:9911`.

## Windows up Source Code Deployment

0. First go to the python.org website to download the python3.9+ version and install it, it is recommended to install 3.10. When installing, carefully check and tick the "Add ... Path" checkbox for convenience.

1. Install Windows git client, [click to download git](https://git-scm.com/download/win), select to download 64-bit Git for Windows Setup, double-click to install, follow through steps until completion.

2. Create an empty directory, such as the ott directory under the D drive, then enter the directory `D:/ott`, enter `cmd` in the address bar and press enter, in the opened cmd black window, enter `git clone https://github.com/jianchang512/ott .`  and press enter.

3. Create a virtual environment, continue to enter the command `python -m venv venv` in the cmd window and press enter.

>     Pay attention here: If it prompts "python is not an internal or external command, also not a runnable program", it indicates that the checkbox was not ticked when installing python in step 0. Click the downloaded Python installer again, choose "Modify", and make sure to tick "Add ... Path".
>
>     After reinstalling python, **You must close the opened cmd window**, then enter`D:/ott`, enter`cmd` in the address bar and press enter, then execute `python -m venv venv`
>

4. After executing the command in the previous step, continue to enter `.\venv\scripts\activate` and press enter, then execute `pip install -r requirements.txt --no-deps`. If it prompts "not found version xxx", please change the mirror source to pip official or Aliyun mirror.

5. If you need to enable cuda acceleration translation, continue to execute

    `pip uninstall -y torch`

    `pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cu121`

6. Set proxy address in set.ini PROXY=proxy address, for example if your proxy address is `http://127.0.0.1:10189`, then you should fill in `PROXY=http://127.0.0.1:10189`

7. Execute the command to start the service, `python start.py`

## Mac or Linux Deployment

0. First confirm whether the correct version python3.9+ and git is installed, `python -V` or `python3 -V`

1. Create an empty directory and enter, for example `/data/ott && cd /data/ott`, then pull the source code `git clone https://github.com/jianchang512/ott .`

2. Create a virtual environment and activate it  `python3 -m venv venv && . ./venv/bin/activate`

3. Install dependency, `pip3 install -r requirements.txt --no-deps`. If it prompts "not found ", change the mirror to pip official or Aliyun mirror likewise.

4. If cuda acceleration translation needs to be enabled, continue to execute

    `pip3 uninstall -y torch`

    `pip3 install torch==2.1.2 --index-url https://download.pytorch.org/whl/cu121`

5. Set proxy address in she.ini

6. Start service `python3 start.py`

Please note if your python execution command is not`python3`, the python3 in the above commands should be replaced with your corresponding command.

## Api Interface Usage

Assume your deployment address and port is `http://127.0.0.1:9911` 


API address: `http://127.0.0.1:9911/translate` 


Language code: zh=Simplified Chinese  /  zt=Traditional Chinese  /  en=English  /  fr=French /  de=German /  ja=Japanese /  ko=Korean  /  ru=Russian  /  es=Spanish /  th=Thai /  it=Italian  /  pt=Portuguese /  ar=Arabic  /  tr=Turkish /  hi=Hindi 


Request method: POST

Request data: `q`=text to be translated, `source`=text original language code can be filled in auto automatic recognition, `target`=target language code to be translated to

Return data: Return JSON data, when correct, '{translatedText: "translated result'} ', when error,' {error:" error reason '}'`


**Python requests request example**

```

import requests

result=requests.post("http://127.0.0.1:9911/translate",json={"q":"Hello, my friend","source":"en","target":"zh"})
print(result.json())

#The output is as follows
{'translatedText': '你好,我的朋友'}

#When error returns
{'error':'Error cause'}

```



**JavaScripts fetch request**

```
fetch("http://127.0.0.1:9911/translate", {
  method: "POST",
  body: JSON.stringify({
    q: "Hello!", // The text to translate
    source: "en",// original language, or 'auto' for auto detect
    target: "zh"// target language
  }),
  headers: { "Content-Type": "application/json" }
});

// Returns json response
{
    "translatedText": "你好!" // The translated text is in the transloatedText field
}

#When error returns
{'error':'Error cause'}
```

**JavaScripts jQuery ajax request**

```
$.post("http://127.0.0.1:9911/translate", {
    q: "Hello!", // The text to translate
    source: "en",// original language, or 'auto' for auto detect
    target: "zh"// target language
  },
  function(res){
    console.log(res)
  }
);

// Returns json response
{
    "translatedText": "你好!" // The translated text is in the translatedText field
}

#When error returns

{'error':'Error cause'}

```

**PHP curl**

```

$data = array(
    'q' => 'Hello',
    'source' => 'auto',
    'target' => 'zh'
);
 
$json = json_encode($data);
$url = 'http://127.0.0.1:9911/translate';
$ch = curl_init($url);
 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $json);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json',
    'Content-Length: ' . strlen($json)
));
 
$response = curl_exec($ch);
if(curl_errno($ch)) {
    echo 'Error: ' . curl_error($ch);
} else {
    echo $response;
}
curl_close($ch);

#Return
{
    "translatedText": "你好!" // The translated text is in the translatedText field
}

#When error returns
{'error':'Error cause'}

```



## Modifications to Argostranslate

1. Modified the get method in `\venv\Lib\site-packages\argostranslate\networking.py`. When the download fails, an exception is thrown to remind the user to use a proxy in case of a download mode error.


```
def get (url: str, retry_count: int = 3) - > bytes | None:
    """Downloads data from a url and returns it

    Args:
        url: The url to download (http, https)
        retry_count: The number of retries to attempt if the initial download fails.
                If retry_count is 0 the download will only be attempted once.

    Returns:
        The downloaded data, None is returned if the download fails
    """
    if get_protocol (url) not in supported_protocols:
        return None
    info (f"Get {url}")
    print (f'{url=}')
    download_attempts_count = 0

    while download_attempts_count <= retry_count:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT},
            )
            response = urllib.request.urlopen(req)
            data = response.read()
            info (f"Got {url}")
            return data
        except Exception as err:
            download_attempts_count += 1
            # Add exception throw ++
            raise Exception ('download error')
            error (err)
    # Add exception throw ++
    raise Exception ('download error')
    return None
```

2. `\venv\Lib\site-packages\argostranslate\package.py`

Comment out the error when you can't connect to raw.github.com. This has been handled in the entry file.


```
def update_package_index ():
    """Download remote package index"""
    with package_lock :
        try :
            response = urllib. request. urlopen (settings. remote_package_index)
        except Exception as err :
            # Comment out the error output, the index. json has been obtained in the entry file, if it can't be connected here, it will not output the error, to avoid causing confusion for the layman
            #error (err) --
            return 
        data = response. read ()
        with open (settings. local_package_index, "wb") as f :
            f. write (data)
```

## CUDA Acceleration Support

**Install CUDA Tools** [Detailed Installation Method](https://juejin.cn/post/7318704408727519270)


After installing CUDA, if there are problems, run `pip uninstall -y torch`, and then run `pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cu121`.


Sometimes you will encounter an error that "cublasxx.dll does not exist", or even if this error does not occur, and CUDA is configured correctly, but the recognition is always wrong, you need to download cuBLAS, and then copy the dll file to the system directory

[Click to Download cuBLAS](https://github.com/jianchang512/stt/releases/download/0.0/cuBLAS_win.7z), unzip and copy the dll files to C:/Windows/System32


## Based on the following open source project

1. https://github.com/LibreTranslate/LibreTranslate

2. https://github.com/argosopentech/argos-translate
