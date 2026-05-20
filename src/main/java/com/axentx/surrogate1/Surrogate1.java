package com.axentx.surrogate1;

import com.axentx.surrogate1.analyzer.ConcurrentCollectionAnalyzer;

public class Surrogate1 {
    private ConcurrentCollectionAnalyzer analyzer;

    public Surrogate1() {
        this.analyzer = new ConcurrentCollectionAnalyzer();
    }

    public void analyzeCode(String code) {
        analyzer.detectRaceConditions(code);
    }

    public static void main(String[] args) {
        Surrogate1 surrogate = new Surrogate1();
        String sampleCode = "/* Sample concurrent collection code */";
        surrogate.analyzeCode(sampleCode);
    }
}