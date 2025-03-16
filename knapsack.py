from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, value

class Objeto:
    """
    Clase que representa un objeto con un peso y un valor.
    """
    def __init__(self, peso, valor):
        self.peso = peso
        self.valor = valor
    
    def __str__(self):
        return f"Objeto(peso={self.peso}, valor={self.valor})"

class Mochila:
    """
    Clase que representa una mochila con una capacidad máxima y una lista de objetos.
    """
    def __init__(self, capacidad_maxima, objetos):
        self.capacidad_maxima = capacidad_maxima
        self.objetos = objetos
    
    def resolver(self):
        """
        Resuelve el problema de la mochila utilizando programación entera.
        Retorna los objetos seleccionados, el valor total y el peso total.
        """
        # Crear el problema de optimización (maximización)
        prob = LpProblem("Problema_Mochila", LpMaximize)
        
        # Crear variables de decisión binarias (0 o 1)
        # x[i] = 1 si el objeto i se incluye en la mochila, 0 en caso contrario
        x = [LpVariable(f"x{i}", 0, 1, 'Binary') for i in range(len(self.objetos))]
        
        # Función objetivo: maximizar el valor total
        prob += sum(self.objetos[i].valor * x[i] for i in range(len(self.objetos)))
        
        # Restricción: el peso total no debe exceder la capacidad máxima
        prob += sum(self.objetos[i].peso * x[i] for i in range(len(self.objetos))) <= self.capacidad_maxima
        
        # Resolver el problema
        prob.solve()
        
        # Verificar si se encontró una solución óptima
        if LpStatus[prob.status] != 'Optimal':
            return [], 0, 0
        
        # Obtener los resultados
        objetos_seleccionados = []
        valor_total = 0
        peso_total = 0
        
        for i in range(len(self.objetos)):
            if value(x[i]) == 1:
                objetos_seleccionados.append(self.objetos[i])
                valor_total += self.objetos[i].valor
                peso_total += self.objetos[i].peso
        
        return objetos_seleccionados, valor_total, peso_total

def resolver_mochila(capacidad_maxima, objetos):
    """
    Función que resuelve el problema de la mochila.
    Recibe la capacidad máxima de la mochila y una lista de objetos.
    Retorna los objetos seleccionados, el valor total y el peso total.
    """
    mochila = Mochila(capacidad_maxima, objetos)
    return mochila.resolver()

# Ejemplo de uso
if __name__ == "__main__":
    # Datos de entrada
    capacidad_maxima = 10
    objetos = [
        Objeto(peso=5, valor=10),
        Objeto(peso=4, valor=40),
        Objeto(peso=6, valor=30),
        Objeto(peso=3, valor=50)
    ]
    
    # Resolver el problema
    objetos_seleccionados, valor_total, peso_total = resolver_mochila(capacidad_maxima, objetos)
    
    # Mostrar resultados
    print("Objetos seleccionados:")
    for obj in objetos_seleccionados:
        print(obj)
    print(f"Valor total: {valor_total}")
    print(f"Peso total: {peso_total}")

