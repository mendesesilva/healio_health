# setup_env.py

import os
import subprocess

def install_packages():
    # Instalar pacotes usando setup.py
    print("Instalando pacotes usando setup.py...")
    subprocess.check_call([os.sys.executable, 'setup.py', 'install'])

def configure_google_cloud():
    print("Configurando o Google Cloud SDK...")
    # Defina o projeto do Google Cloud
    project_id = "arete-ai"
    bucket_name = "arete-ai"
    subprocess.check_call(['gcloud', 'config', 'set', 'project', project_id])
    print(f"Projeto definido para {project_id}")

    # Verificação e criação do bucket no Google Cloud Storage
    print(f"Verificando se o bucket '{bucket_name}' existe...")
    bucket_check = subprocess.run(['gsutil', 'ls', f'gs://{bucket_name}'], capture_output=True, text=True)
    if bucket_check.returncode != 0:
        print(f"Bucket '{bucket_name}' não encontrado. Criando...")
        subprocess.check_call(['gsutil', 'mb', f'gs://{bucket_name}'])
    else:
        print(f"Bucket '{bucket_name}' já existe.")

    # Configuração do Pub/Sub
    print("Configurando o Pub/Sub...")
    topic_name = "audio-transcription"
    subscription_name = "transcription-sub"
    print(f"Verificando se o tópico '{topic_name}' existe...")
    topic_check = subprocess.run(['gcloud', 'pubsub', 'topics', 'describe', topic_name], capture_output=True, text=True)
    if topic_check.returncode != 0:
        print(f"Tópico '{topic_name}' não encontrado. Criando...")
        subprocess.check_call(['gcloud', 'pubsub', 'topics', 'create', topic_name])
    else:
        print(f"Tópico '{topic_name}' já existe.")

    print(f"Verificando se a inscrição '{subscription_name}' existe...")
    subscription_check = subprocess.run(['gcloud', 'pubsub', 'subscriptions', 'describe', subscription_name], capture_output=True, text=True)
    if subscription_check.returncode != 0:
        print(f"Inscrição '{subscription_name}' não encontrada. Criando...")
        subprocess.check_call(['gcloud', 'pubsub', 'subscriptions', 'create', subscription_name, '--topic', topic_name])
    else:
        print(f"Inscrição '{subscription_name}' já existe.")

if __name__ == "__main__":
    install_packages()
    configure_google_cloud()
