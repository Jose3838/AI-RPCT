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
    }
};
