import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';

/**
 * InputForm component allows users to enter a text prompt and submit it.
 * The submitted value is passed to the onSubmit callback.
 */
interface InputFormProps {
  onSubmit: (data: { name: string; email: string; comments: string }) => void;
}

export const InputForm: React.FC<InputFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    comments: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({ name: '', email: '', comments: '' });
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        Input Form
      </Typography>
      <TextField
        label="Name"
        variant="outlined"
        fullWidth
        name="name"
        value={formData.name}
        onChange={handleChange}
        required
        sx={{ mb: 2 }}
      />
      <TextField
        label="Email"
        variant="outlined"
        fullWidth
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        required
        sx={{ mb: 2 }}
      />
      <TextField
        label="Comments"
        variant="outlined"
        fullWidth
        multiline
        rows={4}
        name="comments"
        value={formData.comments}
        onChange={handleChange}
        sx={{ mb: 2 }}
      />
      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </Box>
  );
};