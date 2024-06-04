from google.cloud import language_v1
import json

def analyze_text(text):
    """
    Realiza a análise de sentimentos e a extração de entidades de um texto usando o Google Cloud Natural Language.

    Args:
        text (str): Texto a ser analisado.
    
    Returns:
        dict: Resultados da análise, incluindo sentimentos e entidades.
    """
    # Inicializa o cliente do Google Cloud Natural Language
    client = language_v1.LanguageServiceClient()

    # Prepara o documento para análise
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analisa o sentimento do texto
    sentiment_response = client.analyze_sentiment(request={'document': document})
    sentiment = sentiment_response.document_sentiment

    # Extrai entidades do texto
    entities_response = client.analyze_entities(request={'document': document})
    entities = entities_response.entities

    # Formata os resultados
    analysis_results = {
        'sentiment': {
            'score': sentiment.score,
            'magnitude': sentiment.magnitude
        },
        'entities': []
    }

    for entity in entities:
        analysis_results['entities'].append({
            'name': entity.name,
            'type': language_v1.Entity.Type(entity.type_).name,
            'salience': entity.salience,
            'metadata': entity.metadata,
            'mentions': [mention.text.content for mention in entity.mentions]
        })

    return analysis_results

if __name__ == '__main__':
    import argparse

    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Analisa um texto, realizando análise de sentimentos e extração de entidades.')
    parser.add_argument('text', type=str, help='Texto a ser analisado.')

    args = parser.parse_args()
    
    # Executa a função de análise com o texto fornecido
    analysis_results = analyze_text(args.text)
    
    # Imprime os resultados da análise em formato JSON
    print(json.dumps(analysis_results, indent=2, ensure_ascii=False))
