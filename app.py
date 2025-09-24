from flask import Flask, request, render_template_string, send_file
from stegano import lsb
import os
from flask import url_for


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>LSB-Embedder</title>
  <style>
    body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #fff;
  text-align: center;
  background: 
  url('{{ url_for('static', filename='background.jpg') }}') no-repeat calc(5% - 250px) center,
  url('{{ url_for('static', filename='jian.png') }}') no-repeat calc(95% + 10px) center;
  background-attachment: fixed, fixed;
  background-size: auto, auto; /* adjust each image size individually if needed */
  margin: 0;
  padding: 0;
}
    h1 {
      margin-top: 30px;
      font-size: 2.5rem;
      text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
    }
    form {
      background: rgba(0,0,0,0.6);
      padding: 20px;
      margin: 20px auto;
      border-radius: 15px;
      width: 80%;
      max-width: 500px;
      box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    }
    label {
      display: block;
      margin: 10px 0 5px;
      font-weight: bold;
    }
    input, textarea {
      width: 95%;
      padding: 10px;
      border-radius: 8px;
      border: none;
      margin-bottom: 15px;
      font-size: 1rem;
    }
    button {
      background: linear-gradient(45deg, #00c6ff, #0072ff);
      color: white;
      border: none;
      padding: 12px 25px;
      border-radius: 25px;
      cursor: pointer;
      font-size: 1rem;
      transition: 0.3s ease;
      box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    button:hover {
      background: linear-gradient(45deg, #0072ff, #00c6ff);
      transform: scale(1.05);
    }
    pre {
      background: rgba(0,0,0,0.7);
      padding: 15px;
      border-radius: 10px;
      white-space: pre-wrap;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <h1>🖼️ LSB-Embedder </h1>

  <form action="/embed" method="post" enctype="multipart/form-data">
    <h2>🔒 Embed Secret in Image</h2>
    <label>Upload Image:</label>
    <input type="file" name="image" accept="image/*" required>
    <label>Secret Text:</label>
    <textarea name="secret" rows="4" required></textarea>
    <button type="submit">✨ Embed & Download</button>
  </form>

  <form action="/extract" method="post" enctype="multipart/form-data">
    <h2>🔍 Extract Secret from Image</h2>
    <label>Upload Image:</label>
    <input type="file" name="image" accept="image/*" required>
    <button type="submit">📖 Extract Text</button>
  </form>

  {% if extracted %}
    <h2>📜 Extracted Secret:</h2>
    <pre>{{ extracted }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/embed", methods=["POST"])
def embed():
    image = request.files["image"]
    secret = request.form["secret"]

    in_path = os.path.join(UPLOAD_FOLDER, "input.png")
    out_path = os.path.join(UPLOAD_FOLDER, "output.png")

    image.save(in_path)
    lsb.hide(in_path, secret).save(out_path)

    return send_file(out_path, as_attachment=True, download_name="stego.png")

@app.route("/extract", methods=["POST"])
def extract():
    image = request.files["image"]
    in_path = os.path.join(UPLOAD_FOLDER, "to_extract.png")
    image.save(in_path)

    secret = lsb.reveal(in_path)
    return render_template_string(HTML, extracted=secret)

if __name__ == "__main__":
    app.run(debug=True)
