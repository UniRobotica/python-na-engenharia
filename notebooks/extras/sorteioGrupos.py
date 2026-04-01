import random

grupos = []
for i in range(7):
    nome = input(f"Digite o nome do grupo {i+1}: ")
    grupos.append(nome)

questoes = ["Questão 1", "Questão 2", "Questão 3", "Questão 4", "Questão 5", "Questão 6", "Questão 7"]

random.shuffle(questoes)

print("\nResultado do sorteio:\n")
for grupo, questao in zip(grupos, questoes):
    print(f"{grupo} -> {questao}")