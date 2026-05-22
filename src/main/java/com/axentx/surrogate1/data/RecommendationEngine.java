package com.axentx.surrogate1.data;

import com.axentx.surrogate1.data.AnomalyData;
import com.axentx.surrogate1.data.HistoricalData;
import com.axentx.surrogate1.data.Recommendation;

import java.util.ArrayList;
import java.util.List;

public class RecommendationEngine {
    /**
     * 根据历史数据和阈值生成推荐措施
     * @param anomalyData 当前异常数据
     * @param historicalData 历史数据
     * @return 推荐列表
     */
    public List<Recommendation> generateRecommendations(AnomalyData anomalyData, HistoricalData historicalData) {
        List<Recommendation> recommendations = new ArrayList<>();
        
        // 1. 资源使用率过高建议
        if (anomalyData.getUsage() > historicalData.getAverageUsage() * 1.2) {
            recommendations.add(new Recommendation(
                "Reduce resource consumption", 
                "Current usage exceeds 20% above historical average"
            ));
        }
        
        // 2. 预防性维护建议（示例）
        if (anomalyData.getUsage() > historicalData.getAverageUsage() * 1.5) {
            recommendations.add(new Recommendation(
                "Schedule maintenance", 
                "Critical threshold reached - risk of system failure"
            ));
        }
        
        return recommendations;
    }
}