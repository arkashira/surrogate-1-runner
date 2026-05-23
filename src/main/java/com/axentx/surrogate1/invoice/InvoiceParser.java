package com.axentx.surrogate1.invoice;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class InvoiceParser {

    public static class LineItem {
        private final String description;
        private final double amount;

        public LineItem(String description, double amount) {
            this.description = description;
            this.amount = amount;
        }

        public String getDescription() {
            return description;
        }

        public double getAmount() {
            return amount;
        }
    }

    public List<LineItem> parseInvoice(String invoiceText) {
        if (invoiceText == null || invoiceText.isEmpty()) {
            throw new IllegalArgumentException("Invoice text cannot be null or empty");
        }

        List<LineItem> lineItems = new ArrayList<>();
        String lineItemPattern = "(\\w[\\w\\s]*?)\\s+(\\d+\\.\\d{2})"; // Regex for line items

        Pattern pattern = Pattern.compile(lineItemPattern);
        Matcher matcher = pattern.matcher(invoiceText);

        while (matcher.find()) {
            String description = matcher.group(1).trim();
            try {
                double amount = Double.parseDouble(matcher.group(2));
                lineItems.add(new LineItem(description, amount));
            } catch (NumberFormatException e) {
                throw new IllegalArgumentException("Invalid amount format in invoice: " + matcher.group(2));
            }
        }

        return lineItems;
    }
}