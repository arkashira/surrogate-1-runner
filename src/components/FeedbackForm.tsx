import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import axios from 'axios';

const schema = yup.object().shape({
  name: yup.string().required('Name is required'),
  email: yup.string().email('Invalid email').required('Email is required'),
  feedback: yup.string().required('Feedback is required'),
});

const FeedbackForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
  });

  const [isSubmitted, setIsSubmitted] = useState(false);

  const onSubmit = async (data) => {
    try {
      await axios.post('/api/feedback', data);
      setIsSubmitted(true);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  if (isSubmitted) {
    return <div>Thank you for your feedback!</div>;
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" {...register('name')} />
        {errors.name && <p>{errors.name.message}</p>}
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" {...register('email')} />
        {errors.email && <p>{errors.email.message}</p>}
      </div>
      <div>
        <label htmlFor="feedback">Feedback</label>
        <textarea id="feedback" {...register('feedback')} />
        {errors.feedback && <p>{errors.feedback.message}</p>}
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default FeedbackForm;