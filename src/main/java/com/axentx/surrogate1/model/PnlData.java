package com.axentx.surrogate1.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Simple DTO representing Profit & Loss figures.
 */
public class PnlData {

    private final double revenue;
    private final double expense;
    private final double profit;

    @JsonCreator
    public PnlData(
            @JsonProperty("revenue") double revenue,
            @JsonProperty("expense") double expense,
            @JsonProperty("profit") double profit) {
        this.revenue = revenue;
        this.expense = expense;
        this.profit = profit;
    }

    public double getRevenue() {
        return revenue;
    }

    public double getExpense() {
        return expense;
    }

    public double getProfit() {
        return profit;
    }

    @Override
    public String toString() {
        return "PnlData{" +
                "revenue=" + revenue +
                ", expense=" + expense +
                ", profit=" + profit +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        PnlData pnlData = (PnlData) o;

        if (Double.compare(pnlData.revenue, revenue) != 0) return false;
        if (Double.compare(pnlData.expense, expense) != 0) return false;
        return Double.compare(pnlData.profit, profit) == 0;
    }

    @Override
    public int hashCode() {
        int result;
        long temp;
        temp = Double.doubleToLongBits(revenue);
        result = (int) (temp ^ (temp >>> 32));
        temp = Double.doubleToLongBits(expense);
        result = 31 * result + (int) (temp ^ (temp >>> 32));
        temp = Double.doubleToLongBits(profit);
        result = 31 * result + (int) (temp ^ (temp >>> 32));
        return result;
    }
}