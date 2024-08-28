import random
import math

#criptografia el gamal
#chaves publicas: e1 (inteiro alatório), e2 (e1^d mod p), p (primo grande aleatório)
#chave privada: d (inteiro aleatório)
#fórmula p/ criptografar:
#cifra 1 -> e1^r mod p
#cifra 2 -> mensagem * (e2^r mod p)
#fórmula p/ descriptografar:
#mensagem -> c2*((c1^d)^-1) mod p

#função p/ exponenciação modular, calcula de forma mais eficiente por serem números grandes
#b -> base
#p -> potencia
#m -> modulo
#r -> resultado

def mod_exp(b, p, m, r):
    if p > 0:
      if p % 2 == 1:
        r = (r * b) % m
      b = (b * b) % m
      p //= 2
      return mod_exp(b, p, m, r) #RECURSIVO
    return r

def gerar_chave():
  p = 426405985185585738245912460581 #numero primo grande
  d = random.randint(2, p-2) #chave privada aleatoria
  e1 = random.randint(2, p) #primeira parte p criptografar, inteiro aleatorio
  e2 = mod_exp(e1,d,p,1) #segunda parte p criptografar, calcular e1^d mod p
  return p, d, e1, e2

#transforma m para ascii
def para_ascii(m):
    m_cod = [ord(char) for char in m]
    return m_cod

#criptografar a mensagem usando a chave publica
def criptografar(p, e1, e2, m):
  r = random.randint(2, p-2) #inteiro aleatorio para exponenciar
  c1 = mod_exp(e1,r,p,1) #primeira cifra
  c2 = m * (mod_exp(e2,r,p,1)) #segunda cifra
  return c1, c2

#descriptografar a mensagem (c2*((c1^d)^-1) mod p)
#para calcular ^-1 é calculado o inverso multiplicativo de c1
def descriptografar(p, d, c1, c2):
  s = mod_exp(c1,d,p,1)
  s_inverso = mod_exp(s,p-2,p,1) #inverso multiplicativo
  m = c2 * s_inverso % p
  return m

#etapa dps d descriptografar, transformar nos numeros ascii dnv e formar o texto original
def para_string(cod_ascii):
    letra = chr(cod_ascii)
    return letra

def main():
  m = str(input()) #mensagem
  m_cod = para_ascii(m) #mensagem dps de mudar para ascii
  p, d, e1, e2 = gerar_chave()

  print("Mensagem: ", m)
  print("Chave pública (p, e1, e2): ", {p},{e1},{e2})
  print("Chave privada (d): ", {d})

#criptografando o texto----------------------
  c = [[0, 0] for _ in range(len(m))] #matriz para armazenar cifra 1 e cifra 2 de cada letra

  for i in range(len(m)):
     c1, c2 = criptografar(p, e1, e2, m_cod[i]) #criptografa letra por caracter e retorna 2 cifras
     c[i][0] = c1 #armazena cifra 1
     c[i][1] = c2 #armazena cifra 2

  #tira os c1 e c2 das chaves
  cifras_concat = [f"{cifra[0]}{cifra[1]}" for cifra in c]

  #junta tudo em uma string
  c_concat = "".join(cifras_concat)

  #printa todo o texto criptografado
  print("Texto criptografado: ", c_concat)

  #descriptografando o texto----------------------
  m_descript = [[0] for _ in range(len(m))]

  for i in range(len(m)):
     m_descod = descriptografar(p, d, c[i][0], c[i][1]) #retorna o código ascii de cada caracter
     m_descript[i] = para_string(m_descod) #retorna o caracter

  txt_descript = '' #variavel qualquer para armazenar o texto original
  for i in range(len(m)):
     txt_descript += str(m_descript[i]) #transformando em string e concatenando


  print("Mensagem descriptografada:",txt_descript)

if __name__ == '__main__':
  main()