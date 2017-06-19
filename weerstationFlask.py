from flask import Flask
from flask import render_template
from DbClass import  DbClass
import datetime
import pygal
import os

app = Flask(__name__)

temperaturen = []
lichtsterktes = []
luchtdrukken = []
luchtvochtigheden = []
tijdstippen = []

@app.route('/')
def weerstation():
    graph_t = pygal.Line()
    graph_h = pygal.Line()
    graph_p = pygal.Line()
    graph_l = pygal.Line()
    graph_t.title = 'Temperatuur'
    graph_h.title = 'Luchtvochtigheid'
    graph_p.title = 'Luchtdruk'
    graph_l.title = 'Lichtsterkte'
    DB_layer = DbClass()
    tijdstip = datetime.now()
    tijdstippen.append(tijdstip)
    temperatuur = DB_layer.getDataFromDatabaseMetVoorwaarde(1)
    licht = DB_layer.getDataFromDatabaseMetVoorwaarde(2)
    luchtdruk = DB_layer.getDataFromDatabaseMetVoorwaarde(3)
    luchtvochtigheid = DB_layer.getDataFromDatabaseMetVoorwaarde(4)
    temperaturen.append(temperatuur)
    lichtsterktes.append(licht)
    luchtdrukken.append(luchtdruk)
    luchtvochtigheden.append(luchtvochtigheid)
    graph_t.x_labels = tijdstippen
    graph_h.x_labels = tijdstippen
    graph_p.x_labels = tijdstippen
    graph_l.x_labels = tijdstippen
    graph_data_t = graph_t.render_data_uri()
    graph_data_h = graph_h.render_data_uri()
    graph_data_p = graph_p.render_data_uri()
    graph_data_l = graph_l.render_data_uri()
    hoogsteT = max(temperaturen)
    laagsteT = min(temperaturen)
    return render_template('weer.html',temperatuur=temperatuur, pressure=luchtdruk, humidity = luchtvochtigheid, licht=licht, tijdstip=tijdstip, graph_data_h=graph_data_h, graph_data_l=graph_data_l, graph_data_p=graph_data_p, graph_data_t=graph_data_t, hoogsteT=hoogsteT, laagsteT=laagsteT)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error/404.html", error=error)


if __name__ == '__main__':
    port = int(os.environ.get("PORT",8080))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)
