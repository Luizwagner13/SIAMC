from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
import json

app = Flask(__name__)
app.secret_key = 'segredo123'

USERS_FILE = 'users.json'

# Carrega os usuários do arquivo (ou cria um novo)
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            user_folder = os.path.join('user_data', username)
            os.makedirs(user_folder, exist_ok=True)
            flash('Login realizado com sucesso!', 'sucesso')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos', 'erro')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            hashed_password = generate_password_hash(password)
            users[username] = hashed_password
            with open(USERS_FILE, 'w') as f:
                json.dump(users, f)
            flash('Cadastro realizado com sucesso! Faça login.', 'sucesso')
            return redirect(url_for('login'))
        else:
            flash('Usuário já existe', 'erro')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    flash('Faça login para acessar sua área.', 'erro')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout realizado com sucesso.', 'sucesso')
    return redirect(url_for('login'))

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    user_folder = os.path.join('user_data', username)
    os.makedirs(user_folder, exist_ok=True)

    files = request.files.getlist('pdfs')
    for file in files:
        if file and file.filename.endswith('.pdf'):
            filename = os.path.basename(file.filename)
            filepath = os.path.join(user_folder, filename)
            file.save(filepath)

    flash('PDF(s) enviados com sucesso.', 'sucesso')
    return redirect(url_for('dashboard'))

@app.route('/upload_medicao', methods=['POST'])
def upload_medicao():
    if 'user' not in session:
        flash('Faça login para enviar a medição.', 'erro')
        return redirect(url_for('login'))

    file = request.files.get('medicao')
    if not file or not file.filename.endswith('.xlsx'):
        flash('Envie um arquivo .xlsx válido.', 'erro')
        return redirect(url_for('dashboard'))

    username = session['user']
    user_folder = os.path.join('user_data', username)
    os.makedirs(user_folder, exist_ok=True)

    caminho_medicao = os.path.join(user_folder, 'medicao_atualizada.xlsx')
    file.save(caminho_medicao)

    flash('Planilha de medição enviada e substituída com sucesso!', 'sucesso')
    return redirect(url_for('dashboard'))

@app.route('/criar_planilha', methods=['POST'])
def criar_planilha():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    user_folder = os.path.join('user_data', username)

    subprocess.run(['python', 'extrair_informacoes.py', user_folder])

    for filename in os.listdir(user_folder):
        if filename.endswith('.pdf'):
            os.remove(os.path.join(user_folder, filename))

    flash('Planilha criada com sucesso!', 'sucesso')
    return redirect(url_for('dashboard'))

@app.route('/baixar_planilha')
def baixar_planilha():
    if 'user' not in session:
        flash('Faça login para baixar a planilha.', 'erro')
        return redirect(url_for('login'))

    username = session['user']
    user_folder = os.path.join('user_data', username)
    filepath = os.path.join(user_folder, 'informacoes_extraidas.xlsx')

    if not os.path.exists(filepath):
        flash('Nenhuma planilha encontrada para download.', 'erro')
        return redirect(url_for('dashboard'))

    return send_file(filepath, as_attachment=True)

@app.route('/baixar_medicao')
def baixar_medicao():
    if 'user' not in session:
        flash('Faça login para baixar a medição.', 'erro')
        return redirect(url_for('login'))

    username = session['user']
    user_folder = os.path.join('user_data', username)
    filepath = os.path.join(user_folder, 'medicao_atualizada.xlsx')

    if not os.path.exists(filepath):
        flash('Nenhuma planilha de medição encontrada para download.', 'erro')
        return redirect(url_for('dashboard'))

    return send_file(filepath, as_attachment=True)

@app.route('/atualizar_medicao', methods=['POST'])
def atualizar_medicao():
    if 'user' not in session:
        flash('Faça login para atualizar a medição.', 'erro')
        return redirect(url_for('login'))

    username = session['user']
    user_folder = os.path.join('user_data', username)

    caminho_pdf = os.path.join(user_folder, 'informacoes_extraidas.xlsx')
    caminho_medicao = os.path.join(user_folder, 'medicao_atualizada.xlsx')

    try:
        subprocess.run(['python', 'atualizar_medicao.py', caminho_pdf, caminho_medicao], check=True)
        flash('Medição atualizada com sucesso!', 'sucesso')
    except subprocess.CalledProcessError:
        flash('Erro ao atualizar a medição.', 'erro')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)