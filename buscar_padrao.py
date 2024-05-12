#!/usr/bin/python3

import sys
import subprocess
from colorama import Fore, Style

def print_help():
    print("Uso: python buscar_padroes.py [opção] <nome_do_arquivo>\n")
    print("Descrição: Este script busca padrões específicos em URLs\n de um arquivo usando o GF.")
    print("Argumentos:")
    print("       <nome_do_arquivo>: O caminho para o arquivo contendo as\n URLs a serem analisadas.")
    print("\nOpções:")
    print("  -h, --help: Mostra esta mensagem de ajuda.")
    print("  -p PADRAO, --padrao PADRAO: Especifica um padrão de busca.\n Padrões disponíveis: CORS, SSRF, SSTI, SQLI, RCE.")
    sys.exit(0)

# Função para buscar padrões específicos nas URLs
def buscar_padroes_arquivo(arquivo, padrao=None):
    # Padrões a serem buscados e suas cores correspondentes
    padroes = {
        "CORS": (r'cors', Fore.RED),
        "SSRF": (r'ssrf', Fore.BLUE),
        "SSTI": (r'ssti', Fore.GREEN),
        "SQLI": (r'sqli', Fore.YELLOW),
        "RCE": (r'rce', Fore.MAGENTA)
    }

    # Se um padrão específico foi especificado, usar apenas esse padrão
    if padrao:
        padroes = {padrao.upper(): padroes[padrao.upper()]}

    try:
        # Abrir o arquivo e ler o conteúdo
        with open(arquivo, 'r') as file:
            conteudo = file.read()

        # Executar o GF para cada padrão e capturar a saída
        for nome, (padrao, cor) in padroes.items():
            # Executar o comando GF para buscar o padrão no conteúdo do arquivo
            resultado = subprocess.run(['gf', padrao], input=conteudo, capture_output=True, text=True)

            # Dividir as linhas de saída e imprimi-las com a cor correspondente
            for linha in resultado.stdout.splitlines():
                print(f"{cor}GF {nome}: {Style.RESET_ALL}{linha}")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado ao ler o arquivo: {e}")
        sys.exit(1)

# Verificar se o script foi chamado com a opção de ajuda
if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
    print_help()

# Verificar se o usuário especificou um padrão de busca
padrao = None
if len(sys.argv) > 2 and sys.argv[1] in ("-p", "--padrao"):
    padrao = sys.argv[2]
    if padrao.upper() not in ("CORS", "SSRF", "SSTI", "SQLI", "RCE"):
        print("Erro: Padrão de busca inválido. Padrões disponíveis: CORS, SSRF, SSTI, SQLI, RCE.")
        sys.exit(1)

# Nome do arquivo contendo as URLs
arquivo_urls = sys.argv[-1]

# Chamar a função para buscar padrões no arquivo
buscar_padroes_arquivo(arquivo_urls, padrao)
