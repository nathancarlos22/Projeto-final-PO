# -*- coding: utf-8 -*-
"""PO_finish.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xW4TUSMoATW0hqmCkde3hwXg81vACVOd
"""

import numpy as np

#!pip install ortools

"""# Lendo arquivo"""

path = 'Problema.txt'
arquivo = open(path,'r')
numeros = []

for linha  in arquivo:
  linha = linha.strip()
  numeros.append(linha)

arquivo.close()
numeros

x1 = numeros[0].split(' ') #Variaveis e restricoes
c = numeros[1].split(' ') #Coecicientes das variaveis na funcao objetivo

rest = len(numeros)-2 #Numeros de restrições
var = int(x1[0]) #Números de variáveis

a = [0]*rest #inicializando array com o numero de restricoes
b = [0]*rest 

for i in range(2, len(numeros)): #começando em dois pois oq vem depois da linha 2 sao as restricoes
    aa = numeros[i].split(' ')
    b[i-2] = aa[len(aa)-1]
    del(aa[len(aa)-1])
    a[i-2] = aa
print(a, b, c)

a = np.double( a )
b = np.double( b )
c = np.double( c )

print(a, b, c)

obj= 'Min'  

igualdade = 'MoreOrEqual'

"""# Adicionando no modelo"""

def create_data_model(A, B, C, num_vars, num_rest):
  data = {}
  data['constraint_coeffs'] = A
  data['bounds'] = B
  data['obj_coeffs'] = C
  data['num_vars'] = num_vars
  data['num_constraints'] = num_rest
  return data

data = create_data_model(a, b, c, var, rest)

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

infinity = solver.infinity()
x = {}

for j in range(data['num_vars']):
    x[j] = solver.NumVar(0, 1, 'x[%i]' % j) #Variáveis que pertencem ao conjunto entre 0 e 1

print("\n==== Solução inicial ====\n ")
print('\n\nNumero de variaveis =', solver.NumVariables())

if igualdade == 'MoreOrEqual':
  for i in range(data['num_constraints'] ): 
    constraint = solver.RowConstraint(data['bounds'][i], infinity, '')#limite inferior, superior e nome da restrição
    for j in range(data['num_vars']):
      constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j]) 

print('Numero de restriçoes =', solver.NumConstraints())

objective = solver.Objective()

for j in range(data['num_vars']):
    objective.SetCoefficient(x[j], data['obj_coeffs'][j])

if obj == 'Max':
  objective.SetMaximization() #Problema de maximização
  status = solver.Solve()

if obj == 'Min':
  objective.SetMinimization() #Problema de minimização
  status = solver.Solve()

solution_value = []
if status == pywraplp.Solver.OPTIMAL:
    print('\nValor ótimo = ', solver.Objective().Value())
    for j in range(data['num_vars']):
        print(x[j].name(), ' = ', x[j].solution_value())
        solution_value.append(x[j].solution_value()) 
    print()
    print('Problema resolvido em %f milliseconds' % solver.wall_time())
    print('Problema resolvido em %d nós' % solver.nodes())
else:
    print('Nao tem solucao otima.')

solution = (solution_value, solver.Objective().Value())

"""# Função para resolver cada restrição"""

#from __future__ import print_function
from ortools.linear_solver import pywraplp

