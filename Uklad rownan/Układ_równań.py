import copy

try:

    def rozw_uklad_rownan(uklad):
        for k, column in enumerate(uklad):
            for r, rows in enumerate(uklad):
                if k == r : continue 
                else:
                    if int(uklad[k][k]) == 0:
                        bufor = copy.deepcopy(uklad[k])
                        bf = copy.copy(k)
                        while int(uklad[bf][k]) == 0:
                            if int(uklad[bf+1][k]) != 0:
                                uklad[k] = copy.deepcopy(uklad[bf+1])
                                uklad[bf + 1] = copy.deepcopy(bufor)
                                break
                            bf += 1
                    jut = int(uklad[r][k])/int(uklad[k][k])
                    uklad[r][0] = int(uklad[r][0]) - jut * int(uklad[k][0]) 
                    for i, czynnik in enumerate(uklad):
                        uklad[r][i+1] = int(uklad[r][i+1]) - jut * int(uklad[k][i+1]) 
        rozw = []
        for j, zmienna in enumerate(uklad):
            rozw += [float(uklad[j][-1])/float(uklad[j][j])]
        return(rozw)

    print("Podaj ilość zmiennych")
    il_zmiennych = int(input())
    print("Podaj macierz")
    i = 0
    uklad=[]
    while i < il_zmiennych :
        uklad += [[0]]
        uklad[i] = input().split(" ")
        i+=1

    print(rozw_uklad_rownan(uklad))

    f=input("\n\nWciśnij enter by zakończyć")

except:
    print("Układ nie posiada dokładnie jednego rozwiązania")