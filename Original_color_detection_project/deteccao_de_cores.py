import cv2 as cv
import pandas as pd

#Criando analisador de argumentos para obter o caminho da imagem da linha de comando
img_path = r'colorpic.jpg'

#Lendo a imagem com 'opencv'
img = cv.imread(img_path)

#Declarando variáveis globais (não usadas posteriormente)
clicked = False
r = g = b = xpos = ypos = 0

#Lendo o arquivo 'csv' com a biblioteca 'pandas' e dando nomes para cada coluna
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#Função para calcular a distância mínima de todas as cores e obter a cor mais precisa/correspondente
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#Função para obter as coordenadas 'x' e 'y' do clique duplo do mouse
def draw_function(event, x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv.namedWindow('image')
cv.setMouseCallback('image',draw_function)

while(1):

    cv.imshow("image",img)
    if (clicked):
   
        #cv.rectangle(image, startpoint, endpoint, color, thickness)-1 - Preenche todo o retângulo 
        cv.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Criando 'string' de texto para exibir (Cor, nome e valores do RGB)
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv.LINE_AA)

        #Para cores muito claras, exibiremos texto na cor preto
        if(r+g+b>=600):
            cv.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv.LINE_AA)
            
        clicked=False

    #Parando o 'loop' quando pressionada a tecla 'Esc' pelo usuário
    if cv.waitKey(20) & 0xFF ==27: #O 27 é a tecla 'Esc', o (0) qualquer tecla, (5000) cinco seg fecha automático, (13) enter, ord('a') tecla a ou colocar qualquer outra do alfabeto
        break
    
cv.destroyAllWindows()