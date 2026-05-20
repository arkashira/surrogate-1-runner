package com.axentx.surrogate1.resource;

import java.util.Optional;

public interface ResourceService {

    Optional<String> getResourceById(String resourceId);
}