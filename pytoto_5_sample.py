from pytoto import Toto
 
 
def main():
    wdl_dict ={
        'ha_w':100,
        'ha_d':0,
        'ha_l':0,
        'ha':40,
        'rd':0
    }
 
    game = Toto(1068)
    game.set_wdlweight(**wdl_dict)
    #game.set_wdlweight(100,0,0,40,0)
    #game.ha_d = 1000
    game.show_matchtable()
 
 
if __name__=="__main__":
    main()
