from flask import Flask, render_template, request, Response, make_response, url_for
import re
import csv
from io import StringIO

# Create a Flask app instance
app = Flask(__name__)

# Function to check if the input is a valid Markdown table
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

# Function to convert a valid Markdown table to a CSV table
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

# Route for the main page, handling both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    color = None
    md_table = None
    csv_table = None

    # Handle POST request (form submission)
    if request.method == 'POST':
        
        # Get the submitted Markdown table from the form
        md_table = request.form['md_table']

        # Validate the Markdown table        
        if is_valid_markdown_table(md_table):
            message = 'Valid Markdown'
            color = 'green'

            # Check if the "Convert to CSV" button was clicked
            if 'convert_to_csv' in request.form:
                csv_table = md_table_to_csv(md_table)
        else:
            message = 'Invalid Markdown'
            color = 'red'

    # Render the main page with the appropriate variables
    return render_template('index.html', message=message, color=color, md_table=md_table, csv_table=csv_table)

# Route for downloading the generated CSV file
@app.route('/download_csv', methods=['POST'])
def download_csv():
    # Get the CSV table from the form
    csv_table = request.form['csv_table']

    # Create a response with the CSV table content and set the appropriate headers for the file download
    response = make_response(csv_table)
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='converted_table.csv')

    # Return the response
    return response

# Run in debug mode
if __name__ == '__main__':
    app.run(debug=True)