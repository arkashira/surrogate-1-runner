package com.axentx.surrogate1.resource;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class ResourceMapper {

    private final ResourceService resourceService;

    public ResourceMapper(ResourceService resourceService) {
        this.resourceService = resourceService;
    }

    public Map<String, String> mapInvoiceLineItems(List<Map<String, String>> invoiceLineItems) {
        return invoiceLineItems.stream()
                .collect(Collectors.toMap(
                        item -> item.get("ID"),
                        item -> {
                            String resourceName = item.get("Name");
                            String resourceId = item.get("ID");
                            return resourceService.getResourceById(resourceId)
                                    .map(resource -> "mapped")
                                    .orElseGet(() -> suggestResource(resourceName));
                        }
                ));
    }

    private String suggestResource(String resourceName) {
        // Logic to suggest possible resources based on name
        return "unmapped - suggestion needed";
    }
}