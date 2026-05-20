package com.axentx.rat.controller;

import com.axentx.rat.dto.LinkRequest;
import com.axentx.rat.dto.LinkResponse;
import com.axentx.rat.service.LinkService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

class LinkControllerTest {

    @Mock
    private LinkService linkService;

    @InjectMocks
    private LinkController linkController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void initiateLink_ValidRequest_ReturnsLinkToken() {
        LinkRequest linkRequest = new LinkRequest();
        linkRequest.setClientId("client-id");
        linkRequest.setClientSecret("client-secret");
        linkRequest.setCallbackUrl("https://example.com/callback");

        LinkResponse expectedResponse = new LinkResponse(null, "sample-link-token");
        when(linkService.initiateLink(linkRequest)).thenReturn(expectedResponse);

        ResponseEntity<LinkResponse> response = linkController.initiateLink(linkRequest);

        assertEquals(200, response.getStatusCodeValue());
        assertEquals(expectedResponse, response.getBody());
        verify(linkService, times(1)).initiateLink(linkRequest);
    }

    @Test
    void initiateLink_InvalidRequest_ReturnsBadRequest() {
        LinkRequest linkRequest = new LinkRequest();
        linkRequest.setClientId(null);
        linkRequest.setClientSecret(null);
        linkRequest.setCallbackUrl("https://example.com/callback");

        ResponseEntity<LinkResponse> response = linkController.initiateLink(linkRequest);

        assertEquals(400, response.getStatusCodeValue());
        assertEquals("Client ID and Secret are required", response.getBody().getError());
    }
}