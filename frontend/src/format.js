// shared formatting helpers, used by the table, the metric cards and the chart


// DPI and TVPI, 2 decimal places with an 'x' after
export function formatRatio(value) {

    // checks for null and undefined value
    if (value == null) {
        return "N/A";
    }

    return Number(value).toFixed(2) + "x";
}


// both IRR's, multiplied by 100 to get a percentage
export function formatPercent(value) {

    if (value == null) {
        return "N/A";
    }

    return (value * 100).toFixed(2) + "%";
}


// color class for IRR values
export function getIrrClass(value) {

    if (value == null) {
        return "";
    }
    if (value > 0) {
        return "positive";
    }
    if (value < 0) {
        return "negative";
    }
    return "";
}


// dollar amounts, compact for chart axes ($450K) or full for tooltips ($450,000)
export function formatCurrency(value, compact = false) {

    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        notation: compact ? "compact" : "standard",
        maximumFractionDigits: compact ? 1 : 0,
    }).format(value);
}


// dates from the API come back as "YYYY-MM-DD"
export function formatDate(value) {

    return new Date(value).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        timeZone: "UTC",
    });
}
