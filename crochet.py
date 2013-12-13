from hashlib import md5
from datetime import datetime
import re

KEY = re.compile("^[a-zA-z1-9-_]+$")
VALUE = re.compile("^[\w\d\s]*$")

class Crochet:
    def __init__(self, path="/tmp/crochet/*"):

        if not self.concistency(path):
            self._Nodos = {
                "None":[]
                }
            self._Relations= {}
            
    def concistency(self, path):
        return False
    
    def CreateIndex(self, index):
        try:
            self._Nodos[index]
        except KeyError:
            self._Nodos[index] = []
            return True

        return False

    def writeNode(self, data, index="None", createIndex=False):
        newData = data.copy()
        
        if createIndex and not existIndex(index):
            estatusIndex = createIndex(index)

        try:
            key=self.getIndex(index)
            key.append(newData)
        except NonExistIndex:
            # key = md5(str(datetime.now())).hexdigest()
            # amm newData["_id"] = key
            self._Nodos[key].append(newData)

        sync = self.syncDataDisk()
        return ({"_id": index}, sync)
        

    def writeRelation(self, 
                      relation, 
                      fromNode=None, 
                      toNode=None,
                      properties={},
                      direction=None):
        if fromNode != None and toNode != None:
            uRelation = self.getRelation(relation)
            
            if uRelation == {}:
                uRelation = {
                    "name": relation,
                    "relations": []                   
                    }

            uRelation["relations"].append({
                    "from": fromNode,
                    "to": toNode,
                    "direction": direction,
                    "properties": properties
                    })

            self._Relations[relation] = uRelation
            
            sync = self.syncDataDisk()
            return ({'_id': relation}, sync)


    def getNode(self, properties, index=None, limit=1):
        Results = []
        if not index:
            for indexes in self._Nodos.values():
                for node in indexes:
                    append = True
                    for key in properties.keys():
                        try:
                            if node[key] != properties[key]:
                                append = False
                                break
                        except KeyError:
                            append = False
                            break                            

                    if append:
                        Results.append(node)
                        if len(Results) == limit:
                            return Results

        else:
            for node in getIndex(index):
                append = True
                for key in properties.keys():
                    try:
                        if node[key] != properties[key]:
                            append = False
                            break
                    except KeyError:
                        append = False
                        break


                if append:
                    Results.append(node)
                    if len(Results) == limit:
                        return Results
        
        return Results

    def getRelation(self, relation):
        if self.existRelation(relation):
            return self._Relations[relation]
        else:
            return {}


    def getIndex(self, node):
        try:
            localNode = self._Nodos[node]
        except KeyError:
            raise NonExistIndex(node)

        return localNode


    def existRelation(self, relation):
        try:
            self._Relations[relation]
        except KeyError:
            return False

        return True

    def existIndex(self, index):
        try:
            self.getIndex(index)
        except NonExistIndex:
            return False

        return True

    def syncDataDisk(self):
        pass


class SyncData(Exception):
    pass



class NonExist(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NonExistNode(NonExist):
    pass

class NonExistRelation(NonExist):
    pass

class NonExistIndex(NonExist):
    pass
        
class NotUniqueKey(Exception):
    def __init__(self, value):
        self.value = value
        

    def __str__(self):
        return repr(self.value)
