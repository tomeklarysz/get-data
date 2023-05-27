import pandas as pd

excel_file = 'Psychidae_ISEZ.xlsx' # nazwa pliku excel

data = pd.read_excel(excel_file) # odczytywanie z tego pliku

df = pd.DataFrame(data) # data frame

df2 = df.loc[df["Gatunek"] == "Acanthopsyche atra (Linnaeus, 1767)"] # mniejszy data frame -> tylko gatunek, ktory nas interesuje

# liczba_wierszy = len(df2)
# liczba_kolumn = len(list(df2))

print("Acanthopsyche atra (Linnaeus, 1767)")  # na samej górze nazwa gatunku
print()

kraje = {} # dictionary (coś w stylu tablicy), w którym key to to kraj, a value to dane, które będą do skopiowania
wojewodztwa = {} # key to województwa, na tej samej zasadzie co wyżej 
     
df_kraj = pd.DataFrame(df2["Kraj"]) # data frame tylko z krajami
df_kraj = df_kraj.fillna(0) # zamiana pustych komórek na 0, aby potem łatwiej je pominąć

df_woj = pd.DataFrame(df2["Województwo"]) # data frame tylko z województwami
df_woj = df_woj.fillna(0) # zamiana pustych komórek na 0, aby potem łatwiej je pominąć

#print(df_woj.iloc[0].item())
#print(df_woj.iloc[1])

# pętla do uzupełniania dictionary z krajami
for i in range(0, len(df_kraj)):
    cur = df_kraj.iloc[i].item()
    if cur != 0 and cur not in kraje and cur != "?":
        kraje.update({cur: ""})
    if cur == "?":
        cur = "Brak lokalizacji"
        kraje.update({cur: ""})

# pętla do uzupełniania dictionary z wojewodztwami
for i in range(0, len(df_woj)):
    cur = df_woj.iloc[i].item()
    if cur != 0 and cur not in wojewodztwa and cur != "?":
        wojewodztwa.update({cur: ""})
    if cur == "?":
        cur = "Brak lokalizacji"
        wojewodztwa.update({cur: ""})

print(kraje)
print(wojewodztwa)


# zagnieżdżona pętle, żeby iterować po kolumnach i wierszach 
for i in range(0, len(df2)):
    df3 = pd.DataFrame(df2.loc[i]) # dataframe kolejnego wiersza
    df3 = df3.fillna("False") # zamiana brakujących danych w komórce na "False"
    for j in range(2, len(list(df2))-1):
        current = df2.iloc[i][j] # aktualna wartość komórki

        # sprawdzenie, czy aktualna wartosc znajduje sie w tabeli z wojewodztwami i pozniejsze dodanie danych z tego wiersza
        if current in wojewodztwa:
            for k in range(j+1, len(list(df2))-1):
                item = df3.iloc[k].item()
                if item == "False":
                    continue
                if item == df2.iloc[i]["Numer gabloty"]:
                    item = "g. "+item
                if "coll. ISEZ PAN Kraków" in item:
                    item = item.replace(" coll. ISEZ PAN Kraków", "")
                    item = item.replace(", ", "")
                if k != len(list(df2))-2:
                    wojewodztwa[current] += str(item)+", "
                else: wojewodztwa[current] += str(item)
            wojewodztwa[current] += "; "
            
        if current != "PL" and current in kraje:
            for k in range(j+1, len(list(df2))-1):
                item = df3.iloc[k].item()
                if item == "False":
                    continue
                if item == df2.iloc[i]["Numer gabloty"]:
                    item = "g. "+item
                if "coll. ISEZ PAN Kraków" in item:
                    item = item.replace(" coll. ISEZ PAN Kraków", "")
                    item = item.replace(", ", "")
                if k != len(list(df2))-2:
                    kraje[current] += str(item)+", "
                else: kraje[current] += str(item)
            kraje[current] += "; "
        
        if current == "PL":
            continue

    
    #print(kraje)
    #print("---------------------------------------------------------------------")

for w in wojewodztwa:
    print(wojewodztwa[w])
    print()
print("----------")
for k in kraje:
    print(kraje[k])
    print()
print("---------------------------------------------------------------------")
#print(wojewodztwa)
