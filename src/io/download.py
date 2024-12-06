import os
import time
import zipfile
import requests
from src.io.get_files_dict import main as get_files_dict
from src.io.utils import create_folder, display_progress

n = 8192  # Tamanho do chunk de download
dict_status = {}  # Dicionário para armazenar o status do download


def main():  # pragma: no cover
    dict_files_dict = get_files_dict()
    create_folder(dict_files_dict['folder_ref_date_save_zip'])
    started_at = time.time()
    list_needs_download = []

    for tbl in dict_files_dict.keys():
        _dict = dict_files_dict[tbl]
        # Ignora a chave 'folder_ref_date_save_zip', que não é um dicionário
        if isinstance(_dict, str):
            continue

        for file in _dict.keys():
            link_to_download = _dict[file]['link_to_download']
            path_save_file = _dict[file]['path_save_file']
            file_size_bytes = _dict[file]['file_size_bytes']

            # Verifica se o arquivo já foi baixado
            try:
                # Tenta abrir o arquivo como um ZIP
                archive = zipfile.ZipFile(path_save_file, 'r')
                print(f"'{path_save_file:60}' - [OK] already downloaded")
                continue
            except zipfile.BadZipFile:
                print(f"'{path_save_file:60}' - [NO] corrupted, needs re-download")
                list_needs_download.append(path_save_file)
            except FileNotFoundError:
                print(f"'{path_save_file:60}' - [NO] not found, needs download")
                list_needs_download.append(path_save_file)

            # Inicia o download do arquivo
            download_file(file, link_to_download, path_save_file, file_size_bytes, started_at)

    # Mensagens finais
    print('\n' * 3)
    if list_needs_download:
        for e, _file in enumerate(list_needs_download, 1):
            print(f"[{e:3}]/[{len(list_needs_download):3}] downloaded file: {_file}")
    else:
        print("All files are already downloaded")


def download_file(file_name, link_to_download, path_save_file, file_size_bytes, started_at):  # pragma: no cover
    """
    Faz o download de um arquivo para o sistema local.
    :param file_name: Nome do arquivo
    :param link_to_download: Link para download do arquivo
    :param path_save_file: Caminho onde o arquivo será salvo
    :param file_size_bytes: Tamanho esperado do arquivo em bytes
    :param started_at: Tempo inicial do processo
    """
    print(f"Starting download: {file_name}")
    with requests.get(link_to_download, stream=True) as r:
        r.raise_for_status()
        current_file_downloaded_bytes = 0
        with open(path_save_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=n):
                f.write(chunk)
                current_file_downloaded_bytes += len(chunk)
                running_time_seconds = time.time() - started_at
                speed = current_file_downloaded_bytes / running_time_seconds if running_time_seconds > 0 else 0
                eta = (file_size_bytes - current_file_downloaded_bytes) / speed if running_time_seconds > 0 else 0
                global dict_status
                dict_status[file_name] = {
                    'total_completed_bytes': current_file_downloaded_bytes,
                    'file_size_bytes': file_size_bytes,
                    'pct_downloaded': current_file_downloaded_bytes / file_size_bytes,
                    'started_at': started_at,
                    'running_time_seconds': running_time_seconds,
                    'speed': speed,
                    'eta': eta,
                }
                display_progress(dict_status, started_at=started_at, source='Download', th_to_display=0.05)

    print(f"Download completed: {file_name}")


if __name__ == '__main__':
    main()
