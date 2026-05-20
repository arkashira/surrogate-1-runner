import tkinter as tk
from tkinter import filedialog, messagebox
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'axentx-surrogate-1-secret-key'
app.config['UPLOAD_FOLDER'] = '/opt/axentx/surrogate-1/design_files'
app.config['ALLOWED_EXTENSIONS'] = {'json', 'csv', 'txt'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class DesignUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Surrogate Tools UI")
        self.create_widgets()

    def create_widgets(self):
        # Create menu bar
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.root.config(menu=menubar)

        # Create main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create left pane for file list
        left_pane = tk.Frame(main_frame, bg="lightgray")
        left_pane.pack(side=tk.LEFT, fill=tk.Y)

        file_list_label = tk.Label(left_pane, text="Design Files")
        file_list_label.pack(pady=5)

        self.file_listbox = tk.Listbox(left_pane)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        # Create right pane for file content
        right_pane = tk.Frame(main_frame, bg="white")
        right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        file_content_label = tk.Label(right_pane, text="File Content")
        file_content_label.pack(pady=5)

        self.file_text = tk.Text(right_pane, wrap=tk.WORD)
        self.file_text.pack(fill=tk.BOTH, expand=True)

        # Create button to upload file
        upload_button = tk.Button(right_pane, text="Upload File", command=self.upload_file)
        upload_button.pack(pady=5)

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'r') as file:
                content = file.read()
                self.file_text.delete(1.0, tk.END)
                self.file_text.insert(tk.END, content)
                self.file_listbox.insert(tk.END, filepath)

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            content = self.file_text.get(1.0, tk.END)
            with open(filepath, 'w') as file:
                file.write(content)
            messagebox.showinfo("Success", "File saved successfully!")

    def upload_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            file = request.files['file']
            if file.filename == '':
                flash('No file selected')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File successfully uploaded')
                return redirect(url_for('index'))
            else:
                flash('Invalid file type')
                return redirect(request.url)

@app.route('/')
def index():
    # List design files
    design_files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        design_files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    # List workflows (mock data for now)
    workflows = [
        {'id': 1, 'name': 'Data Processing', 'status': 'completed', 'progress': 100},
        {'id': 2, 'name': 'Model Training', 'status': 'running', 'progress': 65},
        {'id': 3, 'name': 'Validation', 'status': 'pending', 'progress': 0}
    ]
    
    return render_template('index.html', design_files=design_files, workflows=workflows)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesignUI(root)
    root.mainloop()
    app.run(host='0.0.0.0', port=5000, debug=True)