import { CartesianGrid, Legend, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { formatCurrency, formatDate } from '../format';


// builds one row per date with the running net cash flow and/or the NAV on that date,
// keyed by timestamp so the X axis spaces points by actual date
function buildChartData(cash_flows, nav_snapshots) {

    const rows = new Map();

    function rowFor(date) {
        const time = new Date(date).getTime();
        if (!rows.has(time)) {
            rows.set(time, { time });
        }
        return rows.get(time);
    }

    // sorts a copy so props/state aren't mutated
    const sorted = cash_flows.toSorted((a, b) => new Date(a.date) - new Date(b.date));

    let runningTotal = 0;
    for (const cf of sorted) {
        runningTotal += Number(cf.amount);
        rowFor(cf.date).cumulative = runningTotal;
    }

    for (const ns of nav_snapshots) {
        rowFor(ns.date).nav = Number(ns.value);
    }

    return [...rows.values()].sort((a, b) => a.time - b.time);
}


// one tick on Jan 1 of each year the data covers, so years don't repeat on the axis
function yearTicks(data) {

    const first = new Date(data[0].time).getUTCFullYear();
    const last = new Date(data[data.length - 1].time).getUTCFullYear();

    const ticks = [];
    for (let year = first; year <= last + 1; year++) {
        ticks.push(Date.UTC(year, 0, 1));
    }
    return ticks;
}


export default function CashFlowChart({ fund }) {

    const data = buildChartData(fund.cash_flows, fund.nav_snapshots);

    if (data.length === 0) {
        return <p className="status">No cash flows recorded for this fund yet</p>;
    }

    const ticks = yearTicks(data);

    return (

        <div className="chart-container">
            <ResponsiveContainer width="100%" height={320}>
                <LineChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 8 }}>
                    <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" vertical={false} />
                    <XAxis
                        dataKey="time"
                        type="number"
                        scale="time"
                        domain={[ticks[0], ticks[ticks.length - 1]]}
                        ticks={ticks}
                        tickFormatter={(time) => new Date(time).getUTCFullYear()}
                        stroke="var(--text-muted)"
                        tick={{ fontSize: 12 }}
                    />
                    <YAxis
                        tickFormatter={(value) => formatCurrency(value, true)}
                        stroke="var(--text-muted)"
                        tick={{ fontSize: 12 }}
                        width={64}
                    />
                    <ReferenceLine y={0} stroke="var(--text-muted)" />
                    <Tooltip
                        labelFormatter={(time) => formatDate(time)}
                        formatter={(value) => formatCurrency(value)}
                        contentStyle={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 8 }}
                    />
                    <Legend wrapperStyle={{ fontSize: 13 }} />
                    {/* cumulative cash flow only changes on cash flow dates, so it's drawn as steps */}
                    <Line
                        name="Cumulative net cash flow"
                        dataKey="cumulative"
                        type="stepAfter"
                        stroke="var(--accent)"
                        strokeWidth={2}
                        dot={{ r: 3 }}
                        connectNulls
                        isAnimationActive={false}
                    />
                    <Line
                        name="NAV"
                        dataKey="nav"
                        type="monotone"
                        stroke="var(--accent-2)"
                        strokeWidth={2}
                        strokeDasharray="5 4"
                        dot={{ r: 3 }}
                        connectNulls
                        isAnimationActive={false}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )

}
