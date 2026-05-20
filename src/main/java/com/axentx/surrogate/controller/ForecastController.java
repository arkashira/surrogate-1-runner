package com.axentx.surrogate.controller;

import com.axentx.surrogate.forecasting.ForecastResult;
import com.axentx.surrogate.forecasting.ForecastingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/forecast")
public class ForecastController {

    @Autowired
    private ForecastingService forecastingService;

    @PostMapping
    public ForecastResult forecast(@RequestBody List<Double> historicalData, @RequestParam int forecastPeriods) {
        return forecastingService.forecast(historicalData, forecastPeriods);
    }
}