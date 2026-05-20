package com.axentx.surrogate1.invoice;

import java.io.InputStream;
import java.util.Scanner;

public class InvoiceParser {

    public String parse(InputStream inputStream) {
        StringBuilder result = new StringBuilder();
        try (Scanner scanner = new Scanner(inputStream)) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                result.append(line).append("\n");
            }
        }
        return result.toString();
    }
}