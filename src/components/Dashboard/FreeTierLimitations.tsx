import React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

const FreeTierLimitations: React.FC = () => {
  const limitations = [
    'Limited to 100 API calls per day',
    'No access to premium features',
    'Basic support only',
    'No custom branding',
  ];

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
          Free Tier Limitations
        </Typography>
        <Typography variant="body1" gutterBottom>
          Here are the limitations of our free tier:
        </Typography>
        <List>
          {limitations.map((limitation, index) => (
            <React.Fragment key={index}>
              <ListItem>
                <ListItemText primary={limitation} />
              </ListItem>
              {index < limitations.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
        <Typography variant="body1" gutterBottom>
          Upgrade to our paid plans for more features and higher limits.
        </Typography>
      </CardContent>
    </Card>
  );
};

export default FreeTierLimitations;