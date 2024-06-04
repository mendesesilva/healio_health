import os
import shutil
from datetime import datetime

def backup_data(src_dir, backup_dir):
    """
    Realiza o backup dos dados de um diretório para outro, adicionando um timestamp ao nome do backup.

    Args:
        src_dir (str): Diretório de origem dos dados.
        backup_dir (str): Diretório de destino dos dados.
    """
    # Cria um timestamp para o nome do backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'backup_{timestamp}')
    
    # Realiza a cópia dos dados
    shutil.copytree(src_dir, backup_path)
    print(f'Dados copiados para {backup_path}')

if __name__ == '__main__':
    src_dir = 'data/uploads'
    backup_dir = 'data/backups'
    
    # Garante que o diretório de backup exista
    os.makedirs(backup_dir, exist_ok=True)
    
    # Realiza o backup dos dados
    backup_data(src_dir, backup_dir)
