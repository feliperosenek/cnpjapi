import os
import time
import requests
from tqdm import tqdm

# URL base
BASE_URL = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2024-11/"
# Lista de arquivos a serem baixados
FILES = [
    "Cnaes.zip",
    "Empresas0.zip", "Empresas1.zip", "Empresas2.zip", "Empresas3.zip", "Empresas4.zip",
    "Empresas5.zip", "Empresas6.zip", "Empresas7.zip", "Empresas8.zip", "Empresas9.zip",
    "Estabelecimentos0.zip", "Estabelecimentos1.zip", "Estabelecimentos2.zip", 
    "Estabelecimentos3.zip", "Estabelecimentos4.zip", "Estabelecimentos5.zip", 
    "Estabelecimentos6.zip", "Estabelecimentos7.zip", "Estabelecimentos8.zip", 
    "Estabelecimentos9.zip", "Motivos.zip", "Municipios.zip", "Naturezas.zip", 
    "Paises.zip", "Qualificacoes.zip", "Simples.zip", "Socios0.zip", "Socios1.zip", 
    "Socios2.zip", "Socios3.zip", "Socios4.zip", "Socios5.zip", "Socios6.zip", 
    "Socios7.zip", "Socios8.zip", "Socios9.zip"
]

# Diretório para salvar os arquivos
DOWNLOAD_FOLDER = "downloads"

# Tamanho do chunk para download (8 KB)
CHUNK_SIZE = 8192


def create_folder(folder_path):
    """Cria o diretório se ele não existir."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def download_file(file_name, url, save_path):
    """
    Faz o download de um arquivo da URL especificada.
    :param file_name: Nome do arquivo
    :param url: URL do arquivo para download
    :param save_path: Caminho onde o arquivo será salvo
    """
    print(f"Baixando: {file_name}")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Tamanho do arquivo para barra de progresso
    total_size = int(response.headers.get('content-length', 0))

    with open(save_path, "wb") as file, tqdm(
        desc=file_name,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            file.write(chunk)
            progress_bar.update(len(chunk))


def main():
    """Executa o processo de download dos arquivos."""
    create_folder(DOWNLOAD_FOLDER)

    for file_name in FILES:
        # Define a URL completa e o caminho para salvar o arquivo
        url = f"{BASE_URL}{file_name}"
        save_path = os.path.join(DOWNLOAD_FOLDER, file_name)

        # Verifica se o arquivo já foi baixado
        if os.path.exists(save_path):
            print(f"'{file_name}' já existe. Pulando download.")
            continue

        # Realiza o download do arquivo
        try:
            download_file(file_name, url, save_path)
            print(f"'{file_name}' foi baixado com sucesso.\n")
        except requests.RequestException as e:
            print(f"Erro ao baixar '{file_name}': {e}")
        except Exception as e:
            print(f"Erro inesperado com '{file_name}': {e}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time = time.time() - start_time
    print(f"\nTodos os downloads concluídos em {elapsed_time:.2f} segundos.")
