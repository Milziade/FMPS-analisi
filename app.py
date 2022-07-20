from functions import *
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='', 
        static_folder='templates/static',
        template_folder='templates')       # initialising the flask app
app.config["ALLOWED_FILE_EXTENSIONS"] = ["XLSX", "DAT"]

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':            # check if the method is post
        f = request.files['file']             # get the file from the files object
        # We only want files with a . in the filename
        if not "." in f.filename:
            return "Sicuro di aver scelto il file giusto?"
        # Split the extension from the filename
        ext = f.filename.rsplit(".", 1)[1]
        # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
        if ext.upper() not in  app.config["ALLOWED_FILE_EXTENSIONS"]:
            return "<h1>Formato file non supportato! Si può usare solo .xlsx o .dat</h1>"
    
        f = request.files['file']             # get the file from the files object
        f.save(secure_filename(f.filename))   # this will secure the file
        if ext.upper() == "DAT":
            if f.filename.rsplit(".", 1)[0][-2:] == "-C":
                current_path = os.getcwd()
                print(secure_filename(f.filename))
                df = GRIMM_df(current_path + "/" + secure_filename(f.filename))        # Ottiene il Dataframe per il GRIMM
                data_lines = GRIMM_lines(df)
                data_heatmap = GRIMM_heatmap(df)
                x, y, z = GRIMM_3D(df)
                total_conc = GRIMM_total(df)
                tot_size_bin = GRIMM_total_conc_bin(df)

                os.remove("{}/{}".format(os.getcwd(), secure_filename(f.filename)))     # Si elimina il file caricato
                return render_template("result.html",  data_lines=data_lines, data_heatmap=data_heatmap, 
                    x=x, y=y, z=z, total_conc=total_conc, tot_size_bin=tot_size_bin)
            else:
                return "Devi caricare il file che finisce per -C"

        if ext.upper() == "XLSX":
            df, title, time_start, time_exp = prepare_df(f)      # Ottieni il dataframe
            print(f"{time_exp=}")
            data_lines = get_lines(df)      # Grafico a linee
            data_heatmap = get_heatmap(df)  
            data_3d = get_3D(df)        # Ottieni il dict dove ci sono tutti i dati
            total_conc = total_graph(df)    # Concentrazione totale vs tempo
            tot_size_bin = total_conc_bin(df)   # Concentrazione totale vs canale

            x = [float(i) for i in data_3d['data'][0]['x']]
            y = [float(i) for i in data_3d['data'][0]['y']]
            z = [i for i in data_3d['data'][0]['z']]
            
            os.remove("{}/{}".format(os.getcwd(), secure_filename(f.filename)))     # Si elimina il file caricato
            return render_template("result.html", title=title, time_start=time_start, time_exp=time_exp,
                data_lines=data_lines, data_heatmap=data_heatmap,
                x=x, y=y, z=z, total_conc=total_conc, tot_size_bin=tot_size_bin)
         
    return render_template("home.html")

if __name__ == '__main__':
   app.run(debug=True) # running the flask app in debug mode
