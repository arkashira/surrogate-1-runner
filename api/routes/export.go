package routes

import (
	"net/http"
	"github.com/gin-gonic/gin"
	"image/png"
	"os"
	"fmt"
	"opt/axentx/surrogate-1/internal/utils/chart_exporter"
)

func SetupExportRoutes(router *gin.Engine) {
	router.POST("/export/chart", ExportChartHandler)
}

func ExportChartHandler(c *gin.Context) {
	chartData := c.PostForm("chart_data")
	fileFormat := c.PostForm("format") // Expected values: "png", "pdf"

	if chartData == "" || fileFormat == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Missing chart_data or format"})
		return
	}

	// Call the chart exporter utility function
	exportedFilePath, err := chart_exporter.ExportChart(chartData, fileFormat)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": fmt.Sprintf("Failed to export chart: %v", err)})
		return
	}

	// Serve the exported file
	http.ServeFile(c.Writer, c.Request, exportedFilePath)

	// Clean up the temporary file after serving
	defer func() {
		err := os.Remove(exportedFilePath)
		if err != nil {
			fmt.Println("Failed to remove PNG file:", err)
		}
	}()
}