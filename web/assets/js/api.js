const API_BASE = "http://127.0.0.1:8000";

async function apiGet(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`);

    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
}

const AiRpctApi = {
    getDashboard() {
        return apiGet("/dashboard");
    },

    getExecutiveDashboard() {
        return apiGet("/dashboard/executive");
    },

    getIntelligenceHub() {
        return apiGet("/copilot/intelligence-hub");
    },

    getPipelineHealth() {
        return apiGet("/pipeline-health");
    },

    getPipelineHistory() {
        return apiGet("/pipeline-history");
    },

    getProviderRankings() {
        return apiGet("/provider-rankings");
    },

    getProviderMarketShare() {
        return apiGet("/provider-marketshare");
    },

    getRegistries(params = "") {
        return apiGet(`/registries${params}`);
    }
};
