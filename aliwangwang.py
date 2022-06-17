# -*- coding: utf-8 -*-


import os, hashlib


def quick_md5(value: str):
    return hashlib.md5(value.encode()).hexdigest().lower()


# HKEY_CURRENT_USER\SOFTWARE\Alibaba\AliWangWang\machineid
def machineid():
    import winreg
    with winreg.OpenKey( \
        winreg.HKEY_CURRENT_USER, r"SOFTWARE\Alibaba\AliWangWang"
    ) as regkey:
        ret, i = winreg.QueryValueEx(regkey, "machineid")
    assert( 1 == i and len(ret) == 32)
    return ret


def ali_data_dir():
    return os.path.expandvars("%appdata%\\aliwangwangData\\MessageSDK\\libaim")


def generate_db_key(uid=''):
    uid_dir = ali_data_dir()

    if (not uid): # take the first one
        uid = list(filter(lambda n: str(n).endswith("@cntaobao"), os.listdir(uid_dir)))[0]

    tmpuid = uid.replace( "@", quick_md5(machineid())[5] )

    tmpmd5, idx = quick_md5(quick_md5(tmpuid) + machineid()), ((len(uid) & 7) + 2)

    return tmpmd5[idx:idx+16]


def main():
    dbkey = generate_db_key()

    ''' go decrypt (first page)'''
    url = r"https://gchq.github.io/CyberChef/#recipe=Take_bytes(0,4096,false)AES_Decrypt(%7B'option':'Latin1','string':'{}'%7D,%7B'option':'Hex','string':''%7D,'ECB','Raw','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)".format(
        dbkey)
    
    os.system("echo go decrypt&& echo \"{}\" && pause".format(url))


if __name__ == "__main__":
    main()