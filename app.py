from flask import Flask, render_template, request, redirect, url_for, send_file
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
from PIL import Image
from docx2pdf import convert as convert_docx_to_pdf
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cria a pasta de uploads, se ainda não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-password', methods=['POST'])
def add_password():
    pdf = request.files['pdf_file']
    password = request.form['password']
    filename = secure_filename(pdf.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf.save(filepath)

    reader = PdfReader(filepath)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"protected_{filename}")
    with open(output_path, 'wb') as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)

@app.route('/remove-password', methods=['POST'])
def remove_password():
    pdf = request.files['pdf_file']
    password = request.form['password']
    filename = secure_filename(pdf.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf.save(filepath)

    reader = PdfReader(filepath)

    if reader.is_encrypted:
        try:
            reader.decrypt(password)
        except:
            return "Erro ao remover senha. Verifique a senha e tente novamente.", 400

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"unlocked_{filename}")
    with open(output_path, 'wb') as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    output_filename = f"{base}.pdf"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    if ext == '.txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in content.splitlines():
            pdf.multi_cell(0, 10, txt=line)
        pdf.output(output_path)

    elif ext in ['.jpg', '.jpeg', '.png']:
        image = Image.open(filepath)
        rgb_image = image.convert('RGB')
        rgb_image.save(output_path)

    elif ext == '.docx':
        try:
            convert_docx_to_pdf(filepath, output_path)
        except Exception as e:
            return f"Erro ao converter DOCX: {str(e)}", 500
    else:
        return "Tipo de arquivo não suportado para conversão.", 400

    # Redireciona para página de download
    return redirect(url_for('download_page', filename=output_filename))

@app.route('/download/<filename>')
def download_page(filename):
    return render_template('download.html', filename=filename)

@app.route('/download-file/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