def main (Data, index, b): #Main para fazer o branch

  solver = pywraplp.Solver('simple_mip_program',
                         pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  infinity = solver.infinity()
  x = {}

  for j in range(Data['num_vars']):
      x[j] = solver.NumVar(0, 1, 'x[%i]' % j) #Variáveis positivas entre 0 e 1
  
  print("\n==== Solução ====\n ")
  print('\n\nNumero de variaveis =', solver.NumVariables())
  
  for i in range(Data['num_constraints'] - 1 ): # -1 para nao add a ultima rest
    constraint = solver.RowConstraint(Data['bounds'][i], infinity, '')#limite inferior, superior e nome da restrição
    for j in range(Data['num_vars']):
      constraint.SetCoefficient(x[j], Data['constraint_coeffs'][i][j]) 
  
  y = solver.NumVar(0, 1, 'y')

  y = x[index]

  solver.Add(y == b)

  print('Numero de restriçoes =', solver.NumConstraints())

  objective = solver.Objective()
  
  for j in range(Data['num_vars']):
      objective.SetCoefficient(x[j], Data['obj_coeffs'][j])
  
  if obj == 'Max':
    objective.SetMaximization() #Problema de maximização
    status = solver.Solve()

  if obj == 'Min':
    objective.SetMinimization() #Problema de minimização
    status = solver.Solve()

  solution_value = []
  if status == pywraplp.Solver.OPTIMAL:
      print('\nValor ótimo = ', solver.Objective().Value())
      for j in range(Data['num_vars']):
          print(x[j].name(), ' = ', x[j].solution_value())
          solution_value.append(x[j].solution_value()) 
      print()
      print('Problema resolvido em %f milliseconds' % solver.wall_time())
      print('Problema resolvido em %d nós' % solver.nodes())
  else:
      print('Nao tem solucao otima.')

      
  return (solution_value, solver.Objective().Value())

"""# Adicionar uma restrição no modelo"""

def append_data_model (Data, index, b): #Adiciona ao modelo uma restrição
    if index == -1:
      return Data

    A = Data['constraint_coeffs']
    B = Data['bounds']
    C = Data['obj_coeffs']
    num_vars = Data['num_vars']
    num_rest = Data['num_constraints'] + 1

    data = {} #Criando outro data para nao alterar oq vir do parametro
    data['constraint_coeffs'] = A
    data['bounds'] = B
    data['obj_coeffs'] = C
    data['num_vars'] = num_vars
    data['num_constraints'] = num_rest

    #Dar um append na restrição indicando qual coeficiente do x é, se for x1, o array é [1 0 0]

    var_x = [0]*data['num_vars']
    x=[]

    for i in range(0, data['num_vars']):
      if i == index:
        var_x[index] = 1
        x.append(var_x)
        data['constraint_coeffs'] = np.append(A, x, axis=0)

    #Dar append no lado direito da igualdade
    data['bounds'] = np.append(B, b)

    return data

"""# Exemplo de quemo fica o modelo adicionando as restrições"""

data1 = append_data_model(data, 2, 0) #modelo, index da variavel que sera relaxada e o lado direito (bounds)
data2 = append_data_model(data, 2, 1)

print(data1)
print(data2)

main(data1, 2, 0)
main(data2, 2, 1)

"""# Árvore"""

class Tree(object):
    def __init__(self, solution, modelo, left=None, right=None):
        self.solution = solution
        self.modelo = modelo
        self.left = left
        self.right = right

"""# Verificar se a variável é um número inteiro"""

def isInt (string):
  t = True
  for i in range(len(string)):
    if string[i] == '.':
      
      j=i+1
      if j >=len(string):
        return t
      for j in range(j,len(string)):
        if int(string[j]) != 0:
          t = False
  return t

"""# Verificar integralidade e a menor distância entre as variáveis
- O valor abs da diminuição com o valor da variável
- retorna o indice da variável (para poder adicionar depois na restrição)
- se retornar -1 quer dizer q todos os valores são inteiros
"""

def Verifica_integralidade(Solution):
    episilon = 10e3; #colocando um valor grande para iniciar
    Index_Da_menor_dist = -1  # Se for -1 todos os x são inteiros

    # precisa verificar se os valores em x são inteiros e verificar se está próximo de 0.5

    for i in range(len(Solution)): #menor que 1 pois o ultimo é o valor de z
      if isInt(str(Solution[i])) == False: #Se for false, quer dizer que tem dígito
        distancia = abs(Solution[i] - 0.5)

        if distancia < episilon: #Se esse valor for menor do que oq já tem no episilon, coloca ele lá
          episilon = distancia
          Index_Da_menor_dist = i

    return Index_Da_menor_dist

"""# Pilha
- Na pilha é colocado a solução do dual e primal
- No momento da inserção da solução na pilha, precisa verificar:
      - Se tiver vazia, só insere
      - Se não tiver vazia, verifica se a solução é inteira (integralidade) e se a solução que já está lá é melhor que será inserida (limitante)
"""

#pip install pythonds

from pythonds.basic.stack import Stack
menosInfinity = -9999 
maisInfinity = 9999

class Pilha:
  def __init__(self):
    self.items = [[[], menosInfinity], [[], maisInfinity]] #DUAL e PRIMAL minimização

  def isEmpty(self):
    return self.items == [[[], menosInfinity], [[], maisInfinity]]
  
  def push(self, item):   
    
    vars = item[0]
    tamVars = len(vars)

    vAdd = item[1]
    dual = pilha.see()[0]
    primal = pilha.see()[1]

    if self.isEmpty() != True: #Se não tiver vazia
      t = -1
      for i in range(0, tamVars): #percorrer os x's
        if isInt(str(vars[i])) != True: #se tiver um NAO inteiro 
          t = 0
          break
      if t == 0 and vAdd >= dual[1] and vAdd != 0 or dual[1] == maisInfinity: #se o valor otimo for maior que o dual, adiciona      
        self.items.append(item)
        self.items.append(primal)
          
      if t == -1 and vAdd <= primal[1] and vAdd != 0 or primal[1] == menosInfinity: #se for inteiro e o valor for menor, add o primal "==infinity para caso seja infinito adicionar"
        self.items.append(dual)
        self.items.append(item)
      
    elif self.isEmpty() == True: #Se tiver vazia, adiciona 
      self.items.append(item)
      self.items.append(primal)
      
  def pop(self):
    return self.items.pop()

  def see(self):
    return (self.items[len(self.items)-2], self.items[len(self.items)-1])

pilha = Pilha()

"""# Exemplo como fica a pilha"""

pilha.see()

pilha.push([[0.75, 1.0, 0.0], 13.75]) #Adicioanndo um x's nao inteiros, adiciona no dual
print(pilha.see())

pilha.push([[1.0, 0.5000000000000001, 0.2499999999999999], 12.0]) #, caso a solução nao seja melhor que a que já tem nao adiciona no dual
print(pilha.see())

pilha.push([[0.5, 1, 18], 17]) #se a solucao do dual for melhor, adiciona
print(pilha.see())

pilha.push([[1, 1, 1], 5]) #se for com criterio de integralidade, adiciona no primal
print(pilha.see())

pilha.push([[1, 1, 1], 18]) #se for maior nao adiciona no primal
print(pilha.see())

pilha.push([[1, 1, 1], 1]) #se for menor adiciona no primal
print(pilha.see())

pilha = Pilha() #reinicializando a pilha
print(pilha.see())

"""# Adicionando lado direito e esquerdo da árvore"""

def AddArv(arv, data_left, data_right, index):
  solution_right = main(data_right, index, 1 )
  solution_left  = main(data_left, index, 0 )

  arv.left  = Tree( solution_left, data_left  ) 
  arv.right  = Tree( solution_right, data_right )

  pilha.push(solution_right)
  pilha.push(solution_left )

  print("\nNó pai\n ", arv.solution)
  print("\nLADO ESQUERDO:\n", arv.left.solution)
  print("LADO DIREITO: \n", arv.right.solution)

  print("Dual: %f Primal: %f\n" % (pilha.see()[0][1], pilha.see()[1][1]))

"""# Percorrendo a arvore"""

no = 0
def Profun (tree, no):
  no = no +1
  print("Nó %d" % (no))
  
  primal = pilha.see()[1][1]
  dual = pilha.see()[0][1]

  index = Verifica_integralidade(tree.solution[0])
  print(tree.solution[1])
  print(primal)
  print(dual)
  
    
  b_limite_para_cima  = ("%0.f") % tree.solution[0][index] #lado arredondado. se for 0.5 fica 1
  b_limite_para_baixo = ("%d"  ) % tree.solution[0][index] #lado inteiro. se for 0.5 fica 0

  data_left  = append_data_model(tree.modelo, int(index), int(b_limite_para_baixo ))
  data_right = append_data_model(tree.modelo, int(index), int(b_limite_para_cima ))

  AddArv(tree, data_left, data_right, index) #Adiciona o lado esquerdo e direito na arvore

  index_left = Verifica_integralidade(tree.left.solution[0])
  index_right = Verifica_integralidade(tree.right.solution[0])

  #Se o valor da solução for menor que o primal e maior que o dual, aprofunda
  if index_left != -1 and tree.left.solution[1] < primal and tree.left.solution[1]  >=dual:
    Profun (tree.left, no)

  if index_right != -1 and tree.right.solution[1] < primal and tree.right.solution[1] >= dual:
    Profun (tree.right, no)
  else :
    return 0

tree = Tree(solution, data)
pilha.push(tree.solution)
print(pilha.see())

print("======== Iniciando a árvore =========\n")
# Profun(tree)
Profun(tree, no)

solucao = pilha.see()
print("Solução que está na pilha = ")
print(solucao)
print()

print("Solução ótima: ")
x = solucao[1][0]
z = solucao[1][1]

for i in range(0,len(x)):
  print('x[%d] = %d' % (i, x[i]))

print("Solucao z = %d" % z)

