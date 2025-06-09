from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
import json
from datetime import datetime

# Importa o blueprint do dividir_pdf
from dividir_pdf import dividir_pdf_bp  

app = Flask(__name__)
app.secret_key = 'segredo123'

# Registra o blueprint para dividir_pdf
app.register_blueprint(dividir_pdf_bp)

USERS_FILE = 'users.json'

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
        user_data = users.get(username)

        if user_data:
            valid_until_str = user_data.get('valid_until')
            if valid_until_str:
                valid_until = datetime.strptime(valid_until_str, '%Y-%m-%d').date()
                today = datetime.today().date()
                if today > valid_until:
                    return render_template('expirado.html', username=username, validade=valid_until)

            if check_password_hash(user_data['password'], password):
                session['user'] = username
                user_folder = os.path.join('user_data', username)
                os.makedirs(user_folder, exist_ok=True)
                flash('Login realizado com sucesso!', 'sucesso')

                if user_data.get('is_admin'):
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('dashboard'))

        flash('Usuário ou senha incorretos', 'erro')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    flash('O cadastro de novos usuários está desativado. Entre em contato com o administrador.', 'erro')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        username = session['user']
        user_data = users.get(username, {})
        validade = user_data.get('valid_until', 'Indefinido')
        return render_template('dashboard.html', user=username, validade=validade)
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

    resultado = subprocess.run(
        ['python', 'extrair_informacoes.py', user_folder],
        capture_output=True,
        text=True
    )
    print("📤 STDOUT:", resultado.stdout)
    print("⚠️ STDERR:", resultado.stderr)

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

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
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

    if not os.path.exists(caminho_pdf):
        flash('Arquivo de informações extraídas não encontrado. Gere a planilha antes de atualizar.', 'erro')
        return redirect(url_for('dashboard'))

    try:
        subprocess.run(['python', 'atualizar_medicao.py', caminho_pdf, caminho_medicao], check=True)

        if not os.path.exists(caminho_medicao) or os.path.getsize(caminho_medicao) == 0:
            flash('Erro: a planilha de medição não foi gerada corretamente.', 'erro')
            return redirect(url_for('dashboard'))

        flash('Medição atualizada com sucesso!', 'sucesso')
    except subprocess.CalledProcessError:
        flash('Erro ao atualizar a medição.', 'erro')

    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' not in session:
        flash('Faça login para acessar esta área.', 'erro')
        return redirect(url_for('login'))

    current_user = session['user']
    user_data = users.get(current_user)

    if not user_data or not user_data.get('is_admin'):
        flash('Acesso negado.', 'erro')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        acao = request.form.get('acao')
        username = request.form.get('username')

        if acao == 'criar':
            nova_senha = request.form.get('new_password')
            validade = request.form.get('valid_until')
            is_admin = True if request.form.get('is_admin') == 'on' else False

            if username in users:
                flash('Usuário já existe.', 'erro')
            else:
                users[username] = {
                    'password': generate_password_hash(nova_senha),
                    'valid_until': validade,
                    'is_admin': is_admin
                }
                with open(USERS_FILE, 'w') as f:
                    json.dump(users, f, indent=2)
                flash(f'Usuário {username} criado com sucesso.', 'sucesso')

        elif acao == 'editar':
            validade = request.form.get('valid_until')
            nova_senha = request.form.get('new_password')
            is_admin = True if request.form.get('is_admin') == 'on' else False

            if username in users:
                users[username]['valid_until'] = validade
                users[username]['is_admin'] = is_admin
                if nova_senha:
                    users[username]['password'] = generate_password_hash(nova_senha)
                with open(USERS_FILE, 'w') as f:
                    json.dump(users, f, indent=2)
                flash(f'Usuário {username} atualizado.', 'sucesso')
            else:
                flash('Usuário não encontrado.', 'erro')

        elif acao == 'excluir':
            if username in users:
                users.pop(username)
                with open(USERS_FILE, 'w') as f:
                    json.dump(users, f, indent=2)
                flash(f'Usuário {username} excluído.', 'sucesso')
            else:
                flash('Usuário não encontrado.', 'erro')

    return render_template('admin.html', users=users)

# Rota inicial para dividir PDF só para teste rápido, você pode criar link na navbar se quiser
@app.route('/dividir_pdf_link')
def dividir_pdf_link():
    return redirect(url_for('dividir_pdf_bp.dividir_pdf_route'))

if __name__ == '__main__':
    app.run(debug=True)