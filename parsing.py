import random
import os
import tldextract
import re


def Un_parsing(url):
    """
    :param   domain:
    :return: 如果ping通 返回1，如果ping不通返回0
    """
    seed = "abcdefghijklnmopqrstuvwxyz0123456789"
    sa = []
    for i in range(16):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    extract = tldextract.TLDExtract()
    website = extract(url).domain + "." + extract(url).suffix
    domain = salt + "." + website
    print(domain)
    try:
        response = os.popen('ping -W 1 -c 1 %s' % domain).read()
        print(response)
        ip = re.search('\((.*?)\)', response, re.I).group(1)
        # print(ip)
        return 1
    except:
        return 0

if __name__ == "__main__":
    res=Un_parsing('http://yllu.ustc.edu.cn/')
    print(res)



