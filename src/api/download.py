"""
Download API endpoint for serving compliance PDFs.

This module exposes a Flask Blueprint `/download/<doc_id>` that streams a
signed PDF file to the client. The PDF is expected to reside in the
`/var/axentx/compliance_docs` directory, named as `<doc_id>.pdf`.

The route validates the existence of the file, sets appropriate
Content-Type headers, and streams the file in chunks to avoid loading the
entire document into memory. If the file does not exist, a 404 response
is returned.
"""

import os
from flask import Blueprint, send_file, abort, current_app

# Use Blueprint for better application structure (from Candidate 2)
download_bp = Blueprint('download', __name__)

# Directory where signed PDFs are stored
PDF_STORAGE_DIR = "/var/axentx/compliance_docs"

@download_bp.route("/download/<doc_id>", methods=["GET"])
def download_pdf(doc_id: str):
    """
    Stream a signed PDF document to the client.

    Parameters
    ----------
    doc_id : str
        Identifier of the document to download. The file is expected to be
        named `<doc_id>.pdf` in the storage directory.

    Returns
    -------
    Response
        Flask response streaming the PDF file or a 404 error if not found.
    """
    # Sanitize doc_id to prevent directory traversal (from Candidate 1)
    safe_doc_id = os.path.basename(doc_id)
    
    # Validate the sanitized ID matches the original (prevent bypass attempts)
    if safe_doc_id != doc_id:
        abort(400, description="Invalid document ID format")
    
    file_path = os.path.join(PDF_STORAGE_DIR, f"{safe_doc_id}.pdf")

    if not os.path.isfile(file_path):
        abort(404, description="Document not found")

    # Use Flask's send_file with as_attachment to prompt download (from Candidate 1)
    # Added conditional for large files to stream instead of loading into memory
    file_size = os.path.getsize(file_path)
    if file_size > 10 * 1024 * 1024:  # >10MB
        # Stream large files to avoid memory issues
        return send_file(
            file_path,
            mimetype="application/pdf",
            as_attachment=True,
            attachment_filename=f"{safe_doc_id}.pdf",
            as_attachment=True,
            download_name=f"{safe_doc_id}.pdf"  # Flask 2.2+ parameter
        )
    
    return send_file(
        file_path,
        mimetype="application/pdf",
        as_attachment=True,
        attachment_filename=f"{safe_doc_id}.pdf",
    )