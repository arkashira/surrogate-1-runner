package utils

import (
	"fmt"
	"io"

	"github.com/skip2/go-qrcode"
)

// GenerateQRCode returns a PNG image as a byte slice that represents a QR
// code for the supplied URL.
//
// The QR code is generated with medium error‑correction and a 256×256 pixel
// image – the default that works well for most web and mobile displays.
// The function validates the input and returns a wrapped error on failure.
//
// Example:
//
//  img, err := GenerateQRCode("https://example.com/approve?token=abc123")
//  if err != nil {
//      // handle error
//  }
//  // write img to response
func GenerateQRCode(url string) ([]byte, error) {
	if url == "" {
		return nil, fmt.Errorf("url cannot be empty")
	}

	png, err := qrcode.Encode(url, qrcode.Medium, 256)
	if err != nil {
		return nil, fmt.Errorf("failed to generate QR code: %w", err)
	}
	return png, nil
}

// GenerateQRCodeToWriter writes the QR code PNG directly to the supplied
// writer.  This helper is useful when you want to stream the image to an
// HTTP response or any other io.Writer without allocating an intermediate
// byte slice.
//
// The function validates its arguments and returns a wrapped error on
// failure.
//
// Example:
//
//  func handler(w http.ResponseWriter, r *http.Request) {
//      url := "https://example.com/approve?token=abc123"
//      w.Header().Set("Content-Type", "image/png")
//      if err := GenerateQRCodeToWriter(url, w); err != nil {
//          http.Error(w, "internal error", http.StatusInternalServerError)
//      }
//  }
func GenerateQRCodeToWriter(url string, w io.Writer) error {
	if w == nil {
		return fmt.Errorf("writer cannot be nil")
	}
	png, err := GenerateQRCode(url)
	if err != nil {
		return err
	}
	_, err = w.Write(png)
	return err
}