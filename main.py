from bottle import route, run, template, request, abort

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

@route("/invalidrequest")
def invalidrequest():
    abort(400, "Argumentos no validos")

@route('/index')
def index():
    return "<h1>Base de datos  minigrafos</h1>"

@route("/searchnode/<usuario>")
def searchNodes(usuario):
    if usuario in nodes.keys():
        return template("""
        <h1>{{nombre}}</h1>
        <ul>
            <li>Edad: {{edad}}</li>
            <li>Estudios {{estudio}}</li>
        </ul>
        """, 
        nombre=usuario, 
        edad=nodes[usuario]["edad"],
        estudio=nodes[usuario]["Estudios"])

    abort(404, "Nodo inexistente")

    

@route("/searchrel/<relation>")
def searchRelation(relation):
    result = "<h1>Relacion %s </h1>" % relation
    if relation in relations.keys():
        for node in relations[relation]["Nodos"]:
            result += template("""
        <h2>{{nombre}}</h2>
        <ul>
            <li>Edad: {{edad}}</li>
            <li>Estudios {{estudio}}</li>
        </ul>
        """, 
        nombre=node, 
                           edad=nodes[node]["edad"],
                           estudio=nodes[node]["Estudios"])
        return result

    abort(404, "Relacion inexistente")
 
@route('/test')
def test():
    """
    Ejemplo de uso
        /test?nombre=casimiro&edad=35&sexo=Masculino

    Si no se pasan parametros se lanzara un codigo de error 400

    """
    if request.query:
        attributes = "<ul>"
        for key,value in request.query.items():
            attributes += template("<li>{{key}} : {{value}}</li>", key=key, value=value)
        attributes += "</ul>"
        return attributes

    abort(400, "Argumentos no validos")

run(host="localhost", port=8080, reloader=True)
