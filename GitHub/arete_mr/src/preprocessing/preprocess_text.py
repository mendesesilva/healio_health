import spacy

def preprocess_text(text):
    """
    Realiza o pré-processamento de um texto, incluindo limpeza, tokenização, lematização e remoção de stopwords.

    Args:
        text (str): Texto a ser pré-processado.
    
    Returns:
        str: Texto pré-processado.
    """
    # Carrega o modelo de língua portuguesa do SpaCy
    nlp = spacy.load('pt_core_news_sm')

    # Processa o texto
    doc = nlp(text)

    # Realiza a lematização, removendo pontuações e stopwords
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    
    # Junta os tokens em uma string única
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

if __name__ == '__main__':
    import argparse

    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Pré-processa um texto, realizando limpeza, tokenização, lematização e remoção de stopwords.')
    parser.add_argument('text', type=str, help='Texto a ser pré-processado.')

    args = parser.parse_args()
    
    # Executa a função de pré-processamento com o texto fornecido
    preprocessed_text = preprocess_text(args.text)
    print(preprocessed_text)
