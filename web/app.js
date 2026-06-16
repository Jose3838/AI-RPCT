async function loadMetrics() {
    const response =
        await fetch(
            "http://127.0.0.1:8000/metrics"
        );

    const data =
        await response.json();

    console.log(data);
}

loadMetrics();

setInterval(
    loadMetrics,
    30000
);
