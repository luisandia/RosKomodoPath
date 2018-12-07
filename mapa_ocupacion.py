from math import *
import sys


class MapaOcupacion:
    def __init__(self, i, j, width, height,x,y):
        print "MapaOcupacion"
        self.BOLDRED = "\033[1m\033[31m"
        self.BOLDYELLOW = "\033[1m\033[33m"
        self.WHITE  = "\033[37m"     
        self.RESET = "\033[0m"
        self.col = j
        self.fil = i
        self.mapa = [ [ "0.000" for j in range(self.col) ] for i in range(self.fil) ]
        # print  self.mapa
        self.komodo = self.WHITE+"kmodo"+self.BOLDYELLOW
        self.mapa[x][y]=self.komodo

    def getMapa(self):
        for i in range(self.col):
            sys.stdout.write(self.BOLDRED+"%6d"%(i))
        print ""
        sys.stdout.write("   ")
        for j in range(self.col):
            sys.stdout.write(self.BOLDYELLOW+"------")
        print ""
        
        for i in range(self.fil):
            sys.stdout.write(self.BOLDRED+ "%d"%i)
            sys.stdout.write(self.BOLDYELLOW+ " |" if len(str(i))==1 else self.BOLDYELLOW +"|" )

            for j in range(self.col):
                if  self.mapa[i][j]!=self.WHITE+"kmodo"+self.BOLDYELLOW and float(self.mapa[i][j])>0.0:
                    sys.stdout.write(self.BOLDRED+str(round(self.mapa[i][j],3))+ self.BOLDYELLOW+"|")
                else:
                    sys.stdout.write(""+str(self.mapa[i][j])+ "|")
            print ""
            sys.stdout.write(self.BOLDYELLOW + "  |")

            # for j in range(self.col):
            #     sys.stdout.write("     |")
            # print ""
            # sys.stdout.write(self.BOLDYELLOW + "  |")

            for j in range(self.col):
                sys.stdout.write("-----|")
            print ""

        print self.RESET
        # print "\n"
    def getValue(self,x,y):
        # print "insert mapa ",x,' ',y
        return float(self.mapa[x][y])

    def setCoord(self,x,y,value):
        self.mapa[x][y]=value

    def interactua(self):

        while not rospy.is_shutdown():
            print self.rear.range
            self.rate.sleep()


if __name__ == '__main__':
    x = MapaOcupacion(5, 5, 0.50, 0.50)
    x.getMapa()
