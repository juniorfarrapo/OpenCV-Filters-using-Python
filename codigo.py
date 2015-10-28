import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-filter","--filtro",type=int,default=0) #Numero de Frames para aprender o cenario
parser.add_argument("-tm","--kernel",type=int,default=3) #Numero de Frames para aprender o cenario
parser.add_argument("arquivo",nargs="?",default=None) #Nome do arquivo, se houver
args = parser.parse_args()

if args.arquivo:
    print "Aplicando filtro a partir do arquivo..."
    img = cv2.imread(args.arquivo,cv2.IMREAD_GRAYSCALE)
else:
    print "Insira um aquivo como argumento"
    sys.exit(1)

height, width = img.shape[:2]
final = np.zeros(img.shape,np.uint8)

if args.kernel > 0:
    tm_kernel = args.kernel
else:
    print "Insira um tamanho valido para o kernel"
    sys.exit(1)

limite = (tm_kernel - 1) / 2

def passa_baixa():
    kernel = np.ones((tm_kernel,tm_kernel),np.float32)/(tm_kernel*tm_kernel)
    return cv2.filter2D(img,-1,kernel) 

def media():
    for x in range(limite, height - limite):
        for y in range(limite, width - limite):
            total = 0
            tm_total = 0
            for i in range(-limite,limite):
                for j in range(-limite,limite):
                    total += img[x + i, y + j]
                    tm_total += 1
            final[x,y] = total/tm_total
    return final

def mediana():
    return cv2.medianBlur(img,tm_kernel)

def especial():
    kernel = np.matrix('1 1 1 ; 1 2 1 ; 1 1 1',np.float32)/(16)
    return cv2.filter2D(img,-1,kernel) 

if args.filtro == 1:
    dst = passa_baixa()
    cv2.imshow("Filtro Passa-Baixa com kernel de tamanho " + str(tm_kernel),dst)
elif args.filtro == 2:
    dst = media()
    cv2.imshow("Filtro da Media com kernel de tamanho " + str(tm_kernel),dst)
elif args.filtro == 3:
    dst = mediana()
    cv2.imshow("Filtro da Mediana com kernel de tamanho " + str(tm_kernel),dst)
elif args.filtro == 4:
    dst = especial()
    cv2.imshow("Filtro Especial",dst)
else:
    print("Escolha um tipo de filtro");
    sys.exit(1)

cv2.waitKey(0)
cv2.destroyAllWindows()

