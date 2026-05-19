/**
 * Pricing Service - handles API calls for pricing suggestions
 * Based on PRD 20260503-083750-reddit-7f5c09f16b298afe
 */

const API_BASE_URL = process.env.REACT_APP_PRICING_API_URL || '/api/pricing';

/**
 * Fetch pricing suggestions based on product details
 * @param {Object} productData - Product information
 * @returns {Promise<Object>} Pricing suggestions with confidence score
 */
export async function fetchPricingSuggestions(productData) {
  const { name, description, features, targetAudience } = productData;
  
  if (!name || !description || !features || features.length === 0) {
    throw new Error('Product name, description, and at least one feature are required');
  }

  const requestBody = {
    product_name: name,
    description,
    features: Array.isArray(features) ? features : [features],
    target_audience: targetAudience || '',
    timestamp: new Date().toISOString(),
  };

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5000);

  try {
    const response = await fetch(`${API_BASE_URL}/suggestions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(requestBody),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error ${response.status}`);
    }

    const data = await response.json();
    return transformPricingResponse(data);
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }
    throw error;
  }
}

function transformPricingResponse(apiResponse) {
  return {
    priceRange: {
      min: apiResponse.price_min ?? apiResponse.price_range?.min ?? 0,
      max: apiResponse.price_max ?? apiResponse.price_range?.max ?? 0,
      suggested: apiResponse.price_suggested ?? apiResponse.price_range?.mid ?? 0,
      currency: apiResponse.currency || 'USD',
    },
    confidenceScore: apiResponse.confidence_score ?? apiResponse.confidence ?? 0,
    competitorComparison: apiResponse.competitors ?? apiResponse.competitor_comparison ?? [],
    marketBenchmarks: apiResponse.benchmarks ?? {},
    metadata: {
      dataPointsUsed: apiResponse.data_points ?? 0,
      modelVersion: apiResponse.model_version ?? 'unknown',
      lastUpdated: apiResponse.timestamp ?? new Date().toISOString(),
    },
  };
}

export async function getMockPricingSuggestions(productData) {
  await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1500));
  
  const seed = productData.name?.length || 10;
  const basePrice = 29.99 + (seed * 3.5);
  
  return {
    priceRange: {
      min: Math.round(basePrice * 0.7 * 100) / 100,
      max: Math.round(basePrice * 1.4 * 100) / 100,
      suggested: Math.round(basePrice * 100) / 100,
      currency: 'USD',
    },
    confidenceScore: Math.round((0.7 + (seed % 30) / 100) * 100) / 100,
    competitorComparison: [
      { name: 'Competitor A', price: Math.round((basePrice * 1.1) * 100) / 100, advantage: 'price' },
      { name: 'Competitor B', price: Math.round((basePrice * 0.9) * 100) / 100, advantage: 'features' },
      { name: 'Competitor C', price: Math.round((basePrice * 1.2) * 100) / 100, advantage: 'brand' },
    ],
    marketBenchmarks: {
      averagePrice: Math.round(basePrice * 100) / 100,
      pricePoints: [19.99, 29.99, 49.99, 79.99],
      category: 'General',
    },
    metadata: {
      dataPointsUsed: 1250 + (seed * 10),
      modelVersion: 'v2.1.0-dev',
      lastUpdated: new Date().toISOString(),
    },
  };
}

export default { fetchPricingSuggestions, getMockPricingSuggestions };