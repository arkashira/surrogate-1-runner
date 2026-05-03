import { Schema, model } from 'mongoose';

const TeamSchema = new Schema({
  name: { type: String, required: true, unique: true },
  slackWebhookUrl: { type: String, required: false }, // per-team webhook
  createdAt: { type: Date, default: Date.now },
});

export const Team = model('Team', TeamSchema);