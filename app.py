import os
import ntpath
import json
import glob
import time
import shutil

from flask import Flask, render_template, request, session, redirect, url_for, g, send_file
from werkzeug.utils import secure_filename
from src.multi.processor import InvoiceMultiProcessor
from src.db.manager import DBManager
from utils.folder_file_manager import save_file
from settings import LOCAL, SERVER_HOST, SERVER_PORT, INVOICE_DIR, OUTPUT_DIR, ARCHIVE_DIR

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_DIR = '/tmp/'

invoice_multi_processor = InvoiceMultiProcessor()
db_manager = DBManager()
total_files = glob.glob(os.path.join(INVOICE_DIR, "*.pdf"))


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    When user signs in, it returns the movie recommended page if user has a rated movie, or rated page so that the user
    can rate even a movie at least.
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password = db_manager.get_user_info(username=username)

        if request.form['password'] == password:
            session['password'] = request.form['password']
            session['user'] = username

            return redirect(url_for('dashboard'))

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if g.user:
        total_files_len = len(total_files)
        processed_files, validated_files = db_manager.get_invoice_status_overview()
        processed_files_len = len(processed_files)
        validated_files_len = len(validated_files)
        not_processed_files_len = total_files_len - processed_files_len
        not_validated_files_len = processed_files_len - validated_files_len
        if total_files_len == 0:
            processed_ratio = 0
            unprocessed_ratio = 0
        else:
            processed_ratio = processed_files_len / total_files_len
            unprocessed_ratio = not_processed_files_len / total_files_len
        if processed_files_len == 0:
            validated_ratio = 0
            invalidated_ratio = 0
        else:
            validated_ratio = validated_files_len / processed_files_len
            invalidated_ratio = not_validated_files_len / processed_files_len

        return render_template("main.html", total_files_len=total_files_len, processed_files_len=processed_files_len,
                               not_processed_files_len=not_processed_files_len, validated_files_len=validated_files_len,
                               not_validated_files_len=not_validated_files_len, processed_ratio=processed_ratio,
                               unprocessed_ratio=unprocessed_ratio, validated_ratio=validated_ratio,
                               invalidated_ratio=invalidated_ratio)

    else:
        return render_template("login.html")


@app.route('/processed', methods=['GET'])
def view_processed_files():
    if g.user:
        processed_files, processed_status = db_manager.get_processed_invoices_name()

        return render_template("processed_file.html", name=session["user"], invalidated=False,
                               response=json.dumps({'file_names': processed_files, 'file_status': processed_status}))
    else:
        return render_template("login.html")


@app.route('/direct_validation', methods=['POST'])
def validate_direct():
    if g.user:
        invoice_name_str = request.form['file_names']
        invoices = invoice_name_str.split(",")[:-1]
        db_manager.update_status_directly(invoice_names=invoices)

        return "Complete"
    else:
        return render_template("login.html")


@app.route('/modification/<init_file_length>')
def modify_invoice_info(init_file_length):
    if g.user:
        invalidated_files = db_manager.get_validated_status_invoices_name(status="0")
        if invalidated_files:
            file_name = invalidated_files[0]
            invoice_info = db_manager.get_invoice_info(file_name=file_name)

            return render_template("invoice_info.html", invoice_info=invoice_info, name=session["user"],
                                   image_info=file_name.replace("pdf", "jpg"), invoice_name=file_name,
                                   init_file_number=init_file_length,
                                   current_file_number=int(init_file_length) - len(invalidated_files) + 1)
        else:
            return redirect(url_for("view_processed_files"))
    else:
        return render_template('login.html')


@app.route('/modify_data', methods=['POST'])
def modify_data():
    if g.user:
        invoice_name = request.form['invoice_name']
        barcode = request.form['barcode']
        lieferschein_nr = request.form['number']
        dts_date = request.form['date']
        dts_time = request.form['time']
        gewicht = request.form['gewicht']
        volume = request.form['volume']
        fuhre = request.form['fuhre']
        db_manager.update_status_with_info(barcode=barcode, lieferschein_nr=lieferschein_nr, dts_date=dts_date,
                                           dts_time=dts_time, gewicht=gewicht, volume=volume, fuhre=fuhre,
                                           invoice_name=invoice_name)
        shutil.move(os.path.join(INVOICE_DIR, invoice_name), os.path.join(ARCHIVE_DIR, invoice_name))

        return "complete"
    else:
        return render_template('login.html')


@app.route('/unprocessed', methods=['GET'])
def view_unprocessed_files():
    if g.user:
        not_processed_files = []
        processed_files, _ = db_manager.get_processed_invoices_name()
        for t_file in total_files:
            t_file_name = ntpath.basename(t_file)
            if t_file_name not in processed_files:
                not_processed_files.append(t_file_name)

        return render_template("unprocessed_file.html", name=session["user"],
                               response=json.dumps({'file_names': not_processed_files}))
    else:
        return render_template("login.html")


@app.route('/unprocessed_files', methods=['POST'])
def process_invoice_files():
    if g.user:
        file_paths = []
        invoice_name_str = request.form['file_names']
        invoices = invoice_name_str.split(",")[:-1]
        for f_invoice in invoices:
            file_path = os.path.join(INVOICE_DIR, f_invoice)
            file_paths.append(file_path)
        invoice_result = invoice_multi_processor.main(pdf_files=file_paths)
        db_manager.insert_unprocessed_invoice_result(invoice_results=invoice_result)
        time.sleep(0.1)

        return "Complete"
    else:
        return render_template("login.html")


@app.route('/validated', methods=['GET'])
def view_validated_files():
    if g.user:
        validated_files = db_manager.get_validated_status_invoices_name(status="1")

        return render_template("validated_file.html", response=json.dumps({'file_names': validated_files}),
                               name=session["user"])
    else:
        return render_template("login.html")


@app.route('/download/<invoice_name_str>', methods=['GET'])
def download_files(invoice_name_str):
    if g.user:
        total_invoice_info = {}
        invoices = invoice_name_str.split(",")[:-1]
        for f_invoice in invoices:
            f_invoice_info = db_manager.get_invoice_info(file_name=f_invoice)
            total_invoice_info[f_invoice] = {"Barcode": f_invoice_info[0], "Lieferschein_Nr": f_invoice_info[1],
                                             "DTS_Date": f_invoice_info[2], "DTS_Time": f_invoice_info[3],
                                             "Gewicht": f_invoice_info[4], "Volume": f_invoice_info[5],
                                             "Fuhre": f_invoice_info[6]}

        output_file_path = os.path.join(OUTPUT_DIR, 'result.json')
        save_file(filename=output_file_path, content=json.dumps(total_invoice_info, indent=4), method="w")

        return send_file(output_file_path, as_attachment=True)
    else:
        return render_template('login.html')


@app.route('/invalidated', methods=['GET'])
def view_invalidated_files():
    if g.user:
        invalidated_files = db_manager.get_validated_status_invoices_name(status="0")
        invalid_status = ["0"] * len(invalidated_files)

        return render_template("processed_file.html", response=json.dumps({'file_names': invalidated_files,
                                                                           'file_status': invalid_status}),
                               name=session["user"], invalidated=True)
    else:
        return render_template("login.html")


@app.route('/file_upload', methods=['GET'])
def file_upload():
    if g.user:
        return render_template("file_upload.html")
    else:
        return render_template("login.html")


@app.route('/upload', methods=['POST'])
def upload():
    if g.user:
        if request.method == 'POST':
            files = request.files.getlist("file")
            for file in files:
                file_name = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_DIR, file_name)
                if ".pdf" in ntpath.basename(file_path):
                    file.save(file_path)

            return render_template("file_upload.html", messages=f"Successfully uploaded {len(files)} invoices!")
    else:
        return render_template("login.html")


@app.route('/logout', methods=['GET'])
def logout():
    drop_session()
    return redirect(url_for('index'))


@app.route('/test', methods=['GET'])
def test_engine():
    return render_template('test_file_upload_form.html', response=json.dumps({"pdf_file_names": []}))


@app.route('/test_extraction', methods=['POST'])
def test_extraction():
    uploaded_files = []
    invoice_multi_processor.multi_pdf_result = {}

    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            file_name = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if ".pdf" in ntpath.basename(file_path):
                file.save(file_path)
                uploaded_files.append(file_path)
        uploaded_invoice_result = invoice_multi_processor.main(pdf_files=uploaded_files)

        uploaded_file_names = list(uploaded_invoice_result.keys())
        response = json.dumps({"pdf_file_names": uploaded_file_names})

        return render_template("test_file_upload_form.html", response=response)


@app.route('/show_result', methods=['POST'])
def show_pdf_result():
    pdf_file_name = request.form['pdf_file']
    response = json.dumps({"invoice_result": invoice_multi_processor.multi_pdf_result[pdf_file_name]})

    return response


@app.route('/update', methods=['POST'])
def update_progress():
    time.sleep(0.1)
    current_processed_files = len(invoice_multi_processor.multi_pdf_result.keys())
    response = json.dumps({"processed_files": current_processed_files})

    return response


@app.route('/dropsession')
def drop_session():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.before_request
def before_request():

    g.user = None
    if 'user' in session:
        g.user = session['user']


if __name__ == '__main__':

    if LOCAL:
        app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
    else:
        app.run(debug=False, host=SERVER_HOST, port=SERVER_PORT)
