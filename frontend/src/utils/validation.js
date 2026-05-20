const validation = {
  validateForm: (formData) => {
    const requiredFields = ['template', 'modelName', 'taskType', 'dataSource'];

    for (const field of requiredFields) {
      if (!formData[field]) {
        return { success: false, message: `Field ${field} is required.` };
      }
    }

    return { success: true };
  },
};

export default validation;