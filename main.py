import random
import matplotlib.pyplot as plt
import math
from scipy import stats
plt.close('all')

    
# Dane wejściowe
wagaPrzedmiotu =    [12, 8, 15, 2, 9, 17, 36, 8, 14, 9]
wartoscPrzedmiotu = [25, 32, 5, 8, 16, 12, 19, 2, 14, 3]
pojemnoscPlecaka = 89

# parametry_algorytmu
rozmiarPopulacji = 20
wspolczynnikMutacji = 0.1
generacjeIlosc = 4
wspolczynnikKrzyzowania=0.8


def Generowanie_Indywidualne():
    return [random.randint(0, 1) for _ in range(len(wagaPrzedmiotu))]

populacja = [Generowanie_Indywidualne() for _ in range(rozmiarPopulacji)]

# oceniać kondycję poszczególnych dopasowan
def OcenaDopasowan(jednostka):
    liczbakrzyzowek=0
    wagaCalkowita = sum([jednostka[i] * wagaPrzedmiotu[i] for i in range(len(wagaPrzedmiotu))])
    wartoscCalkowita = sum([jednostka[i] * wartoscPrzedmiotu[i] for i in range(len(wartoscPrzedmiotu))])
    # print("+")
    return wartoscCalkowita if wagaCalkowita <= pojemnoscPlecaka else 0


def Ruletka(population, wynikDopasowania):
    start = 0.0
    suma = sum(wynikDopasowania)
    los = random.random()
    for x in range(len(wynikDopasowania)):
        nowyStart = wynikDopasowania[x] / suma
        if (start <= los < nowyStart):
            return population[x]
        start = nowyStart


def krzyzowanie(rodzic1, rodzic2):
    punktKrzyzowania = random.randint(1, len(rodzic1) - 1)
    dziecko1 = rodzic1[:punktKrzyzowania] + rodzic2[punktKrzyzowania:]
    dziecko2 = rodzic2[:punktKrzyzowania] + rodzic1[punktKrzyzowania:]
    return dziecko1, dziecko2


def mutate(jednostka, szansa=0.1):
    for i in range(len(jednostka)):
        if random.random() < szansa:
            jednostka[i] = 1 - jednostka[i]


y=[]
for generacja in range(generacjeIlosc):


    wynikDopasowania = [OcenaDopasowan(jednostka) for jednostka in populacja]
    print("Wyniki dopasowania całej polpulacji ",wynikDopasowania)

    # rodzice = [Ruletka(populacja,wynikDopasowania) for _ in range(rozmiarPopulacji)]
    

    kary=0
    for x in range(len(populacja)):
        if(x < 9):
            print("osobnik #",x+1,"  ",populacja[x],"Wynik dopasowania tego osobnika : ",wynikDopasowania[x],end="")
            if wynikDopasowania[x]==0:
                print(" Osobnik ",x+1,"jest przeładowany i ponosi karę",end="")
                kary += 1
            print("")
        else:
            print("osobnik #",x+1," ",populacja[x],"Wynik dopasowania tego osobnika : ",wynikDopasowania[x],end="")
            if wynikDopasowania[x]==0:
                print(" Osobnik ",x+1,"jest przeładowany i ponosi karę",end="")
                kary += 1
            print("")
    print("\n")
    

    nowaPopulacja = []
    odrzucone=0
    for i in range(rozmiarPopulacji // 2):
        rodzic1, rodzic2 = Ruletka(populacja,wynikDopasowania), Ruletka(populacja,wynikDopasowania)
        while rodzic2 == rodzic1:
            rodzic2 = Ruletka(populacja,wynikDopasowania)
        if random.uniform(0, 1) <= wspolczynnikKrzyzowania:
            dziecko1, dziecko2 = krzyzowanie(rodzic1, rodzic2)
        # Przechodzą dalej czy mamy losować nową parę na ich miejsce???
        else:
            dziecko1 = rodzic1
            dziecko2 = rodzic2
            odrzucone += 1
        mutate(dziecko1, wspolczynnikMutacji)
        mutate(dziecko2, wspolczynnikMutacji)
        nowaPopulacja.extend([dziecko1, dziecko2])

    # zastąpienie populacji nową generacją
    populacja = nowaPopulacja

    # wybór najlepszego osobnika
    najlepszy_osobnik = max(populacja, key=OcenaDopasowan)


    najlepszeDopasowanie = OcenaDopasowan(najlepszy_osobnik)
    y.append(najlepszeDopasowanie)
# Wyniki
    print("Najlepszy Osobnik:", najlepszy_osobnik)
    print("Najlepsze Dopasowanie Wartości:", najlepszeDopasowanie)

    najlepszaWaga = 0
# print(najlepszy_osobnik)
# print(wagaPrzedmiotu)
    for x in range(len(wagaPrzedmiotu)):
        if najlepszy_osobnik[x]==1:
            najlepszaWaga= najlepszaWaga + wagaPrzedmiotu[x]

    print ("Przy Wadze:", najlepszaWaga)
    print("Ilość osobników w populacji ukaranych za przeładowanie: )", kary, "\n")
    print("*"*70)

    plt.plot(generacja+1,najlepszeDopasowanie,'ro')
    plt.ylabel("Najlepsze dopadsowanie wartości")
    plt.xlabel("Kolejna generacja")
    x = range(1,generacjeIlosc+1)
    new_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(new_list)
    for x in range(len(populacja)):
        if (OcenaDopasowan(populacja[x])==najlepszeDopasowanie):
            plt.annotate("os"+str(x+1), (generacja+1, najlepszeDopasowanie))
x = range(1, generacjeIlosc + 1)
slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
    return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)

plt.show()
