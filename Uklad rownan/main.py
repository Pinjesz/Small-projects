import copy

def rozw_uklad_rownan(uklad_rozw):
    if wyznacznik(uklad_rozw) == 0 :
        print("Układ nie posiada dokładnie jednego rozwiązania")
    else:
        rozw = []
        main_det = wyznacznik(uklad_rozw)
        for i, rows in enumerate(uklad_rozw) : 
            bufor_r = copy.deepcopy(uklad_rozw)     
            if i == 0:
               continue
            else:           
                rozw.append(wyznacznik(mod_wyzn(bufor_r,i-1))/main_det)
        print(rozw)
        
def wyznacznik(uklad_wzn):
    if len(uklad_wzn) == 2 :
        return int(uklad_wzn[1][0])
    else:
        det = 0
        for i, rows in enumerate(uklad_wzn):
            bufor_w = copy.deepcopy(uklad_wzn)
            if i == 0:
                continue
            else:
                rl = wyznacznik(rozwiniecie_L(bufor_w, i))
                det += int(uklad_wzn[i][0]) *  rl * pow(-1, i+1)
        return det

def rozwiniecie_L(uklad_rl, w):
    bufor_rl = copy.deepcopy(uklad_rl)
    del bufor_rl[w]
    for i, rows in enumerate(bufor_rl):
        if i == 0: continue 
        else:
            del bufor_rl[i][0]
    return bufor_rl

def mod_wyzn(uklad_mod,r):
    bufor_m = copy.deepcopy(uklad_mod)
    for i, rows in enumerate(bufor_m):
        if i == 0 :
            continue
        else:
            bufor_m[i][r] = bufor_m[i][-1]
    return bufor_m

print("Podaj ilość zmiennych")
il_zmiennych = int(input())
print("Podaj macierz")
i = 0
uklad=[[0]]
while i < il_zmiennych :    
    uklad += [[0]]
    i+=1
    uklad[i] = input().split(" ")

rozw_uklad_rownan(uklad)

f=input("\n\nWciśnij enter by zakońcyć")