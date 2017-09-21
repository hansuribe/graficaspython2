from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':  # Something is being submitted
        x1 = str(request.form['x1'])
        x2 = str(request.form['x2'])
        y1 = str(request.form['y1'])
        y2 = str(request.form['y2'])
        z = str(request.form['z'])
    else:
        x1, x2, y1, y2, z = 'teff', 'mass', 'Vmag', 'par', 'logg'
    df = pd.read_table('stars.csv')
    columns = df.columns.values
    df = df.loc[:, list(set([x1, x2, y1, y2, z]))].dropna(axis=0)

    fig, ax = plt.subplots(2, 2, figsize=(10, 8), sharex='col', sharey='row')
    points = ax[0, 0].scatter(df[x1], df[y1], c=df[z], alpha=0.6)
    points = ax[1, 0].scatter(df[x1], df[y2], c=df[z], alpha=0.6)
    points = ax[0, 1].scatter(df[x2], df[y1], c=df[z], alpha=0.6)
    points = ax[1, 1].scatter(df[x2], df[y2], c=df[z], alpha=0.6)
    ax[1, 0].set_xlabel(x1)
    ax[1, 1].set_xlabel(x2)
    ax[0, 0].set_ylabel(y1)
    ax[1, 0].set_ylabel(y2)

    plugins.connect(fig, plugins.LinkedBrush(points))
    plot = fig_to_html(fig)
    return render_template('plot.html', plot=plot, columns=columns,
                           x1=x1, x2=x2, y1=y1, y2=y2, z=z)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
