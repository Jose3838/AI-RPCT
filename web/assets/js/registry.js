let registryOffset = 0;

const initialRegistrySearch =
    new URLSearchParams(window.location.search).get("search") || "";

function getRegistryLimit() {
    return Number(document.getElementById("registryLimit")?.value || 50);
}

function getRegistrySearch() {
    return initialRegistrySearch;
}

function renderRegistryRows(rows) {
    const body = document.getElementById("registryRows");

    AiRpctUi.setText("registryCount", `${rows.length} results`);
    AiRpctUi.setText("registryPage", `Offset ${registryOffset}`);

    body.innerHTML = rows.map((row) => `
        <tr class="clickable-row" data-registry="${row.registry_name}">
            <td>${AiRpctUi.format(row.registry_name)}</td>
            <td>${AiRpctUi.format(row.row_count)}</td>
            <td>${AiRpctUi.format(row.warehouse_group)}</td>
            <td>${AiRpctUi.format(row.status)}</td>
        </tr>
    `).join("");

    document.querySelectorAll("[data-registry]").forEach((row) => {
        row.addEventListener("click", () => loadRegistryPreview(row.dataset.registry));
    });
}

function renderRegistryPreview(name, rows, info) {
    const columns = info.column_names || [];

    AiRpctUi.setText("registryInfoName", info.registry_name);
    AiRpctUi.setText("registryInfoRows", info.rows);
    AiRpctUi.setText("registryInfoColumns", info.columns);
    AiRpctUi.setText("registryInfoStatus", info.status);

    const fields = document.getElementById("registryInfoFields");
    if (fields) {
        fields.innerHTML =
            columns.map((column) => `<span class="schema-pill">${column}</span>`).join("");
    }

    AiRpctUi.setText("registryPreviewTitle", name);
    AiRpctUi.setText(
        "registryPreviewMeta",
        `${rows.length} preview rows · ${columns.length} columns`
    );

    const previewRows = document.getElementById("registryPreviewRows");
    if (previewRows) {
        previewRows.innerHTML = rows.map((row) => `
            <tr>
                <td>
                    ${columns.map((column) =>
                        `<strong>${column}</strong>: ${AiRpctUi.format(row[column])}`
                    ).join("<br>")}
                </td>
            </tr>
        `).join("");
    }
}

async function loadRegistryPreview(name) {
    const [rows, info] = await Promise.all([
        AiRpctApi.getRegistry(name, "?limit=10"),
        AiRpctApi.getRegistryInfo(name),
    ]);

    renderRegistryPreview(name, rows, info);
}

async function loadRegistries() {
    const params = new URLSearchParams();
    const search = getRegistrySearch();
    const sort = document.getElementById("registrySort")?.value || "";
    const limit = getRegistryLimit();

    if (search) params.set("search", search);
    if (sort) params.set("sort", sort);

    params.set("limit", String(limit));
    params.set("offset", String(registryOffset));

    const rows = await AiRpctApi.getRegistries(`?${params.toString()}`);

    renderRegistryRows(rows);
    AiRpctUi.setText("registryStatus", "Live registry API connected");

    if (rows.length) {
        await loadRegistryPreview(rows[0].registry_name);
    }
}

function resetRegistryPagination() {
    registryOffset = 0;
    loadRegistries();
}

document.addEventListener("DOMContentLoaded", () => {

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
});
