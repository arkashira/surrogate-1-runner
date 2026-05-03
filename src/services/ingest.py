--- /opt/axentx/surrogate-1/src/services/ingest.py
+++ /opt/axentx/surrogate-1/src/services/ingest.py
@@ -0,0 +1,40 @@
+import os
+import uuid
+from flask import Flask, request, jsonify
+
+app = Flask(__name__)
+
+UPLOAD_FOLDER = '/data/pending'
+MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
+app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
+app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
+
+class ProcessingStatus:
+    PENDING = 'pending'
+
+def save_pdf(file, ingestion_id):
+    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{ingestion_id}.pdf")
+    file.save(file_path)
+    return file_path
+
+@app.route('/upload', methods=['POST'])
+def upload_pdf():
+    if 'file' not in request.files:
+        return jsonify({"error": "No file part"}), 400
+
+    file = request.files['file']
+    
+    if file.filename == '':
+        return jsonify({"error": "No selected file"}), 400
+
+    ingestion_id = str(uuid.uuid4())
+    save_pdf(file, ingestion_id)
+
+    metadata = {
+        "title": file.filename,
+        "source": "upload",
+        "created_at": request.date,
+        "processing_status": ProcessingStatus.PENDING
+    }
+
+    return jsonify({"ingestion_id": ingestion_id}), 202
+
+if __name__ == '__main__':
+    app.run(debug=True)