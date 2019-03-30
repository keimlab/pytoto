import random
 
n = 13 #試合数
 
def wdl():
#勝ち負けを判定する関数(Win Draw Loose)
 
    wdl_list =['X - -','- X -','- - X']
 
    return random.choice(wdl_list)
 
def main():
 
    for i in range(1,n+1):
        print('{0:2d}試合目:  {1}'.format(i,wdl()))
 
if __name__ == '__main__':
    main()