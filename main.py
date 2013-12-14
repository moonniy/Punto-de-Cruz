#!../bin/python

from bottle import route, run, template, request, abort
from crochet import Crochet
import re

KEY = re.compile("^[a-zA-z1-9\-_]+$")
VALUE = re.compile("^[\-_\w\d\s]*$")

nodes={
    "Monica": {
        "edad": 21,
        "Estudios": "universidad"
    },
    "Miguel": {
        "edad": 21,
        "Estudios": "universidad"
    }
}

relations = {
    "Novios": {
        "Nodos": ("Monica", "Miguel")
        #"atributes": {}
    }
}

db = Crochet()

@route("/invalidrequest")
def invalidrequest():
    abort(400, "Argumentos no validos")

@route('/index')
def index():
    return {"Base de datos":"minigrafos"}

@route("/searchnode")
def searchNodes():
    if request.query:
        query = {}
        for key, value in request.query.items():
            if KEY.search(key) and VALUE.search(value):
                query[key] = value

        bindList = ""
        nodes = db.getNode(query)
        if nodes != []:
            for tmpNode in nodes:
                bindList += "<ul>"
                for clave, valor in tmpNode.items():
                    bindList += template("<li>{{clave}}: {{valor}}</li>",
                                         clave=clave, 
                                         valor=valor)
                bindList += "</ul>"

            return {"nodes": nodes}
                
    abort(404, "Nodo inexistente")

    

@route("/searchrel/<relation>")
def searchRelation(relation):
    rel = db.getRelation(relation)
    if rel != {}:
        result = "<h1>Relacion %s </h1>" % relation
        for node in rel["relations"]:
            result += template("""
        <ul>
            <li>From: {{fromNode}}</li>
            <li>to: {{toNode}}</li>
            <li>direction: {{direction}}
            <li>Properties: {{properties}}
        </ul>
        """, 
            fromNode=node["from"],
            toNode=node["to"],
            direction=node["direction"],
            properties=node["properties"]
            )

        return rel

    abort(404, "Relacion inexistente")
 

@route('/writeRelation')
def writeRelation():
    if request.query:
        data = {}
        fromNode = None
        toNode = None
        relation = "None"
        direction = None
        

        for key, value in request.query.items():
            if KEY.search(key) and VALUE.search(value):
                needabort = False
                if key == "from":
                    fromNode = value
                elif key == "to":
                    toNode = value
                elif key == "name":
                    relation = value
                elif key == "direction" and value in ("unidirectional", "bidirectional"):
                    direction=value
                else:
                    data[key] = value
            else:
                needabort = True
                break

        if not needabort:
            result, sync = db.writeRelation(relation=relation,
                                            fromNode=fromNode,
                                            toNode=toNode,
                                            properties=data,
                                            direction=direction)

            return "<h1>la relacion %s se ha creado correctamente<h1>" % result

        abort(400, "Argumentos no validos")
                             

        

@route('/writeNode')
def writeNode():
    """
    Ejemplo de uso
        /test?nombre=casimiro&edad=35&sexo=Masculino

    Si no se pasan parametros se lanzara un codigo de error 400

    """
    if request.query:
        data = {}

        needabort = False

        for key, value in request.query.items():
            if KEY.search(key) and VALUE.search(value):
                data[key] = value
            else:
                needabort=True
                break

                
        if not needabort:
            id, sync = db.writeNode(data)
            return '<h1>insercion con id. %s satisfactoria </h1>' % id["_id"]

    abort(400, "Argumentos no validos")

run(host="localhost", port=8080, reloader=True)
