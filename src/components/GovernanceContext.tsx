import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Link,
  Box,
  useTheme,
} from '@mui/material';
import { Alert, Approval } from '../types';

interface GovernanceContextProps {
  alerts: Alert[];
  approvals: Approval[];
}

const GovernanceContext: React.FC<GovernanceContextProps> = ({
  alerts,
  approvals,
}) => {
  const [recentAlerts, setRecentAlerts] = useState<Alert[]>([]);
  const [recentApprovals, setRecentApprovals] = useState<Approval[]>([]);
  const theme = useTheme();

  useEffect(() => {
    // Keep only the newest 3 items (assuming arrays are already sorted by timestamp desc)
    setRecentAlerts(alerts.slice(0, 3));
    setRecentApprovals(approvals.slice(0, 3));
  }, [alerts, approvals]);

  const renderItem = (
    item: Alert | Approval,
    color: string,
    key: string
  ) => (
    <Box
      key={key}
      sx={{
        display: 'flex',
        alignItems: 'center',
        mt: 1,
      }}
    >
      <Box
        sx={{
          width: 10,
          height: 10,
          bgcolor: color,
          borderRadius: '50%',
          mr: 1,
        }}
      />
      <Typography variant="body2">
        {item.message}{' '}
        <Link
          href={item.link}
          target="_blank"
          rel="noopener noreferrer"
          underline="hover"
        >
          View Details
        </Link>
      </Typography>
    </Box>
  );

  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6" component="div">
          Governance Context
        </Typography>

        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle1">Recent Alerts</Typography>
          {recentAlerts.map((alert) => renderItem(alert, theme.palette.error.main, alert.id))}
        </Box>

        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle1">Recent Approvals</Typography>
          {recentApprovals.map((approval) =>
            renderItem(approval, theme.palette.success.main, approval.id)
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default GovernanceContext;