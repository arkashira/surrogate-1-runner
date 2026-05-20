package com.axentx.surrogate.service;

import com.axentx.surrogate.dto.TopCostDriverDto;
import com.axentx.surrogate.repository.CostRecordRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class CostRecordService {

    @Autowired private CostRecordRepository repo;

    /** Convert raw query result to DTO list */
    public List<TopCostDriverDto> getTopCostDrivers() {
        return repo.findTopCostDriversRaw().stream()
                .map(r -> new TopCostDriverDto(
                        (String) r[0],
                        (String) r[1],
                        ((Number) r[2]).intValue(),
                        (BigDecimal) r[3]))
                .collect(Collectors.toList());
    }
}