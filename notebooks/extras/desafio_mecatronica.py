"""
DESAFIO DA MECATRÔNICA — ROBÔ EXPLORADOR
O código fica neste arquivo; os termos ficam em um arquivo JSON separado.

Como usar:
  python desafio_mecatronica.py
  python desafio_mecatronica.py banco_mecatronica_5000.json
  python desafio_mecatronica.py outro_banco.json

Sem argumento, usa banco_mecatronica.json.
O JSON deve ficar na mesma pasta do código ou ser informado pelo caminho.
Formato de cada item:
  {
    "palavra": "sensor",
    "tema": "Sensores",
    "nivel": 1,
    "dicas": ["Dica geral", "Dica intermediária", "Dica específica"]
  }

- "tema" e "nivel" são opcionais (padrões: "Geral" e 2).
- "dicas" deve conter pelo menos uma dica.
- Níveis: 1 = básico, 2 = intermediário, 3 = avançado.
- O robô começa cada rodada com seis unidades de energia virtual.
- Uma tentativa incorreta consome uma unidade e libera a próxima dica,
  quando ainda houver dicas disponíveis.
- Letras repetidas e entradas inválidas não consomem energia.
- O conceito é revisado ao final de cada rodada.
"""

import json
import os
import random
import sys
import unicodedata

MAX_ERROS = 6
ARQ_BANCO_PADRAO = "banco_mecatronica.json"
NIVEIS = {1: "Básico", 2: "Intermediário", 3: "Avançado"}


# ==========================================================
# CARGA E VALIDAÇÃO DO BANCO (JSON)
# ==========================================================
def pasta_do_script():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:  # ambientes como Jupyter/Colab não definem __file__
        return os.getcwd()


def resolver_caminho(arquivo):
    """Procura o arquivo como informado e, depois, na pasta do script."""
    if os.path.isabs(arquivo) or os.path.exists(arquivo):
        return arquivo
    return os.path.join(pasta_do_script(), arquivo)


def validar_item(item):
    """Retorna o item normalizado ou None se for inválido."""
    if not isinstance(item, dict):
        return None
    palavra = str(item.get("palavra", "")).strip()
    dicas = item.get("dicas")
    if not palavra or not any(c.isalpha() for c in palavra):
        return None
    if (
        not isinstance(dicas, list)
        or not dicas
        or not all(isinstance(d, str) and d.strip() for d in dicas)
    ):
        return None
    try:
        nivel = int(item.get("nivel", 2))
    except (TypeError, ValueError):
        nivel = 2
    return {
        "palavra": palavra,
        "tema": str(item.get("tema", "Geral")).strip() or "Geral",
        "nivel": nivel if nivel in NIVEIS else 2,
        "dicas": [d.strip() for d in dicas],
    }


def carregar_banco(arquivo):
    caminho = resolver_caminho(arquivo)
    try:
        with open(caminho, encoding="utf-8") as f:
            bruto = json.load(f)
    except FileNotFoundError:
        sys.exit(
            f"Arquivo de banco não encontrado: {caminho}\n"
            f"Coloque '{arquivo}' na mesma pasta do código ou informe o caminho."
        )
    except (json.JSONDecodeError, OSError) as e:
        sys.exit(f"Não foi possível ler o banco '{caminho}': {e}")

    if not isinstance(bruto, list):
        sys.exit("O JSON do banco deve ser uma lista de objetos.")

    banco, descartados = [], 0
    for item in bruto:
        v = validar_item(item)
        if v:
            banco.append(v)
        else:
            descartados += 1

    if not banco:
        sys.exit("Nenhum termo válido encontrado no banco.")
    if descartados:
        print(f"Aviso: {descartados} item(ns) inválido(s) ignorado(s).")
    print(f"Banco carregado de {os.path.basename(caminho)}: {len(banco)} termos.")
    return banco


# ==========================================================
# TEXTO
# ==========================================================
def normalizar(texto):
    """Minúsculas e sem acentos (para comparar letras)."""
    d = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in d if unicodedata.category(c) != "Mn")


def so_letras(texto):
    return "".join(c for c in normalizar(texto) if c.isalpha())


# ==========================================================
# MENU DE SELEÇÃO (tema e nível)
# ==========================================================
def escolher_filtros(banco):
    temas = sorted({i["tema"] for i in banco})
    print("\nTemas disponíveis:")
    print(f"  0. Todos ({len(banco)} termos)")
    for k, t in enumerate(temas, 1):
        qtd = sum(1 for i in banco if i["tema"] == t)
        print(f"  {k}. {t} ({qtd})")
    esc = input("Escolha um tema (número, Enter = todos): ").strip()
    tema = (
        temas[int(esc) - 1]
        if esc.isdigit() and 1 <= int(esc) <= len(temas)
        else None
    )

    print("\nNíveis: 1 = Básico, 2 = Intermediário, 3 = Avançado")
    esc = input("Escolha um nível (1-3, Enter = todos): ").strip()
    nivel = int(esc) if esc in ("1", "2", "3") else None

    filtrado = [
        i
        for i in banco
        if (tema is None or i["tema"] == tema)
        and (nivel is None or i["nivel"] == nivel)
    ]
    if not filtrado:
        print("Nenhum termo com esse filtro. Usando todos.")
        filtrado = banco
    print(f"\n{len(filtrado)} termos no sorteio.")
    return filtrado


