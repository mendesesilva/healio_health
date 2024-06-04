import os
from pip install flask import Flask, request, redirect, url_for, render_template, flash
from google.cloud import storage
from werkzeug.utils import secure_filename

# Configurações da aplicação Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'm4a'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16 MB para uploads

# Configuração de uma chave secreta para mensagens flash
app.secret_key = 'supersecretkey'

# Inicializa o cliente do Google Cloud Storage
storage_client = storage.Client()

# Garante que a pasta de upload exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Verifica se o arquivo enviado tem uma extensão permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Renderiza a página de upload."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Manipula o upload de arquivos."""
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Upload para o Google Cloud Storage
        bucket_name = 'your-bucket-name'
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f'audio/{filename}')
        blob.upload_from_filename(file_path)
        
        flash(f'Arquivo {filename} carregado com sucesso')
        return redirect(url_for('index'))
    else:
        flash('Tipo de arquivo não permitido')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
