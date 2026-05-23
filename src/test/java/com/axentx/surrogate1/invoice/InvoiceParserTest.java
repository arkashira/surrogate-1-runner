package com.axentx.surrogate1.invoice;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class InvoiceParserTest {

    private final InvoiceParser parser = new InvoiceParser();

    @Test
    public void testParseInvoice_validInput() {
        String invoiceText = "Item A 10.00\nItem B 20.50\nItem C 5.75";

        List<InvoiceParser.LineItem> lineItems = parser.parseInvoice(invoiceText);

        assertEquals(3, lineItems.size());
        assertEquals("Item A", lineItems.get(0).getDescription());
        assertEquals(10.00, lineItems.get(0).getAmount());
        assertEquals("Item B", lineItems.get(1).getDescription());
        assertEquals(20.50, lineItems.get(1).getAmount());
        assertEquals("Item C", lineItems.get(2).getDescription());
        assertEquals(5.75, lineItems.get(2).getAmount());
    }

    @Test
    public void testParseInvoice_invalidAmountFormat() {
        String invoiceText = "Item A 10.00\nItem B invalid\nItem C 5.75";

        assertThrows(IllegalArgumentException.class, () -> parser.parseInvoice(invoiceText));
    }

    @Test
    public void testParseInvoice_nullOrEmptyInput() {
        assertThrows(IllegalArgumentException.class, () -> parser.parseInvoice(null));
        assertThrows(IllegalArgumentException.class, () -> parser.parseInvoice(""));
    }
}