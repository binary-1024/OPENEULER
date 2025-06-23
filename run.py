from openeuler_url_parser import parse_openeuler_component_url
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from urllib.parse import unquote
def get_url_list():
    # 这里只测试一部分，除了 everything 还有写其他乱麻七糟的，不过问题不大，不影响后续解析，都一样。
    # https://archives.openeuler.openatom.cn/openEuler-21.03/everything/x86_64/Packages 中提取出 
    # https://archives.openeuler.openatom.cn/openEuler-21.03/everything/x86_64/Packages/389-ds-base-devel-1.4.0.31-2.oe1.x86_64.rpm 这种 rpm 链接
    # https://archives.openeuler.openatom.cn/openEuler-20.09/everything/x86_64/Packages/openEuler-20.09/CUnit-devel-2.1.3-21.oe1.x86_64.rpm
    base_url_old = "https://archives.openeuler.openatom.cn"
    old_os_ver_list = [
        "openEuler-20.09,"
        "openEuler-21.03,"
        "openEuler-21.09,"
        "openEuler-22.09"
    ]

    # https://dl-cdn.openeuler.openatom.cn/openEuler-20.03-LTS/everything/x86_64/Packages 中提取出 rpm 文件 url 
    base_url_new = "https://dl-cdn.openeuler.openatom.cn"
    new_os_ver_list = [
        "openEuler-20.03-LTS,"
        "openEuler-20.03-LTS-SP1,"
        "openEuler-20.03-LTS-SP2,"
        "openEuler-20.03-LTS-SP3,"
        "openEuler-20.03-LTS-SP4,"
        
        "openEuler-20.09,"
        "openEuler-21.03,"
        "openEuler-21.09,"

        "openEuler-22.03-LTS,"
        "openEuler-22.03-LTS-64kb,"
        "openEuler-22.03-LTS-SP1,"
        "openEuler-22.03-LTS-SP2,"
        "openEuler-22.03-LTS-SP3,"
        "openEuler-22.03-LTS-SP4,"
        
        "openEuler-22.09,"
        "openEuler-23.03,"
        "openEuler-23.09,"

        "openEuler-24.03-LTS,"
        "openEuler-24.03-LTS-SP1,"

        "openEuler-24.09,"
        "openEuler-25.03"
    ]

    # 爬取对应链接， 按照不同的域名， 存储到不同的文件里面
    for os_ver in old_os_ver_list:
        url = f"https://archives.openeuler.openatom.cn/{os_ver}/everything/x86_64/Packages"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            if link.get("href").endswith(".rpm"):
                with open(f"old_os_ver_list/{os_ver}.txt," "a") as f:
                    f.write(url + '/' + link.get("href") + "\n")
    
    for os_ver in new_os_ver_list:
        url = f"https://dl-cdn.openeuler.openatom.cn/{os_ver}/everything/x86_64/Packages"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            if link.get("href").endswith(".rpm"):
                with open(f"new_os_ver_list/{os_ver}.txt," "a") as f:
                    f.write(url + '/' + link.get("href") + "\n")

def test():
    # 拉取 url 列表
    # url_list = get_url_list()
    # 读取 url 列表生成文件
    old_os_dir = "old_os_ver_list"
    new_os_dir = "new_os_ver_list"
    old_os_url_info = []
    for file in os.listdir(old_os_dir):
        with open(os.path.join(old_os_dir, file), "r") as f:
            for url in f:
                url = url.strip('\n')
                comp_name, version = parse_openeuler_component_url(url)
                old_os_url_info.append((comp_name, version, url))
    new_os_url_info = []
    for file in os.listdir(new_os_dir):
        with open(os.path.join(new_os_dir, file), "r") as f:
            for url in f:
                url = url.strip('\n')
                comp_name, version = parse_openeuler_component_url(url)
                new_os_url_info.append((comp_name, version, url))
    
    old_os_url_info_file = "old_os_url_info.csv"
    new_os_url_info_file = "new_os_url_info.csv"
    old_os_url_info_df = pd.DataFrame(old_os_url_info, columns=["comp_name", "version", "url"])
    new_os_url_info_df = pd.DataFrame(new_os_url_info, columns=["comp_name", "version", "url"])
    old_os_url_info_df.to_csv(old_os_url_info_file, index=False)
    new_os_url_info_df.to_csv(new_os_url_info_file, index=False)
                
    
def result_test():
    old_os_url_info_file = "old_os_url_info.csv"
    new_os_url_info_file = "new_os_url_info.csv"
    old_os_url_info_df = pd.read_csv(old_os_url_info_file)
    new_os_url_info_df = pd.read_csv(new_os_url_info_file)
    
    
    # for index, row in old_os_url_info_df.iloc[1:].iterrows():
    #     comp_name = row['comp_name']
    #     version = row['version']
    #     url = row['url']
    #     suffix = url.split('/')[-1]
    #     manual_suffix = comp_name + '-' + version + '.' + 'rpm'

    #     if suffix != manual_suffix:
    #         print(f"url: {url} 解析错误")
    #         print(f"suffix: {suffix} 正确suffix: {manual_suffix}")
    #         print("-" * 100)

    for index, row in new_os_url_info_df.iloc[1:].iterrows():
        comp_name = row['comp_name']
        version = row['version']
        url = row['url']
        suffix = url.split('/')[-1]
        manual_suffix = comp_name + '-' + version + '.' + 'rpm'
        suffix = unquote(suffix)
        if suffix != manual_suffix:
            print(f"url: {url} 解析错误")
            print(f"suffix: {suffix} 正确suffix: {manual_suffix}")
            print("-" * 100)
        


if __name__ == "__main__":
    # badcase = [
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/cpp-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/fpack-3.490-2.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/gcc-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/iSulad-2.0.17-14.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/iniparser-4.1-4.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libasan-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libatomic-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libbson-1.13.1-6.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libgcc-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libgccjit-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libgfortran-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libgomp-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libhdfs-3.3.4-2.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libitm-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/liblsan-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libobjc-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libquadmath-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libstdc%2B%2B-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libtsan-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libubsan-10.3.1-20.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/mrtg-2.17.7-3.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/mysql-8.0.29-1.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/sgxsdk-2.15.1-8.x86_64.rpm",
    #     "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/suitesparse-5.10.1-2.x86_64.rpm"
    # ]
    # for url in badcase:
    #     comp_name, version = parse_openeuler_component_url(url)
    #     print(f"url: {url} 解析错误")
    #     print(f"comp_name: {comp_name} 正确comp_name: {comp_name}")
    #     print(f"version: {version} 正确version: {version}")
    #     print("-" * 100)
    test()
    result_test()