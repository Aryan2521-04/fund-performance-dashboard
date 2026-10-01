

// helper function for DPI, and TVPI calculations 
function formatRatio(value) {

    // checks for null and undefinded value
    if (value == null) {
        return ("N/A");
    }


    // returns to 2 decimal place with an 'x' after
    const fixed = Number(value).toFixed(2);

    return (fixed + 'x');

}


// helper function for both IRR's
function formatPercent(value) {

    // checks for null and undefinded value
    if (value == null) {
        return ("N/A");
    }

    // multiples by 100 to get a percentage, then fixes it to 2 decimal places
    const percentValue = value * 100;
    const fixed = percentValue.toFixed(2);

    return (fixed + '%');

}


export default function FundTable({ funds, onSelectFund}) {

    return (

        <table>
            <thead>
                <tr>
                    <th> Name </th>
                    <th> Vintage Year </th> 
                    <th> DPI </th>
                    <th> TVPI </th>
                    <th> IRR (Realized) </th>
                    <th> IRR (Since inception) </th>
                </tr>
            </thead>
            <tbody>
                {funds.map((fund) => (
                    <tr key={fund.id} onClick={() => onSelectFund(fund.id)}>
                        <td> {fund.name} </td>
                        <td> {fund.vintage_year} </td>
                        <td> {formatRatio(fund.dpi)} </td>
                        <td> {formatRatio(fund.tvpi)} </td>
                        <td> {formatPercent(fund.irr_realized)} </td>
                        <td> {formatPercent(fund.irr_since_inception)} </td>
                    </tr>
                ))}
            </tbody>
        </table>
    )
    
}