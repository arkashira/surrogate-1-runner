package com.axentx.rat.controller;

import com.axentx.rat.exception.InvalidClientException;
import com.axentx.rat.model.PlaidLinkToken;
import com.axentx.rat.service.PlaidLinkService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class PlaidLinkControllerTest {

    @Mock
    private PlaidLinkService plaidLinkService;

    @InjectMocks
    private PlaidLinkController plaidLinkController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void createLinkToken_shouldReturnPlaidLinkToken_whenClientCredentialsAreValid() {
        // Arrange
        String clientId = "validClientId";
        String clientSecret = "validClientSecret";
        PlaidLinkToken expectedToken = new PlaidLinkToken("linkToken123", "stateToken123");

        when(plaidLinkService.createLinkToken(clientId, clientSecret))
                .thenReturn(expectedToken);

        // Act
        ResponseEntity<PlaidLinkToken> response = plaidLinkController.createLinkToken(clientId, clientSecret);

        // Assert
        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(expectedToken, response.getBody());
        verify(plaidLinkService, times(1)).createLinkToken(clientId, clientSecret);
    }

    @Test
    void createLinkToken_shouldReturnBadRequest_whenClientCredentialsAreInvalid() {
        // Arrange
        String clientId = "invalidClientId";
        String clientSecret = "invalidClientSecret";

        when(plaidLinkService.createLinkToken(clientId, clientSecret))
                .thenThrow(new InvalidClientException("Invalid client credentials"));

        // Act
        ResponseEntity<PlaidLinkToken> response = plaidLinkController.createLinkToken(clientId, clientSecret);

        // Assert
        assertNotNull(response);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNull(response.getBody());
        verify(plaidLinkService, times(1)).createLinkToken(clientId, clientSecret);
    }
}