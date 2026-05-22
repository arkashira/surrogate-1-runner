package com.axentx.surrogate1.alert;

import com.axentx.surrogate1.data.AnomalyData;
import com.axentx.surrogate1.data.Recommendation;
import com.axentx.surrogate1.data.RecommendationEngine;
import com.axentx.surrogate1.data.HistoricalData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class AlertService {
    private static final Logger logger = LoggerFactory.getLogger(AlertService.class);
    private final RecommendationEngine recommendationEngine;
    private final HistoricalData historicalData;

    public AlertService(RecommendationEngine recommendationEngine, HistoricalData historicalData) {
        this.recommendationEngine = recommendationEngine;
        this.historicalData = historicalData;
    }

    /**
     * 发送异常警报并附带推荐措施
     * @param anomalyData 异常数据对象
     */
    public void sendAlert(AnomalyData anomalyData) {
        try {
            List<Recommendation> recommendations = recommendationEngine.generateRecommendations(anomalyData, historicalData);
            
            // 记录警报日志（实际生产中可扩展为邮件/Slack通知）
            logger.warn("ALERT: Detected anomaly - Usage: {} > Avg: {}", 
                       anomalyData.getUsage(), historicalData.getAverageUsage());
            logger.info("Recommendations: {}", recommendations);
            
            // 可选：调用外部通知系统（示例：发送邮件）
            // sendNotification(anomalyData, recommendations);
        } catch (Exception e) {
            logger.error("Failed to send alert for anomaly: {}", anomalyData, e);
        }
    }
}