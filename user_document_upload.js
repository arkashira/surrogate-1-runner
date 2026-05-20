/**
 * User Document Upload Service
 *
 * • Accepts a single file (PDF, DOCX, PNG, JPG) up to 10 MB.
 * • Stores files in a dedicated `uploads/` directory.
 * • Sends a confirmation e‑mail via Nodemailer.
 * • Falls back to a console‑stub if SMTP credentials are missing.
 * • Exposes a clean Express app that can be started with `app.listen()`.
 *
 * Usage:
 *   const app = require('./user_document_upload');
 *   app.listen(3000, () => console.log('Server running on port 3000'));
 *
 * Environment variables (optional):
 *   SMTP_HOST, SMTP_PORT, SMTP_SECURE, SMTP_USER, SMTP_PASS
 *   EMAIL_FROM
 */

const express = require('express');
const multer  = require('multer');
const nodemailer = require('nodemailer');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();

/* -------------------------------------------------------------------------- */
/* 1️⃣  Upload directory – created if missing                                 */
/* -------------------------------------------------------------------------- */
const UPLOAD_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

/* -------------------------------------------------------------------------- */
/* 2️⃣  Multer configuration – storage, size limit, MIME filtering           */
/* -------------------------------------------------------------------------- */
const storage = multer.diskStorage({
  destination: (_, __, cb) => cb(null, UPLOAD_DIR),
  filename: (_, file, cb) => {
    const ts = Date.now();
    const safe = file.originalname.replace(/[^a-zA-Z0-9.\-_]/g, '_');
    cb(null, `${ts}-${safe}`);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 10 * 1024 * 1024 }, // 10 MB
  fileFilter: (_, file, cb) => {
    const allowed = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'image/png',
      'image/jpeg',
    ];
    cb(null, allowed.includes(file.mimetype) ? null : new Error('Unsupported file type'));
  },
});

/* -------------------------------------------------------------------------- */
/* 3️⃣  Email transporter – real SMTP or console stub                        */
/* -------------------------------------------------------------------------- */
let transporter;
if (process.env.SMTP_HOST && process.env.SMTP_PORT) {
  transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT),
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });
} else {
  // Stub – logs to console, useful for dev & tests
  transporter = {
    sendMail: async (opts) => {
      console.log('--- Email Stub ---');
      console.log('To:', opts.to);
      console.log('Subject:', opts.subject);
      console.log('Text:', opts.text);
      console.log('--- End Email Stub ---');
      return Promise.resolve();
    },
  };
}

/* -------------------------------------------------------------------------- */
/* 4️⃣  Route – POST /upload                                                 */
/* -------------------------------------------------------------------------- */
app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    const { file } = req;
    const { email } = req.body;

    if (!file) return res.status(400).json({ success: false, error: 'No file uploaded' });
    if (!email) {
      fs.unlinkSync(file.path); // clean up
      return res.status(400).json({ success: false, error: 'Email is required' });
    }

    const mailOptions = {
      from: process.env.EMAIL_FROM || 'no-reply@axentx.com',
      to: email,
      subject: 'Document Upload Confirmation',
      text: `Hello,

Your document "${file.originalname}" has been successfully uploaded and is pending verification.

Thank you,
Axentx Team`,
    };

    await transporter.sendMail(mailOptions);

    res.json({
      success: true,
      filePath: path.relative(__dirname, file.path),
      message: 'File uploaded and confirmation email sent',
    });
  } catch (err) {
    console.error('Upload error:', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

/* -------------------------------------------------------------------------- */
/* 5️⃣  Global error handler – Multer errors & generic errors                */
/* -------------------------------------------------------------------------- */
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    return res.status(400).json({ success: false, error: err.message });
  }
  if (err) {
    return res.status(400).json({ success: false, error: err.message });
  }
  next();
});

module.exports = app;