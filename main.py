from bottle import route, run, template, request

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
    else:
        return "<h1>No existe usuario"
    

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

    return "<h1>No existe</h1>"
 
@route('/test/')
def test():
    a = int(request.GET.get("a"))
    b = float(request.GET.get("b"))
    c = request.GET.get("c").upper()
    return dict(a=a,b=b,c=c)

run(host="localhost", port=8080, reloader=True)
