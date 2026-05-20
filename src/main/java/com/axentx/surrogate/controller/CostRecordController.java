package com.axentx.surrogate.controller;

import com.axentx.surrogate.dto.TopCostDriverDto;
import com.axentx.surrogate.service.CostRecordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cost-records")
public class CostRecordController {

    @Autowired private CostRecordService service;

    @GetMapping("/top-cost-drivers")
    public List<TopCostDriverDto> getTopCostDrivers() {
        return service.getTopCostDrivers();
    }
}