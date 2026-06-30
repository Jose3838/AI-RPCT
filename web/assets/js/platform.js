function injectPlatformTopbar() {
    const content = document.querySelector(".content");

    if (!content) {
        return;
    }

    const topbar = document.createElement("section");
    topbar.className = "platform-topbar";

    topbar.innerHTML = `
        <div>
            <strong>AI-RPCT Platform</strong>
            <p>Governed AI Infrastructure Intelligence</p>
        </div>

        <div class="platform-actions">
            <input
                id="platformSearch"
                class="platform-search"
                type="search"
                placeholder="Search platform..."
            >
            <span class="platform-status">Pipeline Healthy</span>
        </div>
    `;

    content.prepend(topbar);

    document.getElementById("platformSearch").addEventListener("keydown", (event) => {
        if (event.key !== "Enter") {
            return;
        }

        const query = event.target.value.trim();

        if (!query) {
            return;
        }

        window.location.href = `/web/pages/registry.html?search=${encodeURIComponent(query)}`;
    });
}

injectPlatformTopbar();
