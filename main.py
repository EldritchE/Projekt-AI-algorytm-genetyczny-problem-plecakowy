import random
import plotly.express as px
    
# Dane wejściowe
wagaPrzedmiotu =    [12, 8, 15, 2, 9, 17, 36, 8, 14, 9]
wartoscPrzedmiotu = [25, 32, 5, 8, 16, 12, 19, 2, 14, 3]
pojemnoscPlecaka = 89

# parametry_algorytmu
rozmiarPopulacji = 20
wspolczynnikMutacji = 0.1
generacjeIlosc = 2
wspolczynnikKrzyzowania=0.8

# initialize population
def Generowanie_Indywidualne():
    return [random.randint(0, 1) for _ in range(len(wagaPrzedmiotu))]

populacja = [Generowanie_Indywidualne() for _ in range(rozmiarPopulacji)]

# oceniać kondycję poszczególnych dopasowan
def OcenaDopasowan(jednostka):
    wagaCalkowita = sum([jednostka[i] * wagaPrzedmiotu[i] for i in range(len(wagaPrzedmiotu))])
    wartoscCalkowita = sum([jednostka[i] * wartoscPrzedmiotu[i] for i in range(len(wartoscPrzedmiotu))])
    return wartoscCalkowita if wagaCalkowita <= pojemnoscPlecaka else 0

# select parents for crossover
def Ruletka(population, k=3):
    konkurs = random.sample(population, k)
    return max(konkurs, key=OcenaDopasowan)

# perform crossover between parents
def krzyzowanie(rodzic1, rodzic2):
    punktKrzyzowania = random.randint(1, len(rodzic1) - 1)
    dziecko1 = rodzic1[:punktKrzyzowania] + rodzic2[punktKrzyzowania:]
    dziecko2 = rodzic2[:punktKrzyzowania] + rodzic1[punktKrzyzowania:]
    return dziecko1, dziecko2

# perform mutation on individual
def mutate(jednostka, szansa=0.1):
    for i in range(len(jednostka)):
        if random.random() < szansa:
            jednostka[i] = 1 - jednostka[i]

# main genetic algorithm loop
for generacja in range(generacjeIlosc):
    # evaluate fitness of current population
    wynikDopasowania = [OcenaDopasowan(jednostka) for jednostka in populacja]
    # select parents for crossover
    rodzice = [Ruletka(populacja) for _ in range(rozmiarPopulacji)]
    

    
    for x in range(len(populacja)):
        if(x < 9):
            print("osobnik #",x+1,"  ",populacja[x])
        else:
            print("osobnik #",x+1," ",populacja[x])
    print("\n")
    
    # perform crossover and mutation to create new generation
    nowaPopulacja = []
    odrzucone=0
    for i in range(rozmiarPopulacji // 2):
        # TODO: random osoba z wykluczeniem siebie !!!
        rodzic1, rodzic2 = rodzice[i * 2], rodzice[i * 2 + 1]
        if random.uniform(0,1)<=wspolczynnikKrzyzowania:
            dziecko1, dziecko2 = krzyzowanie(rodzic1, rodzic2)
        else:
            dziecko1 = rodzic1
            dziecko2 = rodzic2
            odrzucone+=1
        # print("w tej generacji liczba odrzuconych krzyżówek:", odrzucone)
        mutate(dziecko1, wspolczynnikMutacji)
        mutate(dziecko2, wspolczynnikMutacji)
        nowaPopulacja.extend([dziecko1, dziecko2])

    # zastąpienie populacji nową generacją
    populacja = nowaPopulacja

    # wybór najlepszego osobnika
    najlepszy_osobnik = max(populacja, key=OcenaDopasowan)
    najlepszeDopasowanie = OcenaDopasowan(najlepszy_osobnik)
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

    # fig = px.scatter(x=[], y=[])
    # fig.show()
