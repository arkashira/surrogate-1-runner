import { Schema, model } from 'mongoose';
import crypto from 'crypto';

const RequestSchema = new Schema({
  title: { type: String, required: true },
  status: { type: String, enum: ['open', 'in_progress', 'done', 'cancelled'], default: 'open' },
  dueAt: { type: Date, required: false },
  watchers: [{ type: String }], // user IDs or emails
  teamId: { type: Schema.Types.ObjectId, ref: 'Team', required: true },
  unsubscribeToken: {
    type: String,
    required: true,
    default: () => crypto.randomBytes(16).toString('hex'),
  },
  createdAt: { type: Date, default: Date.now },
});

RequestSchema.methods.isOverdue = function (): boolean {
  return this.dueAt != null && this.dueAt < new Date() && this.status !== 'done' && this.status !== 'cancelled';
};

export const Request = model('Request', RequestSchema);