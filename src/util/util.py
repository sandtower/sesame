from datetime import *
import httplib2

class Util(object):
    @staticmethod
    def get_today():
        today = datetime.today()
        return today.strftime("%Y-%m-%d")

    @staticmethod
    def http_get_content(url, headers=None, charset=None):
        if headers is None:
            headers = {  
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
        }
        try:
            http = httplib2.Http()
            request, content = http.request(uri=url, headers=headers)
            if request.status == 200 and content:
                if charset:
                    return content.decode(charset).encode('utf-8')
                else:
                    return content
        except Exception as e:
            raise e

if __name__ == "__main__":
    util = Util()
    print util.get_today()
    url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%s&jidu=%s" \
          % ('300155', '2015', '1')
    print util.http_get_content(url)
