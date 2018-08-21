## Usage

git clone代码后**第一次运行**, 需要初始化sqlite数据库(只需要执行一次):

``` bash
bash run_at_first_time.sh
```

查询IP的信息: 经纬度,国家,城市等

``` bash
./fetch_ip_info.py www.baidu.com

./fetch_ip_info.py 47.75.51.143
```

支持Python 2 和 Python 3.

## 数据说明

* [GeoIp数据来源(更新20180327)](https://dev.maxmind.com/geoip/legacy/geolite/)
* [chinaz数据来源](http://ip.chinaz.com/ajaxsync.aspx)
* [国家代号:维基百科](https://zh.wikipedia.org/wiki/%E5%9C%8B%E5%AE%B6%E5%9C%B0%E5%8D%80%E4%BB%A3%E7%A2%BC)

## 其他链接

* [百度地图经纬度查询](http://api.map.baidu.com/lbsapi/getpoint/index.html)
* [whois查询](https://www.ultratools.com/tools/ipWhoisLookupResult)
