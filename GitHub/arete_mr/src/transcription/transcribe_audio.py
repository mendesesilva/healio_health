import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage

def transcribe_audio(file_name, bucket_name):
    """
    Transcreve um arquivo de áudio armazenado no Google Cloud Storage usando o Google Cloud Speech-to-Text.

    Args:
        file_name (str): Nome do arquivo de áudio no bucket do Google Cloud Storage.
        bucket_name (str): Nome do bucket no Google Cloud Storage.
    
    Returns:
        str: Transcrição do áudio.
    """
    # Inicializa o cliente do Google Cloud Storage
    storage_client = storage.Client()
    gcs_uri = f'gs://{bucket_name}/{file_name}'

    # Inicializa o cliente do Google Cloud Speech-to-Text
    speech_client = speech.SpeechClient()

    # Configurações avançadas para a transcrição
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pt-BR",
        enable_automatic_punctuation=True,
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
        model="default",
        use_enhanced=True,  # Usa o modelo avançado para melhor qualidade
        speech_contexts=[{
            "phrases": ["ansiedade", "depressão", "psicoterapia", "medicação", "terapia cognitivo-comportamental", "tratamento", "síndrome do pânico"],
            "boost": 20.0
        }]
    )

    # Executa a transcrição
    operation = speech_client.long_running_recognize(config=config, audio=audio)
    print('Esperando pela transcrição...')
    response = operation.result(timeout=540)  # Aguarda até 9 minutos (540 segundos)

    # Compila a transcrição
    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript + '\n'

    # Salva a transcrição no bucket de destino
    transcript_blob = storage_client.bucket(bucket_name).blob(f'transcripts/{file_name}.txt')
    transcript_blob.upload_from_string(transcript)

    print(f'Transcrição concluída e salva em: gs://{bucket_name}/transcripts/{file_name}.txt')
    return transcript

if __name__ == '__main__':
    import argparse

    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Transcreve um arquivo de áudio do Google Cloud Storage.')
    parser.add_argument('file_name', type=str, help='Nome do arquivo de áudio no bucket do Google Cloud Storage.')
    parser.add_argument('bucket_name', type=str, help='Nome do bucket no Google Cloud Storage.')

    args = parser.parse_args()
    
    # Executa a função de transcrição com os argumentos fornecidos
    transcribe_audio(args.file_name, args.bucket_name)
