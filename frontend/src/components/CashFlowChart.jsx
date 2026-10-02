import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function computeCumulativeCashFlow(cash_flows) {

    // sorts the cash_flow array

    const sorted = cash_flows.sort((a, b) => {

        const a_date = new Date(a.date);
        const b_date = new Date(b.date);
        const date_diff = a_date - b_date;
        return date_diff;
});

    let runningTotal = 0;
    const cumulativeData = sorted.map((cf) => {

        let cf_value = Number(cf.amount);
        runningTotal += cf_value;
        return {
            date: cf.date,
            cumulative: runningTotal
        };
});

return cumulativeData;

}

export default function CashFlowChart({ fund }) {


    if (fund === null) {
        return ("Select a fund to see its cash flow history");
    }

    const result = computeCumulativeCashFlow(fund.cash_flows);

    return (


        <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={result}>
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Line type="monotone" dataKey="cumulative" stroke="var(--accent)" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )

}