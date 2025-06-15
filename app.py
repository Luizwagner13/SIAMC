from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
import json
from datetime import datetime

from dividir_pdf import dividir_pdf_bp
from processar_codificacao import processar_codigos
from codificar import get_codigos_disponiveis # <<< NOVA LINHA: Importa a função para obter os códigos disponíveis

app = Flask(__name__)
app.secret_key = 'segredo123'
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
                    return render_template('expirado.html', username=username, validade=valid_until_str) # Corrigido para valid_until_str
            
            # Autenticação e criação da pasta de usuário
            if check_password_hash(user_data['password'], password):
                session['username'] = username # Corrigido para 'username' em vez de 'user' para consistência
                session['valid_until'] = user_data.get('valid_until') # Armazena valid_until na sessão
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
    if 'username' in session: # Corrigido para 'username'
        username = session['username'] # Corrigido para 'username'
        validade = session.get('valid_until', 'Indefinido') # Pega da sessão para consistência
        return render_template('dashboard.html', user=username, validade=validade)
    flash('Faça login para acessar sua área.', 'erro')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None) # Corrigido para 'username'
    session.pop('valid_until', None) # Limpa valid_until
    session.pop('codigos_adicionados', None) # Limpa códigos adicionados
    flash('Logout realizado com sucesso.', 'sucesso')
    return redirect(url_for('login'))

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'username' not in session: # Corrigido para 'username'
        return redirect(url_for('login'))

    username = session['username'] # Corrigido para 'username'
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
    if 'username' not in session: # Corrigido para 'username'
        flash('Faça login para enviar a medição.', 'erro')
        return redirect(url_for('dashboard'))

    file = request.files.get('medicao')
    if not file or not file.filename.endswith('.xlsx'):
        flash('Envie um arquivo .xlsx válido.', 'erro')
        return redirect(url_for('dashboard'))

    username = session['username'] # Corrigido para 'username'
    user_folder = os.path.join('user_data', username)
    os.makedirs(user_folder, exist_ok=True)

    caminho_medicao = os.path.join(user_folder, 'medicao_atualizada.xlsx')
    file.save(caminho_medicao)

    flash('Planilha de medição enviada e substituída com sucesso!', 'sucesso')
    return redirect(url_for('dashboard'))

@app.route('/criar_planilha', methods=['POST'])
def criar_planilha():
    if 'username' not in session: # Corrigido para 'username'
        return redirect(url_for('login'))

    username = session['username'] # Corrigido para 'username'
    user_folder = os.path.join('user_data', username)

    try:
        resultado = subprocess.run(
            ['python', 'extrair_informacoes.py', user_folder],
            capture_output=True,
            text=True,
            timeout=300
        )
        print("📤 STDOUT:", resultado.stdout)
        print("⚠️ STDERR:", resultado.stderr)

        if resultado.returncode != 0:
            flash('Erro ao gerar a planilha. Verifique os dados enviados.', 'erro')
            return redirect(url_for('dashboard'))

    except subprocess.TimeoutExpired:
        flash('A criação da planilha excedeu o tempo limite (5 minutos).', 'erro')
        return redirect(url_for('dashboard'))
    except subprocess.CalledProcessError:
        flash('Erro ao executar o script de criação da planilha.', 'erro')
        return redirect(url_for('dashboard'))

    for filename in os.listdir(user_folder):
        if filename.endswith('.pdf'):
            os.remove(os.path.join(user_folder, filename))

    flash('Planilha criada com sucesso!', 'sucesso')
    return redirect(url_for('dashboard'))

@app.route('/baixar_planilha')
def baixar_planilha():
    if 'username' not in session: # Corrigido para 'username'
        flash('Faça login para baixar a planilha.', 'erro')
        return redirect(url_for('login'))

    username = session['username'] # Corrigido para 'username'
    user_folder = os.path.join('user_data', username)
    filepath = os.path.join(user_folder, 'informacoes_extraidas.xlsx')

    if not os.path.exists(filepath):
        flash('Nenhuma planilha encontrada para download.', 'erro')
        return redirect(url_for('dashboard'))

    return send_file(filepath, as_attachment=True)

@app.route('/baixar_medicao')
def baixar_medicao():
    if 'username' not in session: # Corrigido para 'username'
        flash('Faça login para baixar a medição.', 'erro')
        return redirect(url_for('login'))

    username = session['username'] # Corrigido para 'username'
    user_folder = os.path.join('user_data', username)
    filepath = os.path.join(user_folder, 'medicao_atualizada.xlsx')

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        flash('Nenhuma planilha de medição encontrada para download.', 'erro')
        return redirect(url_for('dashboard'))

    return send_file(filepath, as_attachment=True)

@app.route('/atualizar_medicao', methods=['POST'])
def atualizar_medicao():
    if 'username' not in session: # Corrigido para 'username'
        flash('Faça login para atualizar a medição.', 'erro')
        return redirect(url_for('login'))

    username = session['username'] # Corrigido para 'username'
    user_folder = os.path.join('user_data', username)

    caminho_pdf = os.path.join(user_folder, 'informacoes_extraidas.xlsx')
    caminho_medicao = os.path.join(user_folder, 'medicao_atualizada.xlsx')

    if not os.path.exists(caminho_pdf):
        flash('Arquivo de informações extraídas não encontrado. Gere a planilha antes de atualizar.', 'erro')
        return redirect(url_for('dashboard'))

    try:
        subprocess.run(
            ['python', 'atualizar_medicao.py', caminho_pdf, caminho_medicao],
            check=True,
            timeout=300
        )

        if not os.path.exists(caminho_medicao) or os.path.getsize(caminho_medicao) == 0:
            flash('Erro: a planilha de medição não foi gerada corretamente.', 'erro')
            return redirect(url_for('dashboard'))

        flash('Medição atualizada com sucesso!', 'sucesso')

    except subprocess.TimeoutExpired:
        flash('A atualização da medição excedeu o tempo limite (5 minutos).', 'erro')
    except subprocess.CalledProcessError:
        flash('Erro ao atualizar a medição.', 'erro')

    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session: # Corrigido para 'username'
        flash('Faça login para acessar esta área.', 'erro')
        return redirect(url_for('login'))

    current_user = session['username'] # Corrigido para 'username'
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

