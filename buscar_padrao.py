#usr/bin/python3

import sys
import subprocess
from colorama import Fore, Style

#testado no banco cn só pegou o SSTI e o SQLI verificar dps

# Função para buscar padrões específicos nas URLs
def buscar_padroes_arquivo(arquivo):
    # Padrões a serem buscados e suas cores correspondentes
    padroes = {
        "CORS": (r'cors', Fore.RED),
        "SSRF": (r'ssrf', Fore.BLUE),
        "SSTI": (r'ssti', Fore.GREEN),
        "SQLI": (r'sqli', Fore.YELLOW),
        "RCE": (r'rce', Fore.MAGENTA)
    }

    try:
        # Executar o GF para cada padrão e capturar a saída
        for nome, (padrao, cor) in padroes.items():
            # Executar o comando GF para buscar o padrão
            resultado = subprocess.run(['gf', padrao, arquivo], capture_output=True, text=True)

            # Dividir as linhas de saída e imprimi-las com a cor correspondente
            for linha in resultado.stdout.splitlines():
                print(f"{cor}{nome}: {Style.RESET_ALL}{linha}")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado ao executar o GF: {e}")
        sys.exit(1)

# Verificar se o nome do arquivo foi fornecido como argumento
if len(sys.argv) != 2:
    print("Uso: python buscar_padroes.py <nome_do_arquivo>")
    sys.exit(1)

# Nome do arquivo contendo as URLs
arquivo_urls = sys.argv[1]

# Chamar a função para buscar padrões no arquivo
buscar_padroes_arquivo(arquivo_urls)
                                          