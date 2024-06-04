import os
from google.cloud import storage
from src.upload.upload_audio import upload_file
from src.conversion.convert_audio import convert_to_wav
from src.transcription.transcribe_audio import transcribe_audio
from src.preprocessing.preprocess_text import preprocess_text
from src.analysis.analyze_text import analyze_text
from src.structuring.structure_text import structure_text

def integrate_modules(file_name, bucket_name):
    """
    Integra todos os módulos para processar um arquivo de áudio, transcrever, corrigir, analisar e estruturar o texto em um prontuário médico.

    Args:
        file_name (str): Nome do arquivo de áudio a ser processado.
        bucket_name (str): Nome do bucket no Google Cloud Storage onde os arquivos serão armazenados.
    """
    # Inicializa o cliente do Google Cloud Storage
    storage_client = storage.Client()

    # Define os caminhos locais para os arquivos
    upload_path = os.path.join('data/uploads', file_name)
    converted_path = os.path.join('data/uploads', 'converted_audio.wav')
    
    # Upload do arquivo de áudio
    upload_file(upload_path)
    print(f'Arquivo {file_name} carregado com sucesso.')

    # Converte o arquivo de áudio para WAV
    convert_to_wav(upload_path, converted_path)
    print(f'Arquivo {file_name} convertido para WAV.')

    # Transcreve o arquivo de áudio
    transcribed_text = transcribe_audio({'bucket': bucket_name, 'name': 'converted_audio.wav'}, None)
    print(f'Arquivo {file_name} transcrito com sucesso.')

    # Pré-processa o texto transcrito
    preprocessed_text = preprocess_text(transcribed_text)
    print('Texto pré-processado com sucesso.')

    # Analisa o texto pré-processado
    analysis_results = analyze_text(preprocessed_text)
    print('Texto analisado com sucesso.')
    
    # Estrutura o texto analisado em um prontuário médico
    structured_text = structure_text(preprocessed_text)
    print('Texto estruturado com sucesso.')

    # Salva o prontuário médico estruturado no bucket de destino
    structured_blob = storage_client.bucket(bucket_name).blob(f'structured/{file_name}.txt')
    structured_blob.upload_from_string(structured_text)
    print(f'Prontuário médico estruturado salvo em: gs://{bucket_name}/structured/{file_name}.txt')

if __name__ == '__main__':
    import argparse

    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Integra todos os módulos para processar um arquivo de áudio e gerar um prontuário médico estruturado.')
    parser.add_argument('file_name', type=str, help='Nome do arquivo de áudio a ser processado.')
    parser.add_argument('bucket_name', type=str, help='Nome do bucket no Google Cloud Storage onde os arquivos serão armazenados.')

    args = parser.parse_args()
    
    # Executa a função de integração com os argumentos fornecidos
    integrate_modules(args.file_name, args.bucket_name)
