package com.axentx.surrogate.service;

import com.axentx.surrogate.model.PLData;
import com.axentx.surrogate.repository.PLDataRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

class PLTrendServiceTest {

    @Mock
    private PLDataRepository plDataRepository;

    @InjectMocks
    private PLTrendService plTrendService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void getPLTrend() {
        LocalDate endDate = LocalDate.now();
        LocalDate startDate = endDate.minusMonths(3);

        PLData plData1 = new PLData();
        plData1.setDate(startDate);
        plData1.setProfit(1000.0);
        plData1.setLoss(500.0);

        PLData plData2 = new PLData();
        plData2.setDate(endDate);
        plData2.setProfit(2000.0);
        plData2.setLoss(1000.0);

        List<PLData> expectedPLData = Arrays.asList(plData1, plData2);

        when(plDataRepository.findByDateBetween(startDate, endDate)).thenReturn(expectedPLData);

        List<PLData> actualPLData = plTrendService.getPLTrend(3);

        assertEquals(expectedPLData.size(), actualPLData.size());
        assertEquals(expectedPLData.get(0).getProfit(), actualPLData.get(0).getProfit());
        assertEquals(expectedPLData.get(1).getLoss(), actualPLData.get(1).getLoss());
    }
}