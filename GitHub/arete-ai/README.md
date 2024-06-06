# Arete-IA

## Descrição

O projeto **Arete-IA** é uma ferramenta avançada desenvolvida para automatizar a captura e transcrição de consultas médicas, além de realizar análises detalhadas dos dados do paciente. Utilizando tecnologias de ponta como Google Cloud e GPT-4, o sistema busca melhorar a qualidade dos registros clínicos e a eficiência no atendimento ao paciente.

## Estrutura do Projeto

- `documentos/`: Contém documentos relacionados ao projeto.
  - `arquitetura/`: Documentação e diagramas da arquitetura do sistema.
    - `Arete MR Arquitetura MV.md`: Documento detalhando a arquitetura do sistema.
    - `Arete MR IDEF0.md`: Modelo IDEF0 do sistema.
    - `Arete MR TOGAF.md`: Arquitetura baseada no framework TOGAF.
  
- `imagens/`: Armazena imagens utilizadas no projeto.
  - `arquitetura/`: Imagens relacionadas à arquitetura do sistema.
    - `IMG_2624.png`: Diagrama da arquitetura do sistema.

- `src/`: Código fonte do projeto.
  - `transcricao/`: Código relacionado à transcrição de áudio.
    - `transcricao.py`: Código para transcrição de áudio de consultas médicas.
  - `analise/`: Código para análise dos dados transcritos.
    - `analise.py`: Código para análise de dados clínicos.
  - `utils/`: Funções utilitárias.
    - `utils.py`: Funções gerais e utilitárias.
  - `main.py`: Arquivo principal que orquestra a execução do sistema.
  - `requirements.txt`: Lista de dependências do projeto.

- `tests/`: Testes unitários e de integração.
  - `unit/`: Testes unitários.
    - `test_transcricao.py`: Testes para o módulo de transcrição.
    - `test_analise.py`: Testes para o módulo de análise.
  - `integration/`: Testes de integração.
    - `test_full_flow.py`: Testes do fluxo completo do sistema.

- `logs/`: Arquivos de log.
  - `app/`: Logs da aplicação.
  - `errors/`: Logs de erros.

- `data/`: Dados de entrada e saída do projeto.
  - `input/`: Dados de entrada.
  - `output/`: Dados de saída.

- `configs/`: Arquivos de configuração.
  - `config.yaml`: Configurações gerais do sistema.
  - `secrets.ini`: Variáveis sensíveis e segredos.

- `scripts/`: Scripts auxiliares.
  - `setup_db.py`: Script para configuração de banco de dados.
  - `deploy.sh`: Script para deploy do sistema.

## Requisitos

- **Python 3.8+**: Certifique-se de que você tenha Python instalado.
- **Google Cloud SDK**: Instale e configure o Google Cloud SDK.
- **Dependências**: Listadas no arquivo `requirements.txt`.

## Instalação

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/seu-usuario/arete-ia.git
    cd arete-ia
    ```

2. **Crie um ambiente virtual** (opcional, mas recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. **Instale as dependências**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o ambiente no Google Cloud**:

    Execute o script `setup_env.py` para configurar o ambiente no Google Cloud e instalar as dependências necessárias:

    ```bash
    python setup_env.py
    ```

## Uso

1. **Inicialize o sistema**:

    ```bash
    python src/main.py
    ```

    Isso irá iniciar o sistema Arete-IA e executar a transcrição e análise dos dados.

2. **Transcreva um áudio**:

    Para transcrever um áudio específico, use a função `transcrever_audio` no módulo `transcricao.py`:

    ```python
    from src.transcricao import transcrever_audio

    resultado = transcrever_audio("path/to/audio_file")
    print(resultado)
    ```

3. **Analise os dados transcritos**:

    Para analisar os dados transcritos, utilize a função `analisar_dados` no módulo `analise.py`:

    ```python
    from src.analise import analisar_dados

    dados_analise = analisar_dados("Texto transcrito da consulta")
    print(dados_analise)
    ```

## Testes

1. **Execute os testes**:

    ```bash
    pytest tests/
    ```

    Isso irá executar todos os testes unitários e de integração para garantir que as funções estão funcionando corretamente.

## Contribuição

1. **Faça um fork do projeto**.
2. **Crie uma nova branch**:

    ```bash
    git checkout -b minha-nova-funcionalidade
    ```

3. **Faça suas modificações e commit**:

    ```bash
    git commit -am "Adiciona nova funcionalidade"
    ```

4. **Envie para a branch original**:

    ```bash
    git push origin minha-nova-funcionalidade
    ```

5. **Crie um Pull Request**.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

Este README fornece uma visão abrangente do projeto Arete-IA e instruções claras sobre como começar, usar e contribuir para o desenvolvimento do projeto.
