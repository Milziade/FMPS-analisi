import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
import json
import openpyxl
# -----------------------------------
# |             FMPS                |
# -----------------------------------

def prepare_df(PATH):
    '''df = pd.read_excel(PATH, skiprows=17, sheet_name=0, engine="openpyxl")     # Legge l'excel e skippa le righe inutili
    df = df.drop(0)     # Toglie la riga "elapsed time"
    df = df.iloc[:, :33]    # Seleziona le colonne con le dimensioni (df.iloc(riga_inizio, riga_fine, colonna_inizio, colonna_fine))
    df.rename(columns={"Channel Size [nm]:": "Time"}, inplace=True)     # Cambia il nome da "Channel Size" a "Time"
    print(df.head(5))
    df.set_index("Time", inplace=True)      # Cambiamo l'index con il tempo
    print(df.head(10))
    return df'''

    aa = pd.read_excel(PATH, sheet_name=0).iloc[:, :33]
    columns = ["Time", 6.04, 6.98, 8.06, 9.31, 10.8, 12.4, 14.3, 16.5, 19.1, 22.1, 25.5, 29.4, 34.0, 39.2, 45.3, 52.3, 60.4, 69.8, 80.6, 93.1, 107.5, 124.1, 143.3, 165.5, 191.1, 220.7, 254.8, 294.3, 339.8, 392.4, 453.2, 523.3]

    time_start = aa.iloc[0, 1]
    title = aa.iloc[1, 1]

    for i in range(20):
        if aa.iloc[i, 0] == "Elapsed [s]":
            p = i
    df = aa.iloc[i-1:, :]
    df.columns = columns
    df.set_index(df["Time"], inplace=True)
    df = df.drop("Time", axis=1)
    for i in columns[1:]:
        if df[i].dtype != "float64":
            df[i] = df[i].astype("float64")
    time_exp = len(df)/60
    return df, title, time_start, time_exp

def get_lines(df : pd.DataFrame):
    fig = px.line(df, title="Lines")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    

def get_heatmap(df : pd.DataFrame):
    '''
    Consente di ottenere una heatmap delle dimensioni vs. tempo
    '''
    fig = px.imshow(df.T, origin='lower', title="Heatmap")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def get_3D(df : pd.DataFrame):
    ''' Grafico 3D'''
    z = df.values
    fig = go.Figure(data=[go.Surface(z=z, x=df.columns, y=df.index)])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return json.loads(graphJSON)


def total_graph(df : pd.DataFrame):
    '''
    Ritorna la concentrazione totale per ogni istante campionato 
    (somma di tutti i valori per un dato indice)
    '''
    total = [0]
    x = [0] + list(df.index)
    for i in range(len(df)):
        total.append(sum(df.iloc[i]))
    fig = px.line(x=x, y=total, title="Concentrazione totale vs tempo")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def total_conc_bin(df: pd.DataFrame):
    '''
    Ritorna la concentrazione totale per ogni canale
    '''
    tot = []
    x = [str(i) for i in df.columns]
    for col in df.columns:
        tot.append(df[col].sum())
    fig = px.bar(x=x, y=tot, title="Concentrazione totale vs canale")
    '''fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.columns, y=tot,
                    mode='lines+markers',
                    name='lines+markers'))'''
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# -----------------------------------
# |             GRIMM               |
# -----------------------------------

def GRIMM_df(PATH):
    with open(PATH) as f:
        raw = f.read().splitlines()
    raw = raw[12:]  # Skippiamo le prime 12 righe di cui non ci interessa nulla
    A = []
    for i in raw:
        '''Creiamo una lista di liste che formeranno le nostre righe'''
        x = i.split("\t")[1:]
        A.append(x)
    df = pd.DataFrame(A)
    df = df.rename(columns=df.iloc[0]).loc[1:]
    for i in df.columns:
        '''Se le nostre colonne non sono di tipo float non possiamo plottare'''
        if df[i].dtype != "float64":
            df[i] = df[i].astype("float64")
    return df


def GRIMM_lines(df : pd.DataFrame):
    fig = px.line(df, title="Lines", labels={"index": "Tempo", "value": "Intensità"})
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    

def GRIMM_heatmap(df : pd.DataFrame):
    fig = px.imshow(df.T, origin='lower', title="Heatmap")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def GRIMM_3D(df : pd.DataFrame):
    z = df.values
    col = df.columns
    x = [i.split()[0] for i in col]
    print(x)
    y = list(df.index)
    return x, y, z


def GRIMM_total(df : pd.DataFrame):
    '''
    Ritorna la concentrazione totale per ogni istante campionato 
    (somma di tutti i valori per un dato indice)
    '''
    total = []
    for i in range(len(df)):
        total.append(sum(df.iloc[i]))
    fig = px.line(x=df.index, y=total, title="Concentrazione totale vs tempo", labels={"index": "Tempo", "value": "Intensità"})
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def GRIMM_total_conc_bin(df: pd.DataFrame):
    '''
    Ritorna la concentrazione totale per ogni canale
    '''
    tot = []
    for col in df.columns:
        tot.append(df[col].sum())
    #fig = px.line(x=df.columns, y=tot, title="Concentrazione totale vs canale")
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.columns, y=tot,
                    mode='lines+markers',
                    name='lines+markers'))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON