from flask import Flask, render_template, request, Response, make_response, url_for
import re
import csv
from io import StringIO

app = Flask(__name__)

def is_valid_markdown_table(md_table):
    lines = md_table.split('\n')
    if len(lines) < 2:
        return False

    header_separator = lines[1]
    if not re.fullmatch(r'\|((:?-+:?|\s)+\|)+', header_separator.strip()):
        return False

    for line in lines[2:]:
        if line.strip() and not re.fullmatch(r'\|((.|\s)+\|)+', line.strip()):
            return False

    return True

def md_table_to_csv(md_table):
    lines = [line.strip() for line in md_table.strip().split('\n') if line.strip()]
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)

    for line in lines:
        if not line.startswith('|'):
            continue
        row = [cell.strip() for cell in line.split('|')[1:-1]]
        csv_writer.writerow(row)

    return csv_output.getvalue()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    color = None
    md_table = None
    csv_table = None

    if request.method == 'POST':
        md_table = request.form['md_table']
        if is_valid_markdown_table(md_table):
            message = 'Valid Markdown'
            color = 'green'

            if 'convert_to_csv' in request.form:
                csv_table = md_table_to_csv(md_table)
        else:
            message = 'Invalid Markdown'
            color = 'red'

    return render_template('index.html', message=message, color=color, md_table=md_table, csv_table=csv_table)

@app.route('/download_csv', methods=['POST'])
def download_csv():
    csv_table = request.form['csv_table']
    response = make_response(csv_table)
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='converted_table.csv')

    return response

if __name__ == '__main__':
    app.run(debug=True)