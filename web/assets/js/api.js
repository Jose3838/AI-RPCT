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

    getProviderRankings() {
        return apiGet("/provider-rankings");
    },

    getProviderMarketShare() {
        return apiGet("/provider-marketshare");
    },

    getPipelineHistory() {
        return apiGet("/pipeline-history");
    },

    getRegistries(params = "") {
        return apiGet(`/registries${params}`);
    },

    getRegistry(name, params = "") {
        return apiGet(`/registry/${name}${params}`);
    },

    getRegistryInfo(name) {
        return apiGet(`/registry-info/${name}`);
    }
};
