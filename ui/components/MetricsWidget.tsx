import React from 'react';
import axios from 'axios';

interface Metrics {
    total_alerts_received: number;
    alerts_consolidated: number;
    noise_alerts_identified: number;
    reduction_percentage: number;
}

const MetricsWidget: React.FC = () => {
    const [metrics, setMetrics] = React.useState<Metrics | null>(null);

    React.useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const response = await axios.get('/api/metrics');
                setMetrics(response.data);
            } catch (error) {
                console.error('Failed to fetch metrics:', error);
            }
        };

        fetchMetrics();
    }, []);

    if (!metrics) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Alert Metrics</h2>
            <p>Total Alerts Received: {metrics.total_alerts_received}</p>
            <p>Alerts Consolidated: {metrics.alerts_consolidated}</p>
            <p>Noise Alerts Identified: {metrics.noise_alerts_identified}</p>
            <p>Reduction Percentage: {metrics.reduction_percentage * 100}%</p>
        </div>
    );
};

export default MetricsWidget;