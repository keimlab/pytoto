import urllib3
import certifi 
from bs4 import BeautifulSoup
import sys
 
def toto():
    url = "https://sport-kuji.toto-dream.com/dci/I/IPA/IPA01.do?op=disptotoLotInfo&holdCntId=1042"
 
    http = urllib3.PoolManager(
        cert_reqs = 'CERT_REQUIRED',
        ca_certs = certifi.where())
 
    try:
        r = http.request('GET', url)
        soup = BeautifulSoup(r.data,'lxml')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)
 
    table_soup = soup.findAll("table",{"class":"kobetsu-format3"})[0]
    table_tr = table_soup.findAll("tr")
 
    rows = []
    for row in table_tr:
        cols = []
        for cell in row.findAll(['td','th']):
           cols.append(cell.get_text().strip())
        rows.append(cols)
 
    return rows 
 
def main():
    game_list = toto() 
 
    for i  in range(len(game_list)):
        print(game_list[i])
 
if __name__ == '__main__':
    main()