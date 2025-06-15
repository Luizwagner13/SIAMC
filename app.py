from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
import json
from datetime import datetime

from dividir_pdf import dividir_pdf_bp
from processar_codificacao import processar_codigos
from codificar import get_codigos_disponiveis # <<< Importa a função para obter os códigos disponíveis

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
    if 'username' in session: # Redireciona para a codificação se já estiver logado
        return redirect(url_for('codificar'))
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
                    # Renderiza página de expirado se a conta estiver vencida
                    return render_template('expirado.html', username=username, validade=valid_until_str)
           
            # Autenticação e criação da pasta de usuário
            # NOTA: O campo password no users.json deveria ser 'password_hash' para usar check_password_hash
            # Assumindo que 'password' no users.json é na verdade o hash
            if check_password_hash(user_data['password'], password): 
                session['username'] = username
                session['valid_until'] = user_data.get('valid_until')
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
    # Mantendo o registro desativado conforme seu código
    flash('O cadastro de novos usuários está desativado. Entre em contato com o administrador.', 'erro')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        validade = session.get('valid_until', 'Indefinido')
        return render_template('dashboard.html', user=username, validade=validade)
    flash('Faça login para acessar sua área.', 'erro')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('valid_until', None)
    session.pop('codigos_adicionados', None) # Limpa códigos adicionados na sessão
    flash('Logout realizado com sucesso.', 'sucesso')
    return redirect(url_for('login'))

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
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
    if 'username' not in session:
        flash('Faça login para enviar a medição.', 'erro')
        return redirect(url_for('dashboard'))

    file = request.files.get('medicao')
    if not file or not file.filename.endswith('.xlsx'):
        flash('Envie um arquivo .xlsx válido.', 'erro')
        return redirect(url_for('dashboard'))

    username = session['username']
    user_folder = os.path.join('user_data', username)
    os.makedirs(user_folder, exist_ok=True)

    caminho_medicao = os.path.join(user_folder, 'medicao_atualizada.xlsx')
    file.save(caminho_medicao)

    flash('Planilha de medição enviada e substituída com sucesso!', 'sucesso')
    return redirect(url_for('dashboard'))

@app.route('/criar_planilha', methods=['POST'])
def criar_planilha():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
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

    # Remove PDFs após processamento
    for filename in os.listdir(user_folder):
        if filename.endswith('.pdf'):
            os.remove(os.path.join(user_folder, filename))

    flash('Planilha criada com sucesso!', 'sucesso')
    return redirect(url_for('dashboard'))

@app.route('/baixar_planilha')
def baixar_planilha():
    if 'username' not in session:
        flash('Faça login para baixar a planilha.', 'erro')
        return redirect(url_for('login'))

    username = session['username']
    user_folder = os.path.join('user_data', username)
    filepath = os.path.join(user_folder, 'informacoes_extraidas.xlsx')

    if not os.path.exists(filepath):
        flash('Nenhuma planilha encontrada para download.', 'erro')
        return redirect(url_for('dashboard'))

    return send_file(filepath, as_attachment=True)

@app.route('/baixar_medicao')
def baixar_medicao():
    if 'username' not in session:
        flash('Faça login para baixar a medição.', 'erro')
        return redirect(url_for('login'))

    username = session['username']
    user_folder = os.path.join('user_data', username)
    filepath = os.path.join(user_folder, 'medicao_atualizada.xlsx')

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        flash('Nenhuma planilha de medição encontrada para download.', 'erro')
        return redirect(url_for('dashboard'))

    return send_file(filepath, as_attachment=True)

