from flask import Flask, request, make_response
import zipfile
import io
import csv
import time
import os
app=Flask(__name__)

@app.route("/uploadCsv", methods=['GET', 'POST'])
def upload_file():
    f = request.files['file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("utf-8"), newline=None)  
    csv_input = csv.reader(stream, delimiter=';')
    print(csv_input)
    for row in csv_input:
        print(row)

    stream.seek(0)
    result = stream.read()

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response

if __name__ == "__main__":
    app.run()