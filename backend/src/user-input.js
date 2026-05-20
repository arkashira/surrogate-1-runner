/**
 * Parses raw user input (query string, JSON body, etc.) into a well‑typed
 * object that the review engine can rely on.
 *
 * Expected shape:
 * {
 *   productId: string,               // required
 *   budget?: number,                 // optional – defaults to Infinity
 *   priorities?: string[],           // optional – defaults to ["overall"]
 *   filters?: {
 *     brand?: string,
 *     minRating?: number
 *   },
 *   // Optional: an array of historic user reviews (used by aggregation)
 *   reviews?: Array<{productId:string, rating:number, comment:string}>
 * }
 */
function parseUserInput(rawInput) {
  if (!rawInput || typeof rawInput !== "object") {
    throw new TypeError("User input must be a non‑null object");
  }

  const {
    productId,
    budget,
    priorities,
    filters = {},
    reviews = []                     // may be omitted – default empty array
  } = rawInput;

  if (!productId) {
    throw new Error("`productId` is required");
  }

  // Normalise and apply defaults
  const parsed = {
    productId: String(productId).trim(),
    budget: typeof budget === "number" && budget > 0 ? budget : Infinity,
    priorities: Array.isArray(priorities) && priorities.length
      ? priorities.map(p => String(p).toLowerCase())
      : ["overall"],
    filters: {
      brand: filters.brand ? String(filters.brand).trim() : null,
      minRating: typeof filters.minRating === "number" ? filters.minRating : 0
    },
    // Keep the raw reviews array (will be validated later)
    reviews: Array.isArray(reviews) ? reviews : []
  };

  return parsed;
}

module.exports = { parseUserInput };