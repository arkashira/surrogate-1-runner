const axios = require('axios');
const fs = require('fs');
const path = require('path');

const priceComparisonApiUrl = 'https://price-comparison-api.example.com';
const retailersFilePath = path.join(__dirname, '..', 'data', 'retailers.json');

class PriceComparison {
    constructor() {
        this.retailers = this._loadRetailers();
    }

    _loadRetailers() {
        try {
            const rawData = fs.readFileSync(retailersFilePath);
            return JSON.parse(rawData).retailers;
        } catch (error) {
            console.error('Error loading retailers:', error);
            throw new Error('Failed to load retailers data');
        }
    }

    async getPriceComparison(productId, category = null) {
        const results = [];

        for (const retailer of this.retailers) {
            if (category && !retailer.categories.includes(category)) {
                continue;
            }

            try {
                const response = await axios.get(`${retailer.url}/products/${productId}`);
                results.push({
                    retailerId: retailer.id,
                    retailerName: retailer.name,
                    price: response.data.price,
                    currency: retailer.currency,
                    rating: retailer.rating,
                    delivery: retailer.delivery,
                    url: retailer.url,
                    available: true,
                    productId: productId
                });
            } catch (error) {
                console.error(`Error fetching price from ${retailer.name}:`, error);
            }
        }

        results.sort((a, b) => a.price - b.price);

        return {
            productId: productId,
            category: category,
            retailers: results,
            bestPrice: results.length > 0 ? results[0].price : null,
            bestRetailer: results.length > 0 ? results[0].retailerName : null
        };
    }

    getRetailerById(retailerId) {
        return this.retailers.find(retailer => retailer.id === retailerId);
    }

    getCategories() {
        const categories = new Set();
        this.retailers.forEach(retailer => retailer.categories.forEach(category => categories.add(category)));
        return Array.from(categories);
    }
}

module.exports = PriceComparison;