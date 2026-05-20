const db = require('../db');

class ManufacturerService {
  async createProfile(manufacturerData) {
    const {
      companyName,
      certifications,
      pricingModel,
      productionCapacity,
      description,
      keywords,
    } = manufacturerData;

    if (!companyName || !pricingModel || !productionCapacity) {
      throw new Error('Missing required fields');
    }

    const query = `
      INSERT INTO manufacturer_profiles 
      (company_name, certifications, pricing_model, production_capacity, description, keywords)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *;
    `;

    const values = [
      companyName,
      certifications,
      pricingModel,
      productionCapacity,
      description,
      keywords,
    ];
    const result = await db.query(query, values);
    return result.rows[0];
  }

  async getProfileById(id) {
    const result = await db.query('SELECT * FROM manufacturer_profiles WHERE id = $1', [id]);
    return result.rows[0];
  }

  async searchProfiles(keyword) {
    const query = `
      SELECT * FROM manufacturer_profiles 
      WHERE company_name ILIKE $1 
      OR description ILIKE $1 
      OR keywords ILIKE $1;
    `;
    const result = await db.query(query, [`%${keyword}%`]);
    return result.rows;
  }

  async updateProfile(id, updateData) {
    const fields = Object.keys(updateData);
    const values = Object.values(updateData);
    const setClause = fields.map((field, index) => `${field} = $${index + 2}`).join(', ');

    const query = `UPDATE manufacturer_profiles SET ${setClause} WHERE id = $1 RETURNING *`;
    const result = await db.query(query, [id, ...values]);
    return result.rows[0];
  }
}

module.exports = new ManufacturerService();