package com.axentx.rat.service;

import com.axentx.rat.model.BalanceHistory;
import com.axentx.rat.repository.BalanceHistoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class BalanceHistoryService {

    @Autowired
    private BalanceHistoryRepository balanceHistoryRepository;

    public Page<BalanceHistory> findAll(Pageable pageable) {
        return balanceHistoryRepository.findAll(pageable);
    }
}