# ==========================================================
# PAINEL DE ENERGIA DO ROBÔ
# ==========================================================
def mostrar_energia(erros):
    """Mostra a reserva virtual de energia da rodada."""
    restantes = max(0, min(MAX_ERROS, MAX_ERROS - erros))
    bateria = "■ " * restantes + "□ " * (MAX_ERROS - restantes)
    print("\n🤖 ROBÔ EXPLORADOR")
    print(f"🔋 Energia da rodada: [{bateria.strip()}] {restantes}/{MAX_ERROS}")


def mostrar_palavra(palavra, certas):
    saida = []
    for ch in palavra:
        if ch.isalpha():
            saida.append(ch if normalizar(ch) in certas else "_")
        elif ch == " ":
            saida.append("/")
        else:
            saida.append(ch)
    return " ".join(saida)


def dicas_completas(item):
    """Dicas do banco mais duas dicas automáticas ao final."""
    letras = [c for c in item["palavra"] if c.isalpha()]
    return list(item["dicas"]) + [
        f"Começa com a letra '{letras[0].upper()}'.",
        f"Termina com a letra '{letras[-1].upper()}'.",
    ]


def revisar_conceito(item):
    """Retoma as dicas para transformar a rodada em revisão do conteúdo."""
    print("\nRevisão do conceito:")
    print("Termo:", item["palavra"])
    for i, dica in enumerate(item["dicas"], 1):
        print(f"  {i}. {dica}")


def aviso_nova_dica(erros, dicas):
    """Anuncia uma dica apenas quando ela realmente será liberada."""
    if erros < MAX_ERROS and erros < len(dicas):
        return " Nova dica liberada."
    return ""


# ==========================================================
# RODADA
# ==========================================================
def jogar(item):
    palavra = item["palavra"]
    alvo = so_letras(palavra)
    dicas = dicas_completas(item)
    letras_alvo = set(alvo)

    certas, erradas = set(), set()
    erros = 0

    print("\n========== DESAFIO DA MECATRÔNICA ==========")
    print(f"Tema: {item['tema']}   |   Nível: {NIVEIS.get(item['nivel'], item['nivel'])}")
    print(f"O termo tem {len(alvo)} letras.")
    print("Use as dicas para descobrir o termo e ajudar o robô a concluir a missão.")
    print("Cada tentativa incorreta usa uma unidade de energia virtual.")

    while erros < MAX_ERROS:
        mostrar_energia(erros)

        print("\nDICAS:")
        for i in range(min(erros + 1, len(dicas))):
            print(f"  {i + 1}. {dicas[i]}")

        print("\nTermo:", mostrar_palavra(palavra, certas))
        if erradas:
            print("Letras já investigadas e ausentes:", " ".join(sorted(erradas)))

        if letras_alvo <= certas:
            print("\n🎉 MISSÃO CONCLUÍDA! Termo descoberto.")
            revisar_conceito(item)
            return True

        bruto = input("\nLetra (ou o termo inteiro): ")
        tentativa = so_letras(bruto)

        if not tentativa:
            print("Digite uma letra ou o termo. A energia continua a mesma.")
            continue

        # Termo inteiro
        if len(tentativa) > 1:
            if tentativa == alvo:
                print("\n🎉 MISSÃO CONCLUÍDA! Termo descoberto.")
                revisar_conceito(item)
                return True
            erros += 1
            print("Esse ainda não é o termo." + aviso_nova_dica(erros, dicas))
            continue

        # Letra
        if tentativa in certas or tentativa in erradas:
            print("Essa letra já foi investigada. A energia continua a mesma.")
            continue

        if tentativa in letras_alvo:
            certas.add(tentativa)
            print("Letra encontrada!")
        else:
            erradas.add(tentativa)
            erros += 1
            print("Essa letra não aparece no termo." + aviso_nova_dica(erros, dicas))

    mostrar_energia(MAX_ERROS)
    print("\nA energia desta rodada terminou. Vamos revisar o conceito!")
    revisar_conceito(item)
    return False


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================
def main():
    arquivo = sys.argv[1] if len(sys.argv) > 1 else ARQ_BANCO_PADRAO
    banco = carregar_banco(arquivo)
    selecionados = escolher_filtros(banco)

    disponiveis = selecionados.copy()
    random.shuffle(disponiveis)  # sem repetição até esgotar o banco filtrado
    acertos = rodadas = 0

    while True:
        if not disponiveis:
            print("\nTodos os termos do filtro já apareceram. Embaralhando novamente.")
            disponiveis = selecionados.copy()
            random.shuffle(disponiveis)

        item = disponiveis.pop()
        rodadas += 1
        acertos += jogar(item)
        print(f"\nMissões concluídas: {acertos} em {rodadas} rodada(s).")

        if input("\nIniciar outra missão? (s/n): ").strip().lower() != "s":
            print("Até a próxima aula!")
            break


if __name__ == "__main__":
    main()
