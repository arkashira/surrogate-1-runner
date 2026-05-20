/**
 * Demo responses used by the tutorial API.
 *
 * Each key corresponds to an `action` query parameter that can be
 * passed to the demoCall API endpoint. The values are plain JSON
 * objects that emulate realistic responses from Surrogate-1.
 *
 * The `default` key is used when an unknown action is requested.
 */
const demoResponses = {
  default: {
    message: 'This is a default demo response. Try specifying an action.',
  },
  getUser: {
    user: {
      id: 123,
      name: 'Alice',
      email: 'alice@example.com',
    },
  },
  listItems: {
    items: [
      { id: 1, name: 'Item One', status: 'available' },
      { id: 2, name: 'Item Two', status: 'out_of_stock' },
      { id: 3, name: 'Item Three', status: 'available' },
    ],
  },
  liveData: {
    timestamp: new Date().toISOString(),
    data: {
      temperature: 22.5,
      humidity: 45,
    },
  },
};

module.exports = { demoResponses };