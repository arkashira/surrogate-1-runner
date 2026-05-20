/**
 * Validation middleware for Workio webhook payloads.
 *
 * Expected payload structure:
 * {
 *   task: {
 *     id: string,
 *     status: string,
 *     completed?: boolean
 *   },
 *   data: object (optional, passed to ingestion)
 * }
 *
 * If validation fails, returns a 400 status with actionable remediation.
 */

const requiredFields = ['task'];

function validateWorkioPayload(req, res, next) {
  const payload = req.body;

  // 1. Basic type check: payload must be an object
  if (typeof payload !== 'object' || payload === null || Array.isArray(payload)) {
    return res.status(400).json({
      error: 'Invalid payload: expected a JSON object',
      remediation: 'Ensure the webhook sends a valid JSON body',
    });
  }

  // 2. Check for missing top-level required fields
  const missing = requiredFields.filter((field) => !(field in payload));
  if (missing.length > 0) {
    return res.status(400).json({
      error: `Missing required field(s): ${missing.join(', ')}`,
      remediation: `Add the missing field(s) to the webhook payload`,
    });
  }

  const { task } = payload;

  // 3. Validate 'task' object structure
  if (typeof task !== 'object' || task === null || Array.isArray(task)) {
    return res.status(400).json({
      error: 'Invalid type for "task": expected an object',
      remediation: 'Include a "task" object with "id" and "status"',
    });
  }

  // 4. Validate 'task.id'
  if (typeof task.id !== 'string' || task.id.trim() === '') {
    return res.status(400).json({
      error: 'Missing or invalid "task.id"',
      remediation: 'Ensure "task.id" is a non-empty string',
    });
  }

  // 5. Validate 'task.status'
  if (typeof task.status !== 'string' || task.status.trim() === '') {
    return res.status(400).json({
      error: 'Missing or invalid "task.status"',
      remediation: 'Provide a valid "status" string (e.g., "completed")',
    });
  }

  // 6. Optional: Validate 'data' if present (for ingestion)
  if (payload.data !== undefined && (typeof payload.data !== 'object' || payload.data === null)) {
     return res.status(400).json({
      error: 'Invalid type for "data": expected an object',
      remediation: 'If including "data", it must be a JSON object',
    });
  }

  // All checks passed
  next();
}

module.exports = validateWorkioPayload;