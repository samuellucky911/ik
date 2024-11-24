from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)

# Specify the folder where the files will be saved
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allow only certain file extensions for upload (optional)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# HTML template for uploading and listing files
HTML = '''
<!doctype html>
<title>Upload and Download Files</title>
<h1>Upload a File</h1>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file" accept="image/*, .pdf, .txt">
    <input type="submit" value="Upload">
</form>
<h2>Uploaded Files</h2>
<ul>
    {% for filename in files %}
    <li><a href="/download/{{ filename }}">{{ filename }}</a></li>
    {% endfor %}
</ul>
'''

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Upload a file and display uploaded files."""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the file to the UPLOAD_FOLDER
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return f"File {filename} uploaded successfully!"
    
    # List all files in the upload folder
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, files=files)

@app.route('/download/<filename>')
def download_file(filename):
    """Download a specific file."""
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
