import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';
import { Box, Button, FormControl, FormLabel, Heading, RadioGroup, Radio, Stack, Textarea, Text, VStack, HStack, Flex } from '@chakra-ui/react';

const RatingStars = ({ value, onChange }) => (
  // ...
);

const FeedbackForm = ({ onSubmit, analyticsEnabled = true }) => (
  // ...

  useEffect(() => {
    if (!analyticsEnabled) return;
    const trackEvent = (eventType, data) => {
      // ...
    };

    const handleSubmit = async () => {
      // ...
      trackEvent('feedback_submit_attempt', {
        rating: formData.rating,
        type: formData.type,
      });
      try {
        await onSubmit?.({ ...formData, analytics });
        trackEvent('feedback_submit_success', {
          rating: formData.rating,
          type: formData.type,
        });
      } catch (e) {
        trackEvent('feedback_submit_error', { error: e.message });
      }
    };

    // ...
  }, [formData, analytics]);

  // ...
);

// ...