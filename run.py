from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>Upload File</title>
<h1>Upload a File</h1>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit" value="Upload">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(f"./{file.filename}")
            return f"File {file.filename} uploaded successfully!"
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
