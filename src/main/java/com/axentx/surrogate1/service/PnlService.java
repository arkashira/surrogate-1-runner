package com.axentx.surrogate1.service;

import org.springframework.stereotype.Service;
import com.axentx.surrogate1.model.PnlData;

@Service
public class PnlService {

    public PnlData getPnlData() {
        // Logic to fetch P&L data from the data source
        // This is a placeholder implementation
        PnlData pnlData = new PnlData();
        pnlData.setProfit(1000.0);
        pnlData.setLoss(200.0);
        return pnlData;
    }
}