# FMPS and GRIMM data analysis
I used to work with these two instruments during my bachelor thesis and I thought it could be useful share with you what I made to make data more readable by using graphs and charts.

## How to use this repo
Clone the repository or download the source code
```bash
git clone https://github.com/Milziade/FMPS-analisi.git
```
Move to the FMPS-analisi folder, open your terminal and type:
```
pip install -r requirements.txt
```
Now it's ready to use!

## What does this repo do?
This repo helps you visualize data obtained from [FMPS](https://tsi.com/products/particle-sizers/fast-particle-sizer-spectrometers/fast-mobility-particle-sizer-(fmps)-3091/) analysis and [GRIMM](https://amof.ac.uk/instruments/grimm-optical-particle-counter-1-108/) analysis.
After starting your local server, you can open your browser and navigate to http://127.0.0.1:5000/.

**Upload your file and submit.**

In the next page you will see acquisition span, date and time and the file name. You will also find single-size line, heatmap, 3D visualization and total concentration v. time.

You can zoom and download the graphs without any problem thanks to Plotly library
