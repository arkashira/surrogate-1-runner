package com.axentx.surrogate.service;

import com.axentx.surrogate.model.PLData;
import com.axentx.surrogate.repository.PLDataRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class PLTrendService {

    @Autowired
    private PLDataRepository plDataRepository;

    public List<PLData> getPLTrend(int months) {
        LocalDate endDate = LocalDate.now();
        LocalDate startDate = endDate.minusMonths(months);

        return plDataRepository.findByDateBetween(startDate, endDate);
    }
}