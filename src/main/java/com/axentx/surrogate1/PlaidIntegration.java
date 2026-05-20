package com.axentx.surrogate1;

import com.plaid.client.PlaidClient;
import com.plaid.client.request.ItemPublicTokenExchangeRequest;
import com.plaid.client.response.ItemPublicTokenExchangeResponse;
import com.plaid.client.response.TransactionsGetResponse;

public class PlaidIntegration {

    private static final String PLaid_CLIENT_ID = "your_plaid_client_id";
    private static final String PLaid_SECRET = "your_plaid_secret";

    public static void main(String[] args) {
        // Initialize Plaid client
        PlaidClient plaidClient = PlaidClient.newBuilder()
                .clientId(PLaid_CLIENT_ID)
                .secret(PLaid_SECRET)
                .build();

        // Example method calls
        exchangePublicToken(plaidClient);
        getTransactions(plaidClient);
    }

    private static void exchangePublicToken(PlaidClient plaidClient) {
        ItemPublicTokenExchangeRequest request = ItemPublicTokenExchangeRequest.builder()
                .publicToken("your_public_token")
                .build();
        try {
            ItemPublicTokenExchangeResponse response = plaidClient.itemPublicTokenExchange(request);
            System.out.println("Access Token: " + response.getAccessToken());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void getTransactions(PlaidClient plaidClient) {
        // Assuming we have an access token from the previous step
        String accessToken = "your_access_token";
        TransactionsGetResponse response = plaidClient.transactionsGet(
                accessToken,
                "start_date", // Replace with actual start date
                "end_date"    // Replace with actual end date
        );
        System.out.println("Transactions: " + response.getTransactions());
    }
}