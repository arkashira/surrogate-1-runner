package com.axentx.surrogate1.invoice;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.ui.Model;

@Controller
public class InvoiceUploadController {

    private final InvoiceParser invoiceParser;

    public InvoiceUploadController(InvoiceParser invoiceParser) {
        this.invoiceParser = invoiceParser;
    }

    @PostMapping("/upload-invoice")
    public String handleFileUpload(@RequestParam("file") MultipartFile file, Model model) {
        if (!file.isEmpty()) {
            try {
                String result = invoiceParser.parse(file.getInputStream());
                model.addAttribute("result", result);
                return "invoice-upload";
            } catch (Exception e) {
                model.addAttribute("message", "Error uploading file");
                return "error";
            }
        } else {
            model.addAttribute("message", "Please select a file to upload.");
            return "error";
        }
    }
}