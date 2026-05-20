class AxentxSDK {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseURL = "https://api.axentx.com";
    }

    async addRag(ragData) {
        const headers = {
            "Authorization": `Bearer ${this.apiKey}`,
            "Content-Type": "application/json"
        };
        const response = await fetch(`${this.baseURL}/rag`, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(ragData)
        });
        return await response.json();
    }

    async getRag(ragId) {
        const headers = {
            "Authorization": `Bearer ${this.apiKey}`,
            "Content-Type": "application/json"
        };
        const response = await fetch(`${this.baseURL}/rag/${ragId}`, {
            method: "GET",
            headers: headers
        });
        return await response.json();
    }
}