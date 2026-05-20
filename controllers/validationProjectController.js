const { createOrUpdateValidationProject } = require('../services/validationProjectService');
const { serializeValidationProject } = require('../serializers/validationProjectSerializer');

exports.createOrUpdateValidationProject = async (req, res, next) => {
  try {
    const project = await createOrUpdateValidationProject(req.body);
    res.status(project.isNew ? 201 : 200).json(serializeValidationProject(project));
  } catch (err) {
    next(err); // let error‑handler middleware format the response
  }
};