const ValidationProject = require('../models/validationProject');
const {
  validateCreateValidationProject,
  validateUpdateValidationProject,
} = require('../validators/validationProjectValidator');

exports.createOrUpdateValidationProject = async (data) => {
  if (data.id) {
    // UPDATE
    validateUpdateValidationProject(data);
    const project = await ValidationProject.findByIdAndUpdate(
      data.id,
      { $set: data },
      { new: true, runValidators: true }
    );
    return project;
  } else {
    // CREATE
    validateCreateValidationProject(data);
    const project = new ValidationProject(data);
    await project.save();
    return project;
  }
};