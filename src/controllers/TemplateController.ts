import { Request, Response } from 'express';
import Template, { ITemplate } from '../models/Template';

/**
 * Helper to send a uniform error response
 */
const sendError = (res: Response, status: number, message: string) => {
  console.error(message);
  return res.status(status).json({ error: message });
};

/**
 * Create a new workflow template
 */
export const createTemplate = async (req: Request, res: Response) => {
  try {
    const { name, description, steps, parameters } = req.body;
    const template = await Template.create({ name, description, steps, parameters });
    return res.status(201).json(template);
  } catch (err: any) {
    // Duplicate key error
    if (err.code === 11000) {
      return sendError(res, 409, 'Template name must be unique');
    }
    return sendError(res, 400, err.message);
  }
};

/**
 * Retrieve a single template by ID
 */
export const getTemplate = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const template = await Template.findById(id).lean();
    if (!template) return sendError(res, 404, 'Template not found');
    return res.json(template);
  } catch (err: any) {
    return sendError(res, 400, err.message);
  }
};

/**
 * List all templates – newest first
 */
export const listTemplates = async (_req: Request, res: Response) => {
  try {
    const templates = await Template.find().sort({ createdAt: -1 }).lean();
    return res.json(templates);
  } catch (err: any) {
    return sendError(res, 400, err.message);
  }
};

/**
 * Update an existing template
 */
export const updateTemplate = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    const template = await Template.findByIdAndUpdate(id, updates, {
      new: true,
      runValidators: true,
    }).lean();
    if (!template) return sendError(res, 404, 'Template not found');
    return res.json(template);
  } catch (err: any) {
    return sendError(res, 400, err.message);
  }
};

/**
 * Delete a template
 */
export const deleteTemplate = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const result = await Template.findByIdAndDelete(id);
    if (!result) return sendError(res, 404, 'Template not found');
    return res.status(204).send();
  } catch (err: any) {
    return sendError(res, 400, err.message);
  }
};