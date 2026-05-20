import React, { useEffect, useState } from "react";
import axios from "axios";

const FinancialInsightsTab = () => {
    const [config, setConfig] = useState({
        enabled: false,
        theme: "light",
        refreshInterval: 300
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const response = await axios.get("/api/config");
                setConfig({
                    enabled: response.data.features.financial_insights,
                    theme: response.data.ui.theme,
                    refreshInterval: response.data.ui.refresh_interval
                });
            } catch (error) {
                console.error("Failed to fetch config:", error);
                setConfig(prev => ({...prev, enabled: false}));
            } finally {
                setLoading(false);
            }
        };
        fetchConfig();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (!config.enabled) return null;

    return (
        <div className={`financial-insights-tab theme-${config.theme}`}>
            <h2>Financial Insights</h2>
            <p>Data refreshes every {config.refreshInterval} seconds</p>
            {/* Actual financial insights content would go here */}
        </div>
    );
};

export default FinancialInsightsTab;