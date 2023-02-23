

class ExamException (Exception):
    pass

class CSVTimeSeriesFile ():
    
    def __init__ (self,name):
        self.name=name

    # Metodo ausiliaro con lo scopo di verificare se una linea del mio file sia o meno adatta
    def __validate_line__ (self,line): 

        # Verifica aggiuntiva che si stia lavorando con un oggetto istanza di list
        if not isinstance(line,list): 
            return False
            
        # Verifica aggiuntiva che stia lavorando con:
            #Una data di tipo stringa
            #Un numero di passeggeri sia intero oppure stringa
        if ( type(line[0]) != str ) or ( ( type(line[1]) != int ) and ( type (line[1]) != str ) ):
            return False
            
        # Verifica che il valore dei passeggeri sia positivo
        if (type(line[1])==int):
            if not (line[1]>=0):
                return False
        
        # Controllo che il mese sia numerico
        if (line[1].isnumeric()):
            try:
                # In caso affermativo provo a convertirlo in intero
                line[1]=int(line[1])
            except Exception:
                return False
        else:
            return False

        
        # Verifico che '-' appartenga alla data cioè che sia nel formato corretto
        if ('-' in line[0]):
            # In caso affermativo divido la data
            lista_data_val=line[0].split('-')
        else:
            return False

        # Dopo aver diviso la data controllo che sia numerica
        for i,item in enumerate(lista_data_val):
            if not (lista_data_val[i].isnumeric()):
                return False
        
        # Verifico che il mese appartenga effettivamente ai mesi dell'anno
        if (int(lista_data_val[1]) not in range(1,13)):
            return False

        # Passati tutti i controlli la linea è validata
        return True

    # Metodo ausiliario che prepari da una linea una lista contenente le date per il metodo __duplicate_line__
    def __make_date_list__ (self,line,lista_data):

        if ('-' in line[0]):
            lista_data_make=line[0].split('-')
        else:
            return None
        
        for i,item in enumerate(lista_data_make):
            if (lista_data_make[i].isnumeric()):
                
                try:
                    lista_data_make[i]=int(lista_data_make[i])
                except Exception:
                    return None
                
            else:
                return None
            
        lista_data.append(lista_data_make)

    # Metodo ausiliario che dalla lista di date creata in precedenza verifica che siano in ordine e che non ci siano duplicati
    def __duplicate_line__(self,lista_data):

        
        if (len(lista_data)<=1):
            return None
            
            
        if (len(lista_data)>2):
            
            if (len(lista_data)==3):
                lista_data.pop(0)
                
            else:
                raise ExamException("Superata dimensione prestabilita per lista_data!")
            
        data1=lista_data[0]
        data2=lista_data[1]

        # Verifica che la data successiva nella lista lo sia anche come valore (o uguale) altrimenti le date sono furi ordine
        if (data2[0]>=data1[0]):
            # Se il valore dell'anno è uguale bisogna verificare che il mese sia successivo al precedente
            if (data2[0]==data1[0]):
                if not (data2[1]>data1[1]):
                    raise ExamException("Errore:Date duplicate o fuori ordine!")
        else:
            raise ExamException("Errore:Date fuori ordine!")
                
            
        
    def get_data(self):
        
        lista=[]
        lista_data=[]
        bool_line=True
        
        # Provo ad aprire il file
        try:
            file_csv=open(self.name,'r')
        except Exception:
            raise ExamException("Errore nell'apertura del file...")

        # Provo a leggerlo e inoltre così facendo salto l'intestazione
        try:
            file_csv.readline()
        except Exception:
            raise ExamException("Errore nella lettura del file...")

        # Ciclo che verificando e pulendo una per volta ogni linea crea la lista
        for line in file_csv:

            # Verifico che ',' appartenga alla linea cioè che il formato sia corretto altrimenti passo alla linea successiva
            if (',' in line):
                # In caso affermativo la divido
                line=line.split(',')
            else:
                continue

            # In base al formato considero tutto quello che viene dopo il secondo campo non di interesse quindi lo elimino
            line=line[0:2]
            
            # Pulisco ultimo elemento dall'carattere accapo
            line[-1]=line[-1].strip('\n')

            # Chiamo il metodo ausiliario visto in precedenza per ottenere un valore booleano che mi indica se la linea è valida
            bool_line=self.__validate_line__(line)
            
            # In caso affermativo procedo con i successivi controlli e in caso di buon esito aggiungo finalmente la linea alla lista da ritornare
            if (bool_line is True):
                self.__make_date_list__(line,lista_data)
                self.__duplicate_line__(lista_data)
                lista.append(line)

        file_csv.close()
        return lista

