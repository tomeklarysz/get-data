import pandas as pd

excel_file = 'Psychidae_ISEZ.xlsx' # nazwa pliku excel

data = pd.read_excel(excel_file) # odczytywanie z tego pliku

df = pd.DataFrame(data) # data frame

gatunek = input("Gatunek: ")

df2 = df.loc[df["Gatunek"] == gatunek] # mniejszy data frame -> tylko gatunek, ktory nas interesuje

# liczba_wierszy = len(df2)
# liczba_kolumn = len(list(df2))

print(gatunek)  # na samej górze nazwa gatunku
print()
#print(df2.index)
#print(df2)
#print(df2.iloc[0]["Numer gabloty"])

kraje = {} # dictionary (coś w stylu tablicy), w którym key to to kraj, a value to dane, które będą do skopiowania
wojewodztwa = {} # key to województwa, na tej samej zasadzie co wyżej 
     
df_kraj = pd.DataFrame(df2["Kraj"]) # data frame tylko z krajami
df_kraj = df_kraj.fillna(0) # zamiana pustych komórek na 0, aby potem łatwiej je pominąć

df_woj = pd.DataFrame(df2["Województwo"]) # data frame tylko z województwami
df_woj = df_woj.fillna(0) # zamiana pustych komórek na 0, aby potem łatwiej je pominąć

# pętla do uzupełniania dictionary z krajami
for i in range(0, len(df_kraj)):
    cur = df_kraj.iloc[i].item()
    if cur != 0 and cur not in kraje and cur != "PL":
        kraje.update({cur: ""})
    if cur == 0 or cur == "?":
        cur = "?"
        kraje.update({cur: ""})
    if cur == "PL":
        cur1 = df_woj.iloc[i].item()
        if cur1 != 0 and cur1 not in wojewodztwa and cur1 != "?": # jesli sa wojewodztwa
            wojewodztwa.update({cur1: ""})
        if cur1 == 0 or cur == "?":
            cur1 = "?"
            kraje.update({cur1: ""})


#print(kraje)
#print(wojewodztwa)

index = df2.index # zakres komorek danego gatunku

#print(df2.iloc[index[0]])

# zagnieżdżona pętle, żeby iterować po kolumnach i wierszach 
for i in range(index[0], index[-1]+1):
    df3 = pd.DataFrame(df2.loc[i]) # dataframe kolejnego wiersza
    df3 = df3.fillna("False") # zamiana brakujących danych w komórce na "False"

    for j in range(2, len(list(df2))-1):
        current = df3.iloc[j].item() # aktualna wartość komórki
        
        # sprawdzenie, czy aktualna wartosc znajduje sie w tabeli z wojewodztwami i pozniejsze dodanie danych z tego wiersza
        if current in wojewodztwa:
            for k in range(j+1, len(list(df2))-1):
                item = df3.iloc[k].item().rstrip()
                if item == "False":
                    continue
                for i in range (0, len(list(df2))):
                    if item == df3.loc["Numer gabloty"].item():
                        item = "g. "+item
                    if item == df2.iloc[i]["Uwagi"]:
                        item = "["+item+"]"
                if "coll. ISEZ PAN Kraków" in item:
                    item = item.replace(" coll. ISEZ PAN Kraków", "")
                    item = item.replace(",", "")
                if k != len(list(df2))-2:
                    wojewodztwa[current] += str(item)+", "
                else: wojewodztwa[current] += str(item)
            wojewodztwa[current] += "; "
            
        if current != "PL" and current in kraje:
            for k in range(j+1, len(list(df2))-1):
                item = df3.iloc[k].item().rstrip()
                if item == "False":
                    continue
                for i in range (0, len(list(df2))):
                    if item == df3.loc["Numer gabloty"].item():
                        item = "g. "+item
                    if item == df2.iloc[i]["Uwagi"]:
                        item = "["+item+"]"
                if "coll. ISEZ PAN Kraków" in item:
                    item = item.replace(" coll. ISEZ PAN Kraków", "")
                    item = item.replace(",", "")
                if k != len(list(df2))-2:
                    kraje[current] += str(item)+", "
                else: kraje[current] += str(item)
            kraje[current] += "; "
        
        if current == "PL": # nie dodaje do tablicy polski, bo wtedy patrzymy na województwa
            continue

if wojewodztwa:
    for w in wojewodztwa:
        print(w+": "+wojewodztwa[w])
        print()

print("----------")
if kraje:
    for k in kraje:
        if k == "?":
            print("Brak lokalizacji: "+kraje[k])
            print()
        else: 
            print(k+": "+kraje[k])
            print()
