import openai
import os
import json

# Configuração da API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

def structure_text(transcript):
    """
    Estrutura a transcrição de uma consulta médica em um prontuário médico detalhado usando o modelo GPT-4 da OpenAI.

    Args:
        transcript (str): Texto da transcrição a ser estruturado.
    
    Returns:
        str: Prontuário médico estruturado.
    """
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=f"""Você é um assistente de IA especializado em saúde mental. Sua tarefa é estruturar a seguinte transcrição de uma consulta médica em um prontuário médico detalhado.
        Aqui está a transcrição:

        {transcript}

        Por favor, apresente o prontuário médico abaixo.""",
        temperature=0.5,
        max_tokens=1500,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

    structured_text = response.choices[0].text.strip()
    return structured_text

if __name__ == '__main__':
    import argparse

    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Estrutura a transcrição de uma consulta médica em um prontuário médico detalhado usando GPT-4.')
    parser.add_argument('transcript', type=str, help='Texto da transcrição a ser estruturado.')

    args = parser.parse_args()
    
    # Executa a função de estruturação com o texto fornecido
    structured_text = structure_text(args.transcript)
    
    # Imprime o prontuário médico estruturado
    print(structured_text)
