package utils

import (
	"image"
	"image/color"
	"image/draw"
	"math/rand"
	"os"
	"fmt"
	"image/png"
	"golang.org/x/image/font/basicfont"
	"golang.org/x/image/math/fixed"
)

type ChartData struct {
	Title string
	Data []float64
}

func ExportChart(data string, format string) (string, error) {
	// Parse the chart data string into a ChartData struct
	var chartData ChartData
	err := json.Unmarshal([]byte(data), &chartData)
	if err != nil {
		return "", fmt.Errorf("failed to parse chart data: %v", err)
	}

	// Create a simple image representation of the chart
	img := image.NewRGBA(image.Rect(0, 0, 400, 300))
	draw.Draw(img, img.Bounds(), &image.Uniform{color.White}, image.ZP, draw.Src)

	// Draw chart title
	dr := &font.Drawer{
		Dst:  img,
		Src:  image.Black,
		Face: basicfont.Face7x13,
		Dot:  fixed.Point26_6{X: 10 << 6, Y: 20 << 6},
	}
	dr.DrawString(chartData.Title)

	// Draw some random data points for demonstration purposes
	for i, value := range chartData.Data {
		x := 50 + i*20
		y := 250 - int(value*20)
		img.Set(x, y, color.RGBA{R: uint8(rand.Intn(256)), G: uint8(rand.Intn(256)), B: uint8(rand.Intn(256)), A: 255})
	}

	// Save the image to a temporary file
	tempFile, err := os.CreateTemp("", "chart_export_*.png")
	if err != nil {
		return "", fmt.Errorf("failed to create temp file: %v", err)
	}
	defer tempFile.Close()

	err = png.Encode(tempFile, img)
	if err != nil {
		return "", fmt.Errorf("failed to encode image: %v", err)
	}

	return tempFile.Name(), nil
}