def detect_similar_monthly_variations(time_series, years):

    #verificare anche time_series?
        
    # Se years non è istanza di list alzo un eccezione
    if not isinstance(years,list):
        raise ExamException ("Errore: years non è istanza di list")
    
    if (len(years)!=2):
        raise ExamException ("Errore: la dimensione di years è diversa da 2")

    
    # Se il primo elemento di years è diverso da int verifico che sia numerico e in caso affermativo provo a convertirlo in int   
    if type(years[0])!=int:
        if (years[0].isnumeric()):
            try:
                years[0]=int(years[0])
            except Exception:
                raise ExamException ("Errore: almeno uno degli elementi di years non è di tipo numerico")

    # Stessa cosa per il secondo elemento
    if type(years[1])!=int:
        if (years[1].isnumeric()):
            try:
                years[1]=int(years[1])
            except Exception:
                raise ExamException ("Errore: almeno uno degli elementi di years non è di tipo numerico")
            
    # Adesso bisogna verificare che gli anni siano consecutivi:
    # Ritengo che anche se siano in ordine scambiato possano essere sanatizzati in quanto invertiti non assumono un significato diverso
    # Quindi utilizzo sort che li ordina in maniera crescente
    years.sort()
    
    # Verifica che gli elementi siano consecutivi
    if not (years[1]==(years[0]+1)):
        raise ExamException ("Errore: gli elementi di years non sono consecutivi")

    # Creo un dizonario che mi permetterà in seguito di poter accedere facilmente ai anni d'interesse
    dict_time_series={}
    # Creo una variabile di nome year che mi permetterà di aggiornare le chiavi del dizionario
    year=None
    
    for line in time_series:

        # Aspettandoci che a questo punto del programma la time_series è valida possiamo evitare di controllarla
        # Creiamo una variabile time che aumenta la leggibilità e contiene la data
        time=line[0].split('-')

        # Creiamo la variabile month che oltre che ad aumentare la leggibilità mi servirà come indice per l'assegnamento
        month=int(time[1])-1
        
        if (year is None):
            year=int(time[0])
            dict_time_series[year]=[]
            for i in range(1,13):
                dict_time_series[year].append(None)
            
        if (year!=int(time[0])):
            year=int(time[0])
            dict_time_series[year]=[]
            for i in range(1,13):
                dict_time_series[year].append(None)
        
        
        dict_time_series[year][month]=line[1]

    

    # Uso il metodo keys che crea una lista delle chiavi presenti all'interno del mio dizionario e verifico che l'anno vi appartenga
    if (years[0] not in dict_time_series.keys()):
        raise ExamException ("Errore: Anno in years non presente in time_series")
            
    if (years[1] not in dict_time_series.keys()):
        raise ExamException ("Errore: Anno in years non presente in time_series")

    # Creo la lista_confronto che quella che conterrà se la variazione sta in un intervallo di +-2
    lista_confronto=[]


    for i in range(0,11):

        # Verifica che nessuna coppia contenga un elemento nullo altrimenti non potendo essere valutata verra considerata Falsa
        if (dict_time_series[years[0]][i])==None or (dict_time_series[years[0]][i+1])==None:
            lista_confronto.append(False)
            continue 

        if (dict_time_series[years[1]][i])==None or (dict_time_series[years[1]][i+1])==None:
            lista_confronto.append(False)
            continue 
        
        # Calcolo la variazione per ogni anno
        year0_month_var=(dict_time_series[years[0]][i]) - (dict_time_series[years[0]][i+1])
        year1_month_var=(dict_time_series[years[1]][i]) - (dict_time_series[years[1]][i+1])

        # Calcoliamo la variazione tra i due anni
        if -2 <= ( year0_month_var - year1_month_var ) <= 2:
            lista_confronto.append(True)
        else:
            lista_confronto.append(False)
            
        
    
    return lista_confronto
        
    

    
    


time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

lista_confronto=detect_similar_monthly_variations(time_series,["1949","1950"])




for item in time_series:
    print(item)
    #for x in item:
        #print(type(x),end=" ")
    print()

for item in lista_confronto:
    print(item)
    
    print()