@app.route('/atualizar_medicao', methods=['POST'])
def atualizar_medicao():
    if 'username' not in session:
        flash('Faça login para atualizar a medição.', 'erro')
        return redirect(url_for('login'))

    username = session['username']
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
    if 'username' not in session:
        flash('Faça login para acessar esta área.', 'erro')
        return redirect(url_for('login'))

    current_user = session['username']
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
                    'password': generate_password_hash(nova_senha), # Assumindo que você quer gerar hash para novas senhas
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
                    users[username]['password'] = generate_password_hash(nova_senha) # Gera hash se a senha for alterada
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
# INÍCIO DA ROTA /CODIFICAR COM AS MELHORIAS E TODA A LÓGICA ATUALIZADA (CORRIGIDA)
# ===================================================================================================================
@app.route('/codificar', methods=['GET', 'POST'])
def codificar():
    if 'username' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'erro')
        return redirect(url_for('login'))

    # Pega a lista de códigos disponíveis do arquivo 'codificar.py'
    codigos_disponiveis = get_codigos_disponiveis()

    # Inicializa a sessão para 'codigos_adicionados' se não existir ou não for uma lista
    codigos_adicionados = session.get('codigos_adicionados', [])
    if not isinstance(codigos_adicionados, list):
        codigos_adicionados = [] # Reseta se estiver corrompido
        session['codigos_adicionados'] = codigos_adicionados
        session.modified = True

    texto_codificado = None # Variável para armazenar o resultado da codificação final

    if request.method == 'POST':
        if 'add_codigo' in request.form: # Botão "Adicionar Código" foi clicado
            codigo_selecionado = request.form.get('codigo') # Campo 'codigo' do select

            # Cria um dicionário base para o novo item
            novo_item = {'codigo': codigo_selecionado}

            # Lógica para preencher campos com base no 'codigo_selecionado'
            # É FUNDAMENTAL que os 'name' dos inputs/selects no HTML correspondam aqui.
            if codigo_selecionado == '319 codigos':
                novo_item['pavimento'] = request.form.get('pavimento') 
                novo_item['troca'] = request.form.get('tipo_troca')   # !!! CORRIGIDO: name="tipo_troca" no HTML
                novo_item['profundidade'] = request.form.get('profundidade')
                novo_item['mts_tubo_batido'] = request.form.get('mts_tubo_batido')
                novo_item['diametro'] = '' # Não se aplica ao 319, mas define para consistência
            elif codigo_selecionado == '321 codigos':
                novo_item['pavimento'] = request.form.get('pavimento_321')
                novo_item['troca'] = request.form.get('tipo_troca_321')
                novo_item['diametro'] = request.form.get('diametro_321')
                novo_item['profundidade'] = ''
                novo_item['mts_tubo_batido'] = ''
            elif codigo_selecionado == '313 codigos':
                novo_item['diametro'] = request.form.get('diametro_313')
                novo_item['pavimento'] = ''
                novo_item['troca'] = ''
                novo_item['profundidade'] = ''
                novo_item['mts_tubo_batido'] = ''
            elif codigo_selecionado == '320 (rec) codigos':
                novo_item['diametro'] = request.form.get('diametro_320_rec')
                novo_item['pavimento'] = request.form.get('pavimento_320_rec')
                novo_item['troca'] = ''
                novo_item['profundidade'] = ''
                novo_item['mts_tubo_batido'] = ''
            elif codigo_selecionado == '300 codigos':
                novo_item['diametro'] = request.form.get('diametro_300')
                novo_item['pavimento'] = request.form.get('pavimento_300')
                novo_item['troca'] = ''
                novo_item['profundidade'] = ''
                novo_item['mts_tubo_batido'] = ''
            elif codigo_selecionado == '343 codigos':
                novo_item['diametro'] = request.form.get('diametro_343')
                novo_item['pavimento'] = request.form.get('pavimento_343')
                novo_item['troca'] = request.form.get('tipo_troca_343')
                novo_item['profundidade'] = ''
                novo_item['mts_tubo_batido'] = ''
            elif codigo_selecionado == '329 codigos':
                novo_item['diametro'] = request.form.get('diametro_329')
                novo_item['pavimento'] = request.form.get('pavimento_329')
                novo_item['troca'] = request.form.get('tipo_troca_329')
                novo_item['profundidade'] = ''
                novo_item['mts_tubo_batido'] = ''
            else: 
                # Para outros códigos que não foram explicitamente mapeados acima,
                # tenta pegar campos genéricos se existirem no formulário.
                novo_item['pavimento'] = request.form.get('pavimento_generico', '')
                novo_item['troca'] = request.form.get('tipo_troca_generico', '')
                novo_item['profundidade'] = request.form.get('profundidade_generico', '')
                novo_item['mts_tubo_batido'] = request.form.get('mts_tubo_batido_generico', '')
                novo_item['diametro'] = request.form.get('diametro_generico', '')

            # Converte valores vazios (strings vazias) para None para o processar_codigos
            for key, value in novo_item.items():
                if value == '':
                    novo_item[key] = None

            # Adiciona o dicionário completo à lista na sessão
            codigos_adicionados.append(novo_item)
            session['codigos_adicionados'] = codigos_adicionados # Garante que a sessão é atualizada
            session.modified = True # Marca a sessão como modificada

            # DEBUG: print após adicionar
            print(f"DEBUG app.py: codigos_adicionados após adicionar: {session['codigos_adicionados']}")

            flash('Código adicionado à lista!', 'sucesso')
            # Redireciona para GET para limpar o formulário e exibir a lista atualizada
            return redirect(url_for('codificar'))

        elif 'finalizar' in request.form: # Botão "Codificar e Gerar Resultado" foi clicado
            itens_para_processar = session.get('codigos_adicionados', [])
            
            # DEBUG: print antes de processar
            print(f"DEBUG app.py: Itens para processar (antes de processar_codigos): {itens_para_processar}")

            if not itens_para_processar:
                flash('Nenhum código para codificar. Adicione itens à lista primeiro.', 'erro')
                return render_template('codificar.html', 
                                       codigos=codigos_disponiveis, 
                                       codigos_adicionados=session.get('codigos_adicionados', []))

            try:
                # Chama a função de processamento (processar_codificacao.py) com a lista de dicionários
                # NOTA: A função processar_codigos deve retornar uma string formatada.
                codigos_finalizados_output = processar_codigos(itens_para_processar)
                
                texto_codificado = codigos_finalizados_output # Assumindo que a função já retorna a string formatada

                flash('Códigos finalizados! Abaixo o texto gerado.', 'sucesso')
                
                # DEBUG: print do resultado do processamento
                print(f"DEBUG app.py: Resultado processar_codigos: '{texto_codificado}'")

            except Exception as e:
                # Em caso de erro, exibe a mensagem de erro e uma flash message
                texto_codificado = f"Erro ao processar códigos: {e}"
                flash(f'Ocorreu um erro ao finalizar a codificação: {e}', 'erro')
                
                # DEBUG: print de erro
                print(f"DEBUG app.py: Erro no processamento: {e}")
            
            # Limpa a lista de códigos na sessão APÓS a finalização
            session.pop('codigos_adicionados', None) 
            
            # Renderiza a página com o resultado (texto_codificado)
            return render_template('codificar.html', 
                                   codigos=codigos_disponiveis, 
                                   texto_codificado=texto_codificado,
                                   codigos_adicionados=[]) # Passa lista vazia para limpar a tabela no frontend
            
    # Para requisições GET (visita inicial ou redirecionamento após 'add_codigo')
    # A lista 'codigos_adicionados' é carregada da sessão
    return render_template('codificar.html', 
                           codigos=codigos_disponiveis, 
                           codigos_adicionados=codigos_adicionados, # Usa a lista carregada/inicializada
                           texto_codificado=None)

# ===================================================================================================================
# FIM DA ROTA /CODIFICAR
# ===================================================================================================================

if __name__ == '__main__':
    app.run(debug=True)