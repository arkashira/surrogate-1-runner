module.exports = {
  key: fs.readFileSync('/opt/axentx/surrogate-1/config/tls/key.pem'),
  cert: fs.readFileSync('/opt/axentx/surrogate-1/config/tls/cert.pem'),
  ca: fs.readFileSync('/opt/axentx/surrogate-1/config/tls/ca.pem'),
  ciphers: 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:TLS_AES_256_CBC_SHA256:TLS_AES_128_CBC_SHA256',
  honorCipherOrder: true
};