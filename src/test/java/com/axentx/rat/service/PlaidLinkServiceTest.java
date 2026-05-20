package com.axentx.rat.service;

import com.axentx.rat.exception.InvalidClientException;
import com.axentx.rat.model.ClientCredentials;
import com.axentx.rat.model.PlaidLinkToken;
import com.axentx.rat.repository.ClientCredentialsRepository;
import com.axentx.rat.repository.PlaidLinkTokenRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class PlaidLinkServiceTest {

    @Mock
    private ClientCredentialsRepository clientCredentialsRepository;

    @Mock
    private PlaidLinkTokenRepository plaidLinkTokenRepository;

    @InjectMocks
    private PlaidLinkService plaidLinkService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void createLinkToken_shouldReturnPlaidLinkToken_whenClientCredentialsAreValid() {
        // Arrange
        String clientId = "validClientId";
        String clientSecret = "validClientSecret";
        ClientCredentials clientCredentials = new ClientCredentials(clientId, clientSecret);
        PlaidLinkToken expectedToken = new PlaidLinkToken("linkToken123", "stateToken123");

        when(clientCredentialsRepository.findByClientIdAndClientSecret(clientId, clientSecret))
                .thenReturn(clientCredentials);
        when(plaidLinkTokenRepository.createLinkToken(clientCredentials))
                .thenReturn(expectedToken);

        // Act
        PlaidLinkToken actualToken = plaidLinkService.createLinkToken(clientId, clientSecret);

        // Assert
        assertNotNull(actualToken);
        assertEquals(expectedToken.getLinkToken(), actualToken.getLinkToken());
        assertEquals(expectedToken.getStateToken(), actualToken.getStateToken());
        verify(clientCredentialsRepository, times(1)).findByClientIdAndClientSecret(clientId, clientSecret);
        verify(plaidLinkTokenRepository, times(1)).createLinkToken(clientCredentials);
    }

    @Test
    void createLinkToken_shouldThrowInvalidClientException_whenClientCredentialsAreInvalid() {
        // Arrange
        String clientId = "invalidClientId";
        String clientSecret = "invalidClientSecret";

        when(clientCredentialsRepository.findByClientIdAndClientSecret(clientId, clientSecret))
                .thenReturn(null);

        // Act & Assert
        assertThrows(InvalidClientException.class, () -> plaidLinkService.createLinkToken(clientId, clientSecret));
        verify(clientCredentialsRepository, times(1)).findByClientIdAndClientSecret(clientId, clientSecret);
        verify(plaidLinkTokenRepository, never()).createLinkToken(any());
    }
}