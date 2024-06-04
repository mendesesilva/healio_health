import logging
import os

def setup_logging():
    # Garante que o diretório de logs exista
    os.makedirs('logs', exist_ok=True)
    
    # Configura o logging
    logging.basicConfig(filename='logs/execution.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Log configurado com sucesso.')

if __name__ == '__main__':
    setup_logging()
    logging.info('Exemplo de mensagem de log.')
