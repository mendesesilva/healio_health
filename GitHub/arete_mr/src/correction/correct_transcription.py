import languagetool

def correct_transcription(transcript):
    """
    Corrige a transcrição do texto usando o LanguageTool.

    Args:
        transcript (str): Transcrição original do áudio.

    Returns:
        str: Transcrição corrigida.
    """
    # Inicializa o cliente do LanguageTool para o português
    tool = languagetool.LanguageTool('pt-BR')
    
    # Verifica o texto em busca de erros
    matches = tool.check(transcript)
    
    # Aplica as correções sugeridas
    corrected_text = languagetool.correct(transcript, matches)
    
    return corrected_text

if __name__ == '__main__':
    import argparse

    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Corrige uma transcrição de texto usando o LanguageTool.')
    parser.add_argument('transcript', type=str, help='Transcrição original do áudio.')

    args = parser.parse_args()
    
    # Corrige a transcrição fornecida
    corrected_transcript = correct_transcription(args.transcript)
    print('Transcrição corrigida:')
    print(corrected_transcript)
