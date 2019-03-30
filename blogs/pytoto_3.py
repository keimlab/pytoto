import random
import urllib3
import certifi 
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate
 
 
def toto(kuzi_num):
    url = "http://sport-kuji.toto-dream.com/dci/I/IPA/IPA01.do?op=disptotoLotInfo&holdCntId=" + kuzi_num
 
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
 
def wdl():
#勝ち負けを判定する関数(Win Draw Loose)
 
    wdl_list =['X - -','- X -','- - X']
     
    return random.choice(wdl_list)
 
def main():
    #引数の処理、lenが2(引数は一つ)であれば処理継続
    args = sys.argv
    if len(args) == 2:
        game_list = toto(args[1])
    else:
        print("開催回を入れて下さい。")
        sys.exit(1)
 
    #テーブル処理:ヘッダ
    tbl_head = ["試合","開催日","時間","競技場","ホーム","VS","アウェイ","データ","勝敗"]
  
    #テーブル処理:項目
    del game_list[0]
 
    #勝敗を予測し列に追加 
    for i in range(len(game_list)):
        game_list[i].append(wdl())
 
 
    print(tabulate(game_list,tbl_head,tablefmt="grid"))
 
 
if __name__ == '__main__':
    main()