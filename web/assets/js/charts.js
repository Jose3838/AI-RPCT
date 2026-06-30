const AiRpctCharts = {
    renderBar(containerId, items, options = {}) {
        const container = document.getElementById(containerId);

        if (!container) {
            return;
        }

        if (!items || items.length === 0) {
            container.innerHTML = "<p>No chart data available.</p>";
            return;
        }

        const labelKey = options.labelKey || "label";
        const valueKey = options.valueKey || "value";
        const showValue = options.showValue !== false;

        const maxValue = Math.max(
            ...items.map((item) => Number(item[valueKey] || 0)),
            1
        );

        container.innerHTML = items.map((item) => {
            const label = item[labelKey] || "Unknown";
            const value = Number(item[valueKey] || 0);
            const width = Math.round((value / maxValue) * 100);

            return `
                <div class="chart-row">
                    <div class="chart-row-head">
                        <span>${label}</span>
                        ${showValue ? `<strong>${value}</strong>` : ""}
                    </div>
                    <div class="chart-track">
                        <div class="chart-fill" style="width:${width}%"></div>
                    </div>
                </div>
            `;
        }).join("");
    },

    renderDonut(containerId, items, options = {}) {
        const container = document.getElementById(containerId);

        if (!container) {
            return;
        }

        if (!items || items.length === 0) {
            container.innerHTML = "<p>No chart data available.</p>";
            return;
        }

        const labelKey = options.labelKey || "label";
        const valueKey = options.valueKey || "value";

        const topItems = items.slice(0, 6).map((item) => ({
            label: item[labelKey] || "Unknown",
            value: Number(item[valueKey] || 0),
        }));

        const total = topItems.reduce((sum, item) => sum + item.value, 0) || 1;

        let offset = 0;

        const segments = topItems.map((item, index) => {
            const percentage = (item.value / total) * 100;
            const start = offset;
            const end = offset + percentage;
            offset = end;

            return `var(--chart-${index + 1}) ${start}% ${end}%`;
        }).join(", ");

        const legend = topItems.map((item, index) => {
            return `
                <div class="donut-legend-item">
                    <span class="donut-dot chart-${index + 1}"></span>
                    <strong>${item.label}</strong>
                    <em>${item.value.toFixed(2)}%</em>
                </div>
            `;
        }).join("");

        container.innerHTML = `
            <div class="donut-layout">
                <div class="donut-chart" style="background: conic-gradient(${segments});">
                    <div class="donut-center">
                        <strong>${topItems.length}</strong>
                        <span>providers</span>
                    </div>
                </div>
                <div class="donut-legend">
                    ${legend}
                </div>
            </div>
        `;
    },

    renderPipelineHealth(containerId, health) {
        const container = document.getElementById(containerId);

        if (!container) {
            return;
        }

        const value = Number(health || 0);

        container.innerHTML = `
            <div class="health-ring">
                <div class="health-value">${value}%</div>
            </div>
        `;
    },

    renderConfidenceTrend(containerId, points) {
        const container = document.getElementById(containerId);

        if (!container) {
            return;
        }

        if (!points || points.length === 0) {
            container.innerHTML = "<p>No confidence trend available.</p>";
            return;
        }

        const values = points.map((point) => Number(point.confidence));

        const max = Math.max(...values);
        const min = Math.min(...values);
        const range = Math.max(max - min, 0.001);

        const coords = values.map((value, index) => {
            const x = (index / Math.max(values.length - 1, 1)) * 100;
            const y = 100 - (((value - min) / range) * 100);

            return `${x},${y}`;
        }).join(" ");

        container.innerHTML = `
            <svg
                viewBox="0 0 100 100"
                preserveAspectRatio="none"
                style="width:100%; height:180px;"
            >
                <polyline
                    fill="none"
                    stroke="var(--accent)"
                    stroke-width="2"
                    points="${coords}"
                />
            </svg>
        `;
    },
};
