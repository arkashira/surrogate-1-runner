import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import axios from 'axios';

interface ProfileFormData {
  businessName: string;
  industry: string;
  fundingStage: string;
  teamSize: string;
  keyAchievements: string;
  pitchDeck: FileList;
  videoIntroduction: FileList;
}

const schema = yup.object().shape({
  businessName: yup.string().required('Business name is required'),
  industry: yup.string().required('Industry is required'),
  fundingStage: yup.string().required('Funding stage is required'),
  teamSize: yup.string().required('Team size is required'),
  keyAchievements: yup.string().required('Key achievements are required'),
  pitchDeck: yup.mixed().required('Pitch deck is required'),
  videoIntroduction: yup.mixed().required('Video introduction is required'),
});

const ProfileForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<ProfileFormData>({
    resolver: yupResolver(schema),
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const onSubmit: SubmitHandler<ProfileFormData> = async (data) => {
    setIsSubmitting(true);
    const formData = new FormData();
    formData.append('businessName', data.businessName);
    formData.append('industry', data.industry);
    formData.append('fundingStage', data.fundingStage);
    formData.append('teamSize', data.teamSize);
    formData.append('keyAchievements', data.keyAchievements);
    formData.append('pitchDeck', data.pitchDeck[0]);
    formData.append('videoIntroduction', data.videoIntroduction[0]);

    try {
      await axios.post('/api/profile', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Profile saved successfully!');
    } catch (error) {
      console.error('Error saving profile:', error);
      alert('Error saving profile. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Business Name</label>
        <input {...register('businessName')} />
        {errors.businessName && <p>{errors.businessName.message}</p>}
      </div>
      <div>
        <label>Industry</label>
        <input {...register('industry')} />
        {errors.industry && <p>{errors.industry.message}</p>}
      </div>
      <div>
        <label>Funding Stage</label>
        <input {...register('fundingStage')} />
        {errors.fundingStage && <p>{errors.fundingStage.message}</p>}
      </div>
      <div>
        <label>Team Size</label>
        <input {...register('teamSize')} />
        {errors.teamSize && <p>{errors.teamSize.message}</p>}
      </div>
      <div>
        <label>Key Achievements</label>
        <textarea {...register('keyAchievements')} />
        {errors.keyAchievements && <p>{errors.keyAchievements.message}</p>}
      </div>
      <div>
        <label>Pitch Deck</label>
        <input type="file" {...register('pitchDeck')} />
        {errors.pitchDeck && <p>{errors.pitchDeck.message}</p>}
      </div>
      <div>
        <label>Video Introduction</label>
        <input type="file" {...register('videoIntroduction')} />
        {errors.videoIntroduction && <p>{errors.videoIntroduction.message}</p>}
      </div>
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Saving...' : 'Save Profile'}
      </button>
    </form>
  );
};

export default ProfileForm;