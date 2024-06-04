# Arete MR

## Descrição
Arete MR é um sistema avançado de transcrição e análise de consultas médicas, utilizando tecnologias de ponta para garantir precisão, clareza e utilidade nas transcrições.

## Funcionalidades
- **Upload de Áudio:** Usuários fazem o upload de áudios na página `arete.clinic/medical_record`.
- **Transcrição de Áudio:** Converte gravações de consultas médicas em texto utilizando o Google Cloud Speech-To-Text.
- **Correção Ortográfica Automática:** Aplica o LanguageTool para garantir a correção gramatical e ortográfica do texto transcrito.
- **Melhoria de Transcrição:** Utiliza o GPT-4 para refinar e corrigir automaticamente as transcrições.
- **Análise de Texto:** Utiliza Google Cloud Natural Language para análise de sentimentos e emoções, e extração de entidades.
- **Geração de Prontuário:** Estrutura o texto em seções de um prontuário médico com OpenAI GPT-4.

## Estrutura do Projeto
- **/src:** Código fonte dos módulos.
- **/data:** Dados brutos e processados.
- **/configs:** Arquivos de configuração.
- **/logs:** Logs de execução e erros.

## Como Usar
1. Clone o repositório.
2. Configure as credenciais e variáveis de ambiente no arquivo `.env`.
3. Instale as dependências com `pip install -r requirements.txt`.
4. Execute o sistema com `python main.py`.

## Dependências
As dependências do projeto estão listadas no arquivo `requirements.txt`.

## Contribuição
Contribuições são bem-vindas! Siga as diretrizes no arquivo CONTRIBUTING.md para mais informações.

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
