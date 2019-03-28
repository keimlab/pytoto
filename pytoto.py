import random
import urllib3
import certifi
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate
import argparse
 
 
class Toto():
    def __init__(self, kuzi_num):
        self.url = "http://sport-kuji.toto-dream.com/dci/I/IPA/IPA01.do?op=disptotoLotInfo&holdCntId=" + str(kuzi_num)
         
        #httpsサイト向け処理
        self.http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where(),
        )
 
        #wdl(勝敗予想)のデフォルトウェイト値
        self.ha_w = 4
        self.ha_d = 1
        self.ha_l = 2
        self.ha = 2
        self.rd = 1
 
    def get_matchtable(self):
        try:
            r = self.http.request("GET", self.url)
            soup = BeautifulSoup(r.data, "lxml")
        except:
            print("ページをGETできませんでした。")
            sys.exit(1)
 
        table_soup = soup.findAll("table", {"class": "kobetsu-format3"})[0]
        table_tr = table_soup.findAll("tr")
 
        rows = []
        for row in table_tr:
            cols = []
            for cell in row.findAll(["td", "th"]):
                cols.append(cell.get_text().strip())
 
            #列の最後の文字列(データ)を空白に置き換え
            #開催日により表記ゆれがあるため、条件分岐で処理。
            if cols[-1] == "データ":
                cols[-1] = ""
            else:
                cols.append("")
            rows.append(cols)
 
        #取得データのヘッダ情報を削除
        del rows[0]
 
        return rows
 
    def show_matchtable(self, withoutwdl=0):
        rows = self.get_matchtable()
 
        if withoutwdl != 1:
            for i in range(len(rows)):
                rows[i].pop()
                rows[i].append(self.__wdl())
 
        #テーブル処理:ヘッダ
        tbl_head = ["試合", "開催日", "時間", "競技場", "ホーム", "VS", "アウェイ", "勝敗予想"]
 
        print((tabulate(rows, tbl_head, tablefmt="grid")))
 
    def set_wdlweight(self, ha_w, ha_d, ha_l, ha, rd):
        self.ha_w = ha_w
        self.ha_d = ha_d
        self.ha_l = ha_l
        self.ha = ha
        self.rd = rd
 
    def __wdl(self):
        #勝ち負けを判定する関数(Win Draw Loose)
        wdl_list = ["X - -", "- X -", "- - X"]
 
        #ホーム・アウェイによる予想
        wdl_homeaway = random.choices(
            [0, 1, 2], weights=[self.ha_w, self.ha_d, self.ha_l])
 
        #完全ランダムによる予想
        wdl_random = random.choices([0, 1, 2])
 
        #各予想結果からどの予想を選択するのか
        wdl_select = random.choices([wdl_homeaway[0], wdl_random[0]], weights=[self.ha, self.rd])
 
        return wdl_list[wdl_select[0]]
 
 
def main():
    parser = argparse.ArgumentParser(description="totoの予想をするプログラム")
 
    parser.add_argument("-t", type=int, help="開催回を指定")
    parser.add_argument("-wowdl", type=int, default=0, help="勝敗予想を表に入れるか　0:入れない 1:入れる :default=0")
    parser.add_argument("-ha_w", type=int, default=4, help="勝敗予想:ホーム・アウェイ:ホームが勝利 :default=4")
    parser.add_argument("-ha_d", type=int, default=1, help="勝敗予想:ホーム・アウェイ:引き分け :default=1")
    parser.add_argument("-ha_l", type=int, default=2, help="勝敗予想:ホーム・アウェイ:ホームが敗北 :default=2")
    parser.add_argument("-ha", type=int, default=2, help="勝敗予想:ホーム・アウェイの割合 :default=2")
    parser.add_argument("-rd", type=int, default=1, help="勝敗予想:完全ランダムの割合 :default=1")
 
    args = parser.parse_args()
 
    if args.t == None:
        parser.print_help()
    else:
        game = Toto(args.t)
        game.set_wdlweight(args.ha_w, args.ha_d, args.ha_l, args.ha, args.rd)
        game.show_matchtable(args.wowdl)
 
 
if __name__ == "__main__":
    main()