import sys
import random
import turtle
import numpy as np

class Vertice:
    def __init__(self, id_vertice, x ,y ,etiqueta):
        self.id_vertice = id_vertice
        self.x = x
        self.y = y
        self.etiqueta = etiqueta
        
class Arista:
    def __init__(self, cola, cabeza, peso=0.0):
        self.cola = cola
        self.cabeza = cabeza
        self.peso = peso
        
class Grafo:
    def __init__(self, data, tipo, representacion, vertices = None, aristas = None):
        if (vertices != None):
            self.vertices = vertices
        else:
            self.vertices = {}
        
        if (aristas != None):
            self.aristas = aristas
        else:
            self.aristas = {}

        self.data = data
        self.tipo = tipo
        self.representacion = representacion
        self.data_convertida = None
        self.set_vertices()
        self.set_aristas()
    
    def add_vertice(self, id_vertice):
        if id_vertice not in self.vertices:
            x = random.randrange(-250, 250, 40)
            y = random.randrange(-250, 250, 40)
            etiqueta = str(id_vertice)
            nuevo_vertice = Vertice(id_vertice, x, y, etiqueta)
            self.vertices[id_vertice] = nuevo_vertice
            print("añadido vertice", etiqueta)
    
    def add_arista(self, cola, cabeza, peso = None):
            nueva_arista = Arista(cola, cabeza)
            self.aristas[(cola, cabeza)] = nueva_arista
            #self.aristas.append(nueva_arista)
            print("añadido arista", cola, cabeza)
            if (self.tipo == "P"):
                nueva_arista.peso = peso

    def set_vertices(self):
      if (self.representacion == "MA" or self.representacion == "MI"):
        for vertice in range(self.data.shape[0]):
          self.add_vertice(vertice)
          
      elif (self.representacion == "LA"):
        for vertice in self.data:
          self.add_vertice(vertice)


    def set_aristas(self):
      if(self.representacion == "MA"):
        for cola in range(self.data.shape[0]):
          for cabeza in range(self.data.shape[1]):
              if self.data[cola,cabeza] != 0.0:
                  #print(cola, cabeza)
                  peso = self.data[cola,cabeza]
                  self.add_arista(cola, cabeza, peso)
      
      elif (self.representacion == "LA"):
        for cola in self.data:
          for cabeza in self.data[cola]:
            print(cola, cabeza)
            peso = 0.0
            self.add_arista(cola, cabeza, peso)
      
      elif (self.representacion == "MI"):
        for arista in range(self.data.shape[1]):
          cola = None
          cabeza = None
          peso = 0.0
          for vertice in range(self.data.shape[0]):
            if (self.data[vertice, arista] == 0.0):
              continue
            else:
              if (cola == None): 
                cola = vertice
                print(cola)
              else:
                cabeza = vertice
                print(cabeza)
              if (cola != None and cabeza != None):
                self.add_arista(cola, cabeza, peso)
              
    
    def get_vertices_id(self):
        temp = []
        for vertice in self.vertices.keys():
            temp.append(vertice)
        return temp
  
    def get_aristas(self):
        temp = []
        for arista in self.aristas.keys():
            temp.append(arista)
        return temp
    
    def get_representacion(self):
        return self.representacion
    
    def get_tipo(self):
        return self.tipo
    
    def to_matriz_adyacencia(self):
      try:
        if (self.representacion != "MA"):
          col = row = len(self.vertices.keys())
          self.data_convertida = np.zeros((row, col))
          for arista in self.aristas.keys():
              self.data_convertida[arista] = 1
          return self.data_convertida
        else:
          return self.data
      except IndexError:
        return "Oops, Error"
        print("Oops, error")
    
    def to_lista_adyacencia(self):
      try:
        if (self.representacion != "LA"):
          self.data_convertida = {}
          for arista in self.aristas.keys():
              if (arista[0] not in self.data_convertida):
                  self.data_convertida[arista[0]] = [arista[1]]
              else:
                  self.data_convertida[arista[0]].append(arista[1])
          return self.data_convertida
        else:
          return self.data
      except IndexError:
        return "Oops, Error"
        print("Oops, Error")
    
    def to_matriz_incidencia(self):
      try:
        if(self.representacion != "MI"):
          row = len(self.vertices.keys())
          col = int(len(self.aristas.keys())/2)
          self.data_convertida = np.zeros((row, col))
          contador = 0
          lista_temp = []
          for arista in self.aristas.keys():
              lista_temp.append(arista)
              if (arista[0] == arista[1]):
                  temp_arr = np.zeros((row, 1))
                  temp_arr[arista[0]] = 2
                  print(temp_arr)
                  self.data_convertida = np.append(self.data_convertida, temp_arr, axis=1)
              elif ((arista[1], arista[0]) not in lista_temp):
                  self.data_convertida[(arista[0], contador)] = 1
                  self.data_convertida[(arista[1], contador)] = 1
                  contador += 1
          return self.data_convertida
        else:
          return self.data
      except IndexError:
        return "Oops, Error"
        print("Oops, error")


    def get_data(self):
      if (self.representacion == "LA"):
        items_data = self.data.items()
        temp = np.array(list(items_data), dtype = object)
        return temp
      else:
        return self.data

    def dibujar_grafo(self):
      try:
        #screen = turtle.RawTurtle(canvas)
        turtle.speed(100)
        for vertice in self.vertices:
            vertex = self.vertices[vertice]
            x = vertex.x
            y = vertex.y
            print(vertex, "x: ", x,"y: ", y)
            turtle.penup()
            turtle.goto(x,y-20)
            
            turtle.pendown()
            turtle.fillcolor("blue")
            turtle.begin_fill()
            turtle.circle(10)
            turtle.end_fill()
            turtle.penup()
            turtle.goto(x+2,y+11)
            turtle.write(vertex.etiqueta,align="center",font=("Arial",12,"bold"))
            
        for arista in self.aristas.values():
            turtle.width(2)
            if(arista.cola != arista.cabeza):
                x1 = float(self.vertices[arista.cola].x)
                y1 = float(self.vertices[arista.cola].y)
                x2 = float(self.vertices[arista.cabeza].x)
                y2 = float(self.vertices[arista.cabeza].y)
                print(x1, y1, x2, y2)
                
                turtle.penup()
                turtle.goto(x1,y1-10)
                turtle.pendown()
                turtle.setheading(turtle.towards(x2, y2))
                turtle.goto(x2,y2-10)

                if (self.tipo == "D"):
                  turtle.width(3)
                  turtle.left(45)
                  turtle.backward(20)
                  turtle.forward(20)
                  turtle.right(90)
                  turtle.backward(20)
                
                
            else:
                x1 = float(self.vertices[arista.cola].x) 
                y1 = float(self.vertices[arista.cola].y)
                print(x1, y1)
                turtle.penup()
                turtle.goto(x1,y1 - 20)
                turtle.pendown()
                turtle.circle(15, 340)
                
            if self. tipo == "P" and arista.peso != 0.0:       
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                turtle.penup()
                turtle.goto(x,y)
                turtle.write(str(arista.peso),align="center",font=("Arial",12,"normal"))

      except Exception as e:
        print("Grafo:GD-LA-0003-003 ó GN-LA-0002-003")
