export const validateProfile = (data) => {
  const errors = {};

  if (!data.businessModel?.trim())
    errors.businessModel = 'Business model is required.';

  if (!data.fundingStage?.trim())
    errors.fundingStage = 'Funding stage is required.';

  if (!data.location?.trim())
    errors.location = 'Location is required.';

  return errors;
};