@app.route('/dividir_pdf_link')
def dividir_pdf_link():
    return redirect(url_for('dividir_pdf_bp.dividir_pdf_route'))

# ===================================================================================================================
# INÍCIO DA ROTA /CODIFICAR COM AS MELHORIAS E TODA A LÓGICA ATUALIZADA
# ===================================================================================================================
@app.route('/codificar', methods=['GET', 'POST'])
def codificar():
    if 'username' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'erro')
        return redirect(url_for('login'))

    # Pega a lista de códigos disponíveis do arquivo 'codificar.py'
    codigos_disponiveis = get_codigos_disponiveis() # <<< ALTERAÇÃO: Usa a função importada

    # Inicializa a sessão para 'codigos_adicionados' se não existir
    if 'codigos_adicionados' not in session:
        session['codigos_adicionados'] = []

    texto_codificado = None # Variável para armazenar o resultado da codificação final

    if request.method == 'POST':
        if 'add_codigo' in request.form: # Botão "Adicionar Código" foi clicado
            codigo = request.form.get('codigo')
            
            # Captura TODOS os campos que podem vir do formulário.
            # Usamos .get() para evitar KeyError e atribuímos None se o campo não estiver presente ou vazio.
            pavimento = request.form.get('pavimento')
            troca = request.form.get('troca')
            profundidade = request.form.get('profundidade')
            mts_tubo_batido = request.form.get('mts_tubo_batido') # NOVO CAMPO
            diametro = request.form.get('diametro')             # NOVO CAMPO

            # Cria um dicionário para o item com todos os campos possíveis.
            # Se um campo não foi preenchido/selecionado para um código específico, ele será None.
            item_codificado = {
                'codigo': codigo,
                'pavimento': pavimento if pavimento else None, # <<< ALTERAÇÃO: Garante None se a string for vazia
                'troca': troca if troca else None,             # <<< ALTERAÇÃO: Garante None se a string for vazia
                'profundidade': profundidade if profundidade else None, # <<< ALTERAÇÃO: Garante None se a string for vazia
                'mts_tubo_batido': mts_tubo_batido if mts_tubo_batido else None,
                'diametro': diametro if diametro else None
            }
            
            # Adiciona o dicionário à lista na sessão
            codigos_atualizados = session.get('codigos_adicionados', [])
            codigos_atualizados.append(item_codificado)
            session['codigos_adicionados'] = codigos_atualizados
            
            flash('Código adicionado à lista!', 'sucesso')
            # Redireciona para GET para limpar o formulário e exibir a lista atualizada
            return redirect(url_for('codificar'))

        elif 'finalizar' in request.form: # Botão "Codificar e Gerar Resultado" foi clicado (do novo formulário)
            itens_para_processar = session.get('codigos_adicionados', [])
            
            if not itens_para_processar: # <<< NOVA LINHA: Verifica se há itens para processar
                flash('Nenhum código para codificar. Adicione itens à lista primeiro.', 'erro')
                return render_template('codificar.html', 
                                       codigos=codigos_disponiveis, 
                                       codigos_adicionados=session.get('codigos_adicionados', []))

            try:
                # Chama a função de processamento (processar_codificacao.py) com a lista de dicionários
                codigos_finalizados_output = processar_codigos(itens_para_processar)
                texto_codificado = '\n'.join(codigos_finalizados_output)
                flash('Códigos finalizados! Abaixo o texto gerado.', 'sucesso')
            except Exception as e:
                # Em caso de erro, exibe a mensagem de erro e uma flash message
                texto_codificado = f"Erro ao processar códigos: {e}"
                flash(f'Ocorreu um erro ao finalizar a codificação: {e}', 'erro')
            
            # Limpa a lista de códigos na sessão APÓS a finalização
            session.pop('codigos_adicionados', None) 
            
            # Renderiza a página com o resultado (texto_codificado)
            # A lista de códigos adicionados será vazia no template após o pop da sessão
            return render_template('codificar.html', 
                                   codigos=codigos_disponiveis, 
                                   texto_codificado=texto_codificado,
                                   codigos_adicionados=[]) # <<< ALTERAÇÃO: Passa lista vazia para limpar a tabela no frontend
    
    # Para requisições GET (visita inicial ou redirecionamento após 'add_codigo')
    # A lista 'codigos_adicionados' é carregada da sessão
    return render_template('codificar.html', 
                           codigos=codigos_disponiveis, 
                           codigos_adicionados=session.get('codigos_adicionados', []), 
                           texto_codificado=None) # <<< ALTERAÇÃO: Garante que texto_codificado seja None em GET

# ===================================================================================================================
# FIM DA ROTA /CODIFICAR
# ===================================================================================================================

if __name__ == '__main__':
    app.run(debug=True)