const AiRpctUi = {
    format(value, fallback = "—") {
        if (value === undefined || value === null || value === "") {
            return fallback;
        }

        return value;
    },

    setText(id, value, fallback = "—") {
        const element = document.getElementById(id);

        if (!element) {
            return;
        }

        element.textContent = this.format(value, fallback);
    },

    setStatus(id, status) {
        const element = document.getElementById(id);

        if (!element) {
            return;
        }

        element.textContent = this.format(status);

        element.classList.remove(
            "status-success",
            "status-warning",
            "status-danger"
        );

        const normalized = String(status || "").toLowerCase();

        if (
            normalized.includes("success") ||
            normalized.includes("available") ||
            normalized.includes("healthy")
        ) {
            element.classList.add("status-success");
            return;
        }

        if (
            normalized.includes("warning") ||
            normalized.includes("watch") ||
            normalized.includes("medium")
        ) {
            element.classList.add("status-warning");
            return;
        }

        if (
            normalized.includes("fail") ||
            normalized.includes("critical") ||
            normalized.includes("high")
        ) {
            element.classList.add("status-danger");
        }
    },
};
