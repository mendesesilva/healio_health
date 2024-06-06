# Arete MR: Arquitetura

= SPEC-1: Arete MR - Sistema de Transcrição e Análise de Consultas Médicas
:sectnums:
:toc:

== Background

O projeto Arete MR surgiu da necessidade de médicos de melhorar a qualidade dos registros clínicos. A ferramenta visa automatizar a captura e transcrição de consultas médicas, aplicando análises detalhadas dos dados do paciente, e gerando um registro clínico estruturado e atualizado em tempo real. Com isso, busca-se garantir a continuidade do cuidado ao paciente e melhorar a personalização do tratamento, reduzindo o tempo gasto em tarefas administrativas e aumentando o tempo de interação direta com o paciente.

== Diagrama

![IMG_2624.png](Arete%20MR%20Arquitetura%2033c7bd7cd7f3441bb77223e5af3ab157/IMG_2624.png)

== Requirements

Os requisitos do sistema Arete MR são definidos com base na metodologia MoSCoW (Must have, Should have, Could have, Won't have):

- **Must have:**
    - Captura e transcrição automática de áudio de consultas médicas.
    - Correção automática e refinamento de transcrições.
    - Análise sintática, semântica e de sentimentos do texto transcrito.
    - Extração e normalização de entidades médicas.
    - Atribuição de códigos CID10.
    - Conformidade com as regulamentações da LGPD no Brasil e legislações canadenses para dados de saúde.
- **Should have:**
    - Diarização para identificar diferentes falantes (médico e paciente).
    - Interface de upload de áudio intuitiva e fácil de usar.
    - Monitoramento contínuo e logging centralizado.
- **Could have:**
    - Análises preditivas e de tendências ao longo do tempo.
    - Análises detalhadas de dados demográficos, estilo de vida, histórico familiar e adesão ao tratamento.
- **Won't have:**
    - Criação de um dashboard interativo (não é prioridade no momento).

== Method

=== Definição do Escopo do Projeto

Arete MR é um sistema inovador projetado para transcrever e analisar consultas médicas de maneira eficiente. Ele oferece funcionalidades distintas e úteis, como correção automática, aprimoramento de transcrição, e análise de sentimentos e entidades. A fim de realizar estas tarefas, o sistema emprega com eficácia os serviços e APIs do Google Cloud, além de modelos avançados de Inteligência Artificial, como o GPT-4.

=== Descrição da Arquitetura Geral

A ferramenta Arete MR adota uma arquitetura robusta baseada em serviços na nuvem. Esta arquitetura facilita a integração entre diferentes componentes, incluindo a captura de áudio, transcrição, análise de texto e geração de registros clínicos. A seguir, apresentamos uma descrição detalhada de cada módulo e as tecnologias que os compõem.

=== Detalhamento dos Módulos do Sistema

==== 1. Módulo de Upload de Áudio
**Objetivo:** Este módulo tem como finalidade capturar o áudio da consulta médica e configurar os parâmetros iniciais para transcrição.

- **Tecnologias Utilizadas:** Este módulo faz uso de várias tecnologias, incluindo a Google Cloud Language API, Google Cloud Speech-to-Text, e uma Página Wix.
- **Etapas do Processo:**
    1. **Upload do Áudio:** Esta etapa envolve a disponibilização de uma interface de upload de áudio para usuários na página Wix em arete.clinic/medical_record.
    2. **Conversão do Áudio:** Aqui, o áudio é convertido para o formato WAV, LINEAR16, caso ele não esteja nesse formato inicialmente.
    3. **Detecção do Idioma:** Usando a Google Cloud Language API, o idioma do áudio é detectado.
    4. **Configuração da Transcrição:** Com base no idioma detectado, os parâmetros de transcrição são configurados.
    5. **Diarização:** Nesta etapa, diferentes falantes no áudio, como o médico e o paciente, são identificados.

### Configuração Avançada do Google Cloud Speech-to-Text

```python

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage

def transcribe_audio(data, context):
    # Inicializa o cliente de armazenamento do Google Cloud
    storage_client = storage.Client()

    # Pega o bucket e o nome do arquivo do evento de dados
    bucket_name = data['bucket']
    file_name = data['name']

    # Gera a URI do Google Cloud Storage para o arquivo de áudio
    gcs_uri = f'gs://{bucket_name}/{file_name}'

    # Inicializa o cliente de Speech-to-Text do Google Cloud
    speech_client = speech.SpeechClient()

    # Configuração avançada para a transcrição
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
    response = operation.result(timeout=900)
    # Processa a resposta
    return response
```

==== 2. Módulo de Transcrição e Correção
**Objetivo:** Este módulo é responsável por transcrever o áudio para texto e aplicar correções ortográficas iniciais.

- **Tecnologias Utilizadas:** Para realizar estas tarefas, o módulo utiliza o Google Cloud Speech-to-Text e o OpenAI GPT-4.
- **Etapas do Processo:**
1. **Transcrição com Correção Ortográfica**
    - **Ferramenta:** Google Cloud Speech-to-Text
    - **Etapas:**
        1. **Conversão do Áudio para Texto:** Nesta etapa, o Google Cloud Speech-to-Text é utilizado para transcrever o áudio.
        2. **Correção Ortográfica e Pontuação:** O serviço do Google Cloud aplica automaticamente a correção ortográfica e a pontuação ao texto transcrito.
2. **Verificação de Qualidade e Melhorias pelo GPT-4**
    - **Ferramenta:** OpenAI GPT-4
    - **Etapas:**
        1. **Recebimento do Texto Transcrito:** Primeiro, o texto transcrito com as correções iniciais é recebido.
        2. **Verificação de Qualidade:** Depois, o GPT-4 é utilizado para verificar a qualidade do texto, identificando e corrigindo quaisquer falhas.
        3. **Refinamento do Texto:** Por fim, o texto é refinado para garantir coesão, coerência, clareza e estrutura.

### Configuração Avançada do GPT-4

```python

import openai

def refine_transcription(transcript):
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    prompt = (
        "Você é um assistente de IA especializado em saúde mental. Sua tarefa é refinar a seguinte transcrição de uma consulta médica, corrigindo erros gramaticais, "
        "melhorando a fluidez do texto e garantindo que ele seja claro e coerente. Preserve o conteúdo original, mas faça ajustes necessários para melhorar a qualidade do texto. "
        f"Transcrição Original: {transcript}"
    )
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1500,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )
    refined_transcript = response.choices[0].text.strip()
    return refined_transcript
```

==== 3. Módulo de Processamento do Texto
**Objetivo:** Este módulo tem como objetivo realizar a análise sintática e semântica, a extração de entidades médicas e não-médicas, e a normalização.

- **Tecnologias Utilizadas:** Este módulo utiliza diversas tecnologias, como SpaCy, MedCAT e Google Cloud Natural Language.
- **Etapas do Processo:**
1. **Análise Sintática e Semântica:** Aqui, a estrutura gramatical e as relações entre os tokens são identificadas. Além disso, o significado e o contexto das palavras e frases no texto refinado pelo GPT-4 são compreendidos.
2. **Extração de Entidades:** Nesta etapa, entidades nomeadas são identificadas (por exemplo: medicamentos, sintomas, diagnósticos).
3. **Normalização de Entidades:** As entidades reconhecidas são normalizadas utilizando bases de conhecimento como UMLS.
4. **Atribuição de CID10:** Aqui, CID10 principais e secundários são atribuídos ao quadro do paciente.

==== 4. Bifurcação do Texto
**Objetivo:** Enviar o texto processado para geração do registro clínico e para as análises detalhadas.

**Texto para Geração do Registro Clínico**

**Cópia do Texto para Módulo de Análises Detalhadas**

==== 5. Módulo de Geração do Registro Clínico
**Objetivo:** Criar um registro clínico detalhado e estruturado com base no texto processado.

**Tecnologias:** Google Cloud Functions, Firestore

**Etapas:**

1. **Geração do Registro Clínico:** Utilizar o texto processado para criar um registro clínico estruturado.
2. **Atualização Contínua:** Manter o registro clínico atualizado com cada nova consulta e análise.

==== 6. Módulo de Análises Detalhadas
**Objetivo:** Realizar análises detalhadas sobre o texto e dados do paciente, incluindo análises preditivas.

**Tecnologias:** Google Cloud Functions, SpaCy, MedCAT, modelos de ML customizados

**Etapas (paralelizadas):**

1. **Análise Demográfica Socioeconômica**
    - **Ferramenta:** Scripts customizados e APIs de dados demográficos (Census API)
    - **Etapas:**
        1. **Coleta de Dados:** Coletar dados demográficos e socioeconômicos do paciente.
        2. **Análise:** Analisar os dados coletados para contextualizar o paciente.
2. **Análise de Dados de Estilo de Vida**
    - **Ferramenta:** Scripts customizados
    - **Etapas:**
        1. **Coleta de Dados:** Coletar dados sobre hábitos alimentares, rotina de exercícios, consumo de substâncias.
        2. **Análise:** Analisar os dados coletados para entender o estilo de vida do paciente.
3. **Análise de Dados de Histórico Familiar**
    - **Ferramenta:** Scripts customizados
    - **Etapas:**
        1. **Coleta de Dados:** Coletar antecedentes familiares de doenças mentais, doenças crônicas, histórico de suicídio ou tentativas.
        2. **Análise:** Analisar os dados coletados para entender o histórico familiar do paciente.
4. **Análise de Adesão ao Tratamento**
    - **Ferramenta:** Scripts customizados
    - **Etapas:**
        1. **Coleta de Dados:** Coletar dados sobre frequência de consultas, cumprimento de prescrições, feedback sobre efeitos colaterais de medicamentos.
        2. **Análise:** Analisar os dados coletados para monitorar a adesão ao tratamento.
5. **Identificação de Padrões de Comportamento e Pensamentos**
    - **Ferramenta:** NLP Custom Models
    - **Etapas:**
        1. **Análise de Texto:** Identificar padrões recorrentes de comportamento, pensamentos e sintomas.

6. **Análise de Sentimentos**
- **Ferramenta:** Google Cloud Natural Language, TextBlob
- **Etapas:** 

1. **Avaliação Emocional:** Avaliar o tom emocional do texto transcrito e atribuir pontuações emocionais a diferentes segmentos.

7. **Exame do Estado Mental**
- **Ferramenta:** NLP Custom Models, Avaliação Psicológica
- **Etapas:**
1. **Avaliação Detalhada:** Avaliar orientação, memória, atenção, linguagem, juízo, insight e humor.
2. **Classificação e Resumo:** Classificar e resumir os resultados em um formato estruturado.

8. **Identificação e Classificação de Relações**
- **Ferramenta:** Transformers da Hugging Face
- **Etapas:**
1. **Extração de Relações:** Extrair relações entre entidades médicas (ex: sintomas associados a diagnósticos).
2. **Classificação de Relações:** Classificar as relações extraídas em categorias predefinidas.
9. **Análise de Redes Sociais e de Apoio**
- **Ferramenta:** NetworkX
- **Etapas:**
1. **Identificação de Rede:** Identificar e visualizar a influência e o apoio social das diferentes pessoas mencionadas no texto.
10. **Análise de Dados de Comunicação**
- **Ferramenta:** Análise de vídeo e áudio, NLP
- **Etapas:**
1. **Avaliação de Linguagem:** Avaliar a linguagem usada pelo paciente, tom de voz, expressões faciais e corporais (se capturados por vídeo).
11. **Análise de Rede Social Online**
- **Ferramenta:** Scripts customizados e APIs de redes sociais
- **Etapas:**
1. **Coleta de Dados:** Coletar dados de interações em redes sociais (com consentimento).
2. **Análise:** Analisar interações para identificar possíveis sinais de alerta ou padrões de comportamento.
12. **Análise de Dados Ambientais**
- **Ferramenta:** Scripts customizados e APIs de dados ambientais
- **Etapas:**
1. **Coleta de Dados:** Coletar dados sobre o ambiente de vida do paciente.
2. **Análise:** Analisar os dados coletados para entender o impacto ambiental na saúde do paciente.
13. **Análise de Coerência Textual**
- **Ferramenta:** CountVectorizer, Cosine Similarity
- **Etapas:**
1. **Verificação de Coerência:** Verificar a coerência e coesão das narrativas apresentadas no texto.
14. **Clusterização Semântica e Identificação de Tópicos**
- **Ferramenta:** UMAP, t-SNE, KMeans, DBSCAN
- **Etapas:**
1. **Agrupamento de Segmentos:** Agrupar segmentos de texto semelhantes utilizando técnicas de clusterização.
2. **Identificação de Tópicos:** Identificar tópicos ou temas recorrentes nas conversas.
15. **Análise de Tendências ao Longo do Tempo**
- **Ferramenta:** Scripts de análise temporal, Modelos de séries temporais
- **Etapas:**
1. **Monitoramento:** Avaliar as mudanças no estado mental e emocional ao longo do tempo.
16. **Análise de Eficácia de Intervenções**
- **Ferramenta:** Modelos preditivos e estatísticos
- **Etapas:**
1. **Comparação de Intervenções:** Comparar diferentes intervenções e seus impactos nos sintomas e no bem-estar do paciente.
17. **Análise de Co-ocorrências**
- **Ferramenta:** Scripts customizados
- **Etapas:**
1. **Identificação de Co-ocorrências:** Identificar co-ocorrências de sintomas, eventos e estados emocionais.
18. **Análise de Textura de Linguagem**
- **Ferramenta:** NLP Custom Models
- **Etapas:**
1. **Avaliação de Complexidade:** Avaliar a complexidade e riqueza da linguagem usada pelo paciente.
19. **Análise de Padrões de Comunicação**
- **Ferramenta:** Scripts customizados
- **Etapas:**
1. **Monitoramento de Comunicação:** Avaliar a frequência e padrões de comunicação do paciente.
20. **Análise de Riscos**
- **Ferramenta:** Modelos preditivos baseados em dados históricos e comportamentais
- **Etapas:**
1. **Avaliação de Riscos:** Avaliar fatores de risco para condições graves como suicídio ou automutilação.

==== 7. Módulo de Alimentação do Banco de Dados
**Objetivo:** Armazenar os dados processados e realizar análises contínuas.

**Tecnologias:** Google Cloud Firestore, Google BigQuery

**Etapas (paralelizadas):**

1. **Validação Automática e Revisão Manual:** Validar a integridade e a consistência do texto pós-processamento. Permitir que um profissional revise e ajuste o texto antes de salvar no banco de dados.
2. **Armazenamento e Análise Contínua:** Inserir os dados processados no banco de dados. Realizar análises contínuas e treinar modelos preditivos para prever comportamentos e recomendar intervenções.

==== 8. Módulo de Geração do Texto Estruturado para o Prontuário Eletrônico
**Objetivo:** Criar um registro clínico detalhado e estruturado com base nos dados analisados.

**Tecnologias:** Google Cloud Functions, Google Cloud Firestore

**Etapas:**

1. **Personalização do Modelo:** Adaptar os modelos para considerar o histórico médico e comportamental do paciente.
2. **Geração do Prontuário:** Gerar um texto estruturado com todas as informações relevantes extraídas e analisadas.
3. **Anonimização e Segurança de Dados:** Garantir que todos os dados do paciente sejam protegidos. Implementar medidas de segurança para manter a privacidade dos dados.

=== Tecnologias Utilizadas

Google Cloud Speech-to-Text: Transcrição de áudio em texto.

GPT-4: Melhoria na transcrição e correção automática.

Google Cloud Natural Language: Análise sintática, semântica, e de sentimentos.

Google Cloud Storage: Armazenamento de arquivos de áudio e transcrições.

Google Cloud Functions: Execução de funções de processamento.

Google Cloud Pub/Sub: Comunicação assíncrona entre serviços.

Google Cloud Firestore: Armazenamento de dados estruturados.

Google Cloud Scheduler: Agendamento de tarefas periódicas.

Google Cloud Logging e Monitoring: Monitoramento e logging centralizado.

SpaCy: Análise sintática e semântica.

MedCAT: Extração e normalização de entidades médicas.

NetworkX: Análise de redes sociais e de apoio.

TextBlob: Análise de sentimentos.

UMAP, t-SNE, KMeans, DBSCAN: Clusterização e identificação de tópicos.

CountVectorizer, Cosine Similarity: Análise de coerência textual.

Modelos de ML customizados: Identificação de padrões de comportamento e análise de riscos.

== Implementation

=== Etapas de Implementação

A implementação da ferramenta Arete MR segue uma série de etapas estruturadas para garantir que cada módulo seja corretamente configurado e integrado ao sistema geral. As etapas são organizadas conforme descrito abaixo:

==== 1. Configuração do Ambiente

1. **Configurar o Projeto no Google Cloud:**
    - Criar um novo projeto no Google Cloud Platform.
    - Ativar as APIs necessárias: Google Cloud Storage, Google Cloud Speech-to-Text, Google Cloud Natural Language, Google Cloud Functions, Google Cloud Pub/Sub, Google Cloud Firestore.
2. **Configuração do Armazenamento:**
    - Criar um bucket no Google Cloud Storage para armazenar os arquivos de áudio.
    - Configurar permissões adequadas para leitura e escrita.
3. **Configuração do Google Cloud Speech-to-Text:**
    - Configurar o serviço conforme os parâmetros fornecidos.
    - Implementar a função `transcribe_audio` utilizando o código fornecido.
4. **Configuração do OpenAI GPT-4:**
    - Obter a chave de API do OpenAI.
    - Implementar a função `refine_transcription` utilizando o código fornecido.

==== 2. Desenvolvimento dos Módulos

**Módulo de Upload de Áudio**

1. **Desenvolver Interface de Upload:**
    - Criar a interface de upload de áudio na página Wix em arete.clinic/medical_record.
    - Integrar a interface com o bucket do Google Cloud Storage.
2. **Implementar Conversão de Áudio:**
    - Implementar a lógica de conversão de áudio para o formato WAV, LINEAR16, se necessário.
3. **Implementar Diarização:**
    - Configurar o Google Cloud Speech-to-Text para realizar diarização e identificar diferentes falantes.

**Módulo de Transcrição e Correção**

1. **Transcrição de Áudio:**
    - Integrar o serviço de transcrição utilizando o Google Cloud Speech-to-Text.
    - Configurar a transcrição com correção ortográfica e pontuação.
2. **Verificação e Refinamento de Texto:**
    - Implementar a verificação de qualidade e refinamento do texto utilizando o OpenAI GPT-4.

**Módulo de Processamento do Texto**

1. **Análise Sintática e Semântica:**
    - Implementar a análise sintática e semântica utilizando SpaCy.
2. **Extração e Normalização de Entidades:**
    - Configurar a extração de entidades médicas e não-médicas utilizando SpaCy e MedCAT.
    - Implementar a normalização de entidades com UMLS.
3. **Atribuição de CID10:**
    - Integrar a lógica para atribuir códigos CID10 principais e secundários.

==== 3. Integração e Testes

1. **Integração de Módulos:**
    - Integrar todos os módulos desenvolvidos para garantir a comunicação fluida entre eles.
    - Utilizar Google Cloud Pub/Sub para comunicação assíncrona entre os serviços.
2. **Testes de Unidade e Integração:**
    - Desenvolver testes de unidade para cada módulo.
    - Realizar testes de integração para garantir que todos os módulos funcionem juntos corretamente.
3. **Testes de Desempenho e Segurança:**
    - Realizar testes de desempenho para garantir que o sistema suporte a carga esperada.
    - Implementar medidas de segurança para proteger os dados dos pacientes, conforme as regulamentações da LGPD e legislações canadenses.

==== 4. Implantação e Monitoramento

1. **Implantação no Google Cloud:**
    - Implantar todos os serviços no Google Cloud Platform.
    - Configurar Google Cloud Scheduler para tarefas periódicas.
2. **Monitoramento e Logging:**
    - Configurar Google Cloud Logging e Monitoring para monitoramento contínuo e logging centralizado.
3. **Feedback e Ajustes:**
    - Coletar feedback dos usuários e realizar ajustes conforme necessário.
    - Atualizar e manter a documentação do sistema.

=== Recursos Necessários

- Conta no Google Cloud Platform.
- Chave de API do OpenAI GPT-4.
- Acesso ao ambiente de desenvolvimento para configurar e testar os módulos.

=== Cronograma de Implementação

A implementação do projeto será realizada em várias fases com marcos específicos:

1. **Fase 1: Configuração do Ambiente (1-2 semanas)**
2. **Fase 2: Desenvolvimento dos Módulos (3-4 semanas)**
3. **Fase 3: Integração e Testes (2-3 semanas)**
4. **Fase 4: Implantação e Monitoramento (1-2 semanas)**
5. **Fase 5: Feedback e Ajustes Contínuos (Contínuo)**

== Milestones

1. **Configuração do Projeto e Ambiente**
    - Criação do projeto no Google Cloud Platform.
    - Ativação das APIs necessárias.
    - Configuração inicial do ambiente de desenvolvimento.
2. **Desenvolvimento do Módulo de Upload de Áudio**
    - Desenvolvimento da interface de upload de áudio.
    - Implementação da conversão de áudio e diarização.
    - Integração com o Google Cloud Storage.
3. **Desenvolvimento do Módulo de Transcrição e Correção**
    - Configuração do Google Cloud Speech-to-Text.
    - Implementação da transcrição de áudio com correção ortográfica.
    - Verificação e refinamento de texto com GPT-4.
4. **Desenvolvimento do Módulo de Processamento do Texto**
    - Implementação da análise sintática e semântica com SpaCy.
    - Extração e normalização de entidades com SpaCy e MedCAT.
    - Atribuição de códigos CID10.
5. **Integração de Módulos e Comunicação Assíncrona**
    - Integração dos módulos desenvolvidos.
    - Configuração do Google Cloud Pub/Sub para comunicação entre serviços.
6. **Testes de Unidade e Integração**
    - Desenvolvimento e execução de testes de unidade para cada módulo.
    - Realização de testes de integração para garantir a funcionalidade conjunta dos módulos.
7. **Implantação e Monitoramento**
    - Implantação dos serviços no Google Cloud Platform.
    - Configuração do Google Cloud Scheduler, Logging e Monitoring.
8. **Coleta de Feedback e Ajustes Contínuos**
    - Coleta de feedback dos usuários.
    - Realização de ajustes e melhorias contínuas.
    - Manutenção da documentação do sistema.

== Gathering Results

Para avaliar a eficácia e o desempenho do sistema Arete MR após a implantação, serão utilizadas as seguintes abordagens:

1. **Avaliação de Conformidade:**
    - Verificar a conformidade do sistema com as regulamentações da LGPD no Brasil e legislações canadenses para dados de saúde.
2. **Feedback dos Usuários:**
    - Coletar feedback dos profissionais de saúde que utilizam o sistema.
    - Realizar entrevistas e pesquisas para identificar áreas de melhoria.
3. **Métricas de Desempenho:**
    - Monitorar o desempenho do sistema utilizando Google Cloud Monitoring.
    - Avaliar a latência e a precisão das transcrições e análises.
4. **Análise de Logs e Monitoramento:**
    - Analisar os logs de atividades para identificar possíveis problemas e gargalos.
    - Monitorar o uso de recursos e ajustar a infraestrutura conforme necessário.
5. **Atualizações e Melhorias:**
    - Planejar e implementar atualizações baseadas no feedback e nas métricas de desempenho.
    - Realizar melhorias contínuas para otimizar o sistema e adicionar novas funcionalidades.

Este plano de implementação detalhado garante que a ferramenta Arete MR seja desenvolvida, testada e implantada de forma eficiente, cumprindo todos os requisitos funcionais e regulamentares.