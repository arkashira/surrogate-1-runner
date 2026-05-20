import React from 'react';
import { Card, CardContent, Typography, Chip, Box } from '@mui/material';
import { Variant } from '../types';

interface VariantComparisonCardProps {
  variant: Variant;
}

const VariantComparisonCard: React.FC<VariantComparisonCardProps> = ({ variant }) => {
  return (
    <Card sx={{ minWidth: 275, margin: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {variant.name}
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, marginTop: 2 }}>
          <Typography variant="body2">
            OpenAI Compatibility: <Chip label={variant.openaiCompatibility} color={variant.openaiCompatibility === 'full' ? 'success' : variant.openaiCompatibility === 'partial' ? 'warning' : 'error'} />
          </Typography>
          <Typography variant="body2">
            Model Context Protocol Version: {variant.modelContextProtocolVersion}
          </Typography>
          <Typography variant="body2">
            Containerization Requirements: {variant.containerizationRequirements.join(', ')}
          </Typography>
          <Typography variant="body2">
            Harness Pattern Type: {variant.harnessPatternType}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default VariantComparisonCard;