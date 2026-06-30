let registryOffset = 0;

function getRegistryLimit() {
    return Number(document.getElementById("registryLimit")?.value || 50);
}

function renderRegistryRows(rows) {
    const body = document.getElementById("registryRows");
    const count = document.getElementById("registryCount");
    const page = document.getElementById("registryPage");

    if (!body) return;

    count.textContent = `${rows.length} results`;
    page.textContent = `Offset ${registryOffset}`;

    body.innerHTML = rows.map((row) => `
        <tr>
            <td>${AiRpctUi.format(row.registry_name)}</td>
            <td>${AiRpctUi.format(row.row_count)}</td>
            <td>${AiRpctUi.format(row.warehouse_group)}</td>
            <td>${AiRpctUi.format(row.status)}</td>
        </tr>
    `).join("");
}

async function loadRegistries() {
    const search = document.getElementById("registrySearch")?.value || "";
    const sort = document.getElementById("registrySort")?.value || "";
    const limit = getRegistryLimit();

    const params = new URLSearchParams();

    if (search) params.set("search", search);
    if (sort) params.set("sort", sort);

    params.set("limit", String(limit));
    params.set("offset", String(registryOffset));

    try {
        const rows = await AiRpctApi.getRegistries(`?${params.toString()}`);
        renderRegistryRows(rows);
        AiRpctUi.setText("registryStatus", "Live registry API connected");
    } catch (error) {
        console.error(error);
        AiRpctUi.setText("registryStatus", "Registry API unavailable");
    }
}

function resetRegistryPagination() {
    registryOffset = 0;
    loadRegistries();
}

document.getElementById("registrySearch")?.addEventListener("input", resetRegistryPagination);
document.getElementById("registrySort")?.addEventListener("change", resetRegistryPagination);
document.getElementById("registryLimit")?.addEventListener("change", resetRegistryPagination);

document.getElementById("registryPrev")?.addEventListener("click", () => {
    registryOffset = Math.max(0, registryOffset - getRegistryLimit());
    loadRegistries();
});

document.getElementById("registryNext")?.addEventListener("click", () => {
    registryOffset += getRegistryLimit();
    loadRegistries();
});

loadRegistries();
