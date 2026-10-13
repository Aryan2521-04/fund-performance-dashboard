import { formatPercent, formatRatio, getIrrClass } from '../format';


export default function FundTable({ funds, selectedFundId, onSelectFund }) {

    // lets keyboard users pick a row with Enter or Space, same as a click
    function handleKeyDown(event, fundId) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            onSelectFund(fundId);
        }
    }

    return (

        <div className="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th> Fund </th>
                        <th className="numeric"> Vintage </th>
                        <th className="numeric"> DPI </th>
                        <th className="numeric"> TVPI </th>
                        <th className="numeric"> IRR (Realized) </th>
                        <th className="numeric"> IRR (Since Inception) </th>
                    </tr>
                </thead>
                <tbody>
                    {funds.map((fund) => (
                        <tr
                            key={fund.id}
                            className={fund.id === selectedFundId ? "selected" : ""}
                            tabIndex={0}
                            aria-selected={fund.id === selectedFundId}
                            onClick={() => onSelectFund(fund.id)}
                            onKeyDown={(event) => handleKeyDown(event, fund.id)}
                        >
                            <td className="fund-name"> {fund.name} </td>
                            <td className="numeric"> {fund.vintage_year} </td>
                            <td className="numeric"> {formatRatio(fund.dpi)} </td>
                            <td className="numeric"> {formatRatio(fund.tvpi)} </td>
                            <td className={`numeric ${getIrrClass(fund.irr_realized)}`}> {formatPercent(fund.irr_realized)} </td>
                            <td className={`numeric ${getIrrClass(fund.irr_since_inception)}`}> {formatPercent(fund.irr_since_inception)} </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )

}
