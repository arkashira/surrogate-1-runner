package com.axentx.surrogate.controller;

import com.axentx.surrogate.model.PLData;
import com.axentx.surrogate.service.PLTrendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class PLTrendController {

    @Autowired
    private PLTrendService plTrendService;

    @GetMapping("/api/pl-trend")
    public List<PLData> getPLTrend(@RequestParam int months) {
        return plTrendService.getPLTrend(months);
    }
}