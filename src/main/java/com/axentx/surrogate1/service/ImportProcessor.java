package com.axentx.surrogate1.service;

import com.axentx.surrogate1.model.FinancialData;
import com.axentx.surrogate1.model.ErrorLog;
import com.axentx.surrogate1.repository.FinancialDataRepository;
import com.axentx.surrogate1.repository.ErrorLogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@Service
public class ImportProcessor {

    @Autowired
    private FinancialDataRepository financialDataRepository;

    @Autowired
    private ErrorLogRepository errorLogRepository;

    @Async
    public CompletableFuture<Void> processCsv(MultipartFile file) {
        try {
            CsvToBean<FinancialData> csvToBean = new CsvToBeanBuilder<FinancialData>(new InputStreamReader(file.getInputStream()))
                .withType(FinancialData.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            List<FinancialData> records = csvToBean.parse();
            for (int i = 0; i < records.size(); i++) {
                try {
                    FinancialData data = records.get(i);
                    // Basic validation
                    if (data.getDate() == null || data.getAmount() <= 0) {
                        throw new IllegalArgumentException("Invalid data at line " + (i+1));
                    }
                    financialDataRepository.save(data);
                } catch (Exception e) {
                    errorLogRepository.save(new ErrorLog(
                        "CSV_IMPORT_ERROR", 
                        "Line " + (i+1) + ": " + e.getMessage(),
                        file.getOriginalName()
                    ));
                }
            }
        } catch (IOException e) {
            errorLogRepository.save(new ErrorLog("CSV_READ_ERROR", e.getMessage(), file.getOriginalName()));
        }
        return CompletableFuture.completedFuture(null);
    }
}