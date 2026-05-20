const { v4: uuidv4 } = require('uuid');
const knex = require('../db'); // assumes knex instance exported from src/db.js

/**
 * Persist the current state of the Roth wizard.
 * Expects JSON body:
 * {
 *   client_id: string,
 *   state: object   // wizard state data
 * }
 */
exports.saveWizardState = async (req, res) => {
  try {
    const { client_id, state } = req.body;

    if (!client_id || typeof state !== 'object') {
      return res.status(400).json({
        error: 'Missing or invalid client_id or state',
      });
    }

    const id = uuidv4();
    const now = new Date();

    await knex('roth_wizard_states').insert({
      id,
      client_id,
      state_data: JSON.stringify(state),
      created_at: now,
      updated_at: now,
    });

    return res.status(201).json({ id });
  } catch (err) {
    console.error('Error saving wizard state:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

/**
 * Retrieve a persisted wizard state by its ID.
 * URL param: id
 */
exports.getWizardState = async (req, res) => {
  try {
    const { id } = req.params;
    const record = await knex('roth_wizard_states')
      .select('client_id', 'state_data', 'created_at', 'updated_at')
      .where({ id })
      .first();

    if (!record) {
      return res.status(404).json({ error: 'State not found' });
    }

    return res.status(200).json({
      id,
      client_id: record.client_id,
      state: JSON.parse(record.state_data),
      created_at: record.created_at,
      updated_at: record.updated_at,
    });
  } catch (err) {
    console.error('Error retrieving wizard state:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
};