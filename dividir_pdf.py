import os
import zipfile
from PyPDF2 import PdfReader, PdfWriter
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, current_app
from werkzeug.utils import secure_filename
from tempfile import TemporaryDirectory

dividir_pdf_bp = Blueprint('dividir_pdf_bp', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dividir_pdf_bp.route('/dividir_pdf', methods=['GET', 'POST'])
def dividir_pdf_route():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            flash('Nenhum arquivo enviado.', 'erro')
            return redirect(request.url)
        
        file = request.files['pdf']

        if file.filename == '':
            flash('Nenhum arquivo selecionado.', 'erro')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Arquivo inválido. Envie um PDF.', 'erro')
            return redirect(request.url)

        filename = secure_filename(file.filename)

        with TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, filename)
            file.save(pdf_path)

            try:
                reader = PdfReader(pdf_path)
            except Exception as e:
                flash(f'Erro ao ler PDF: {e}', 'erro')
                return redirect(request.url)

            total_pages = len(reader.pages)
            # Define tamanho máximo de páginas por arquivo menor
            max_pages = 10  
            split_files = []

            for i in range(0, total_pages, max_pages):
                writer = PdfWriter()
                for page_num in range(i, min(i + max_pages, total_pages)):
                    writer.add_page(reader.pages[page_num])
                split_filename = f"{filename.rsplit('.',1)[0]}_parte_{i//max_pages + 1}.pdf"
                split_path = os.path.join(tmpdir, split_filename)
                with open(split_path, 'wb') as f_out:
                    writer.write(f_out)
                split_files.append(split_path)

            # Criar zip com os PDFs menores
            zip_path = os.path.join(tmpdir, f"{filename.rsplit('.',1)[0]}_dividido.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in split_files:
                    zipf.write(file_path, os.path.basename(file_path))

            return send_file(zip_path, as_attachment=True)

    # GET: só renderiza o formulário
    return render_template('dividir_pdf.html')
