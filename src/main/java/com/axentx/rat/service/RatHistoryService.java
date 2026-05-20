package com.axentx.rat.service;

import com.axentx.rat.model.HistoricalBalance;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
public class RatHistoryService {

    public Page<HistoricalBalance> getHistoricalBalances(int page, int size) {
        // Validate size parameter
        if (size < 1 || size > 100) {
            throw new IllegalArgumentException("Size must be between 1 and 100");
        }

        // Create pageable object with sorting by date descending
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "date"));

        // In a real implementation, this would query a database
        // For now, returning an empty page as placeholder
        return Page.empty(pageable);
    }
}