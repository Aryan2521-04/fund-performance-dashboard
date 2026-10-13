import { useEffect, useState } from 'react'
import { getFundDetail, getFunds } from './api';
import FundTable from './components/FundTable';
import CashFlowChart from './components/CashFlowChart';
import { formatPercent, formatRatio, getIrrClass } from './format';


function App() {

  const [funds, setFunds] = useState([]);
  const [selectedFundId, setSelectedFundId] = useState(null);
  const [selectedFundDetail, setSelectedFundDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [detailError, setDetailError] = useState(null);

  useEffect(() => {

    async function loadFunds() {
      try {
        const data  = await getFunds();
        setFunds(data);
        // opens the first fund so the page isn't empty on load
        if (data.length > 0) {
          setSelectedFundId(data[0].id);
        }
      }
      catch (err) {
        setError(`Page failed to load: ${err.message}`);

      }
      finally {
        setLoading(false);
      }
    }
    loadFunds();

  }, []);

  useEffect(() => {

    if (selectedFundId === null) {
      return;
    }

    let ignore = false;

    async function loadFundDetail() {
      try {
        setDetailError(null);
        const data = await getFundDetail(selectedFundId);
        if (!ignore) {
          setSelectedFundDetail(data);
        }
      }
      catch (err) {
        if (!ignore) {
          setDetailError(`Error: ${err.message}`);
        }
      }
    }

    loadFundDetail();
    return () => {ignore = true};
  },[selectedFundId]);


  return (
    <>
    <header className="app-header">
      <div className="brand">
        <img src="/favicon.svg" alt="" width="36" height="36" />
        <div>
          <h1>HarborVest</h1>
          <p>Private fund performance from dated cash flows: IRR, TVPI and DPI</p>
        </div>
      </div>
    </header>

    <main>
      {error && <p className="status error">{error}</p>}
      {!error && loading && <p className="status">Loading funds…</p>}

      {!error && !loading && (
        <>
        <section className="panel">
          <h2>Funds</h2>
          <FundTable funds={funds} selectedFundId={selectedFundId} onSelectFund={setSelectedFundId} />
        </section>

        <section className="panel">
          {detailError && <p className="status error">{detailError}</p>}
          {!detailError && !selectedFundDetail && <p className="status">Select a fund to see its cash flow history</p>}
          {!detailError && selectedFundDetail && <FundDetail fund={selectedFundDetail} />}
        </section>

        <MetricGlossary />
        </>
      )}
    </main>
    </>
  );
}


function FundDetail({ fund }) {

  const metrics = [
    { label: "DPI", value: formatRatio(fund.dpi) },
    { label: "TVPI", value: formatRatio(fund.tvpi) },
    { label: "IRR (Realized)", value: formatPercent(fund.irr_realized), className: getIrrClass(fund.irr_realized) },
    { label: "IRR (Since Inception)", value: formatPercent(fund.irr_since_inception), className: getIrrClass(fund.irr_since_inception) },
  ];

  return (
    <>
    <div className="detail-header">
      <h2>{fund.name}</h2>
      <span className="pill">Vintage {fund.vintage_year}</span>
    </div>

    <div className="metric-grid">
      {metrics.map((metric) => (
        <div className="metric-card" key={metric.label}>
          <span className="metric-label">{metric.label}</span>
          <span className={`metric-value ${metric.className ?? ""}`}>{metric.value}</span>
        </div>
      ))}
    </div>

    <h3>Cash flows vs. NAV</h3>
    <CashFlowChart fund={fund} />
    </>
  );
}


function MetricGlossary() {

  return (
    <section className="glossary">
      <div>
        <h3>DPI</h3>
        <p>Distributions ÷ paid-in capital. How much cash has actually been returned to investors.</p>
      </div>
      <div>
        <h3>TVPI</h3>
        <p>(Distributions + NAV) ÷ paid-in capital. Total value created, realized or not.</p>
      </div>
      <div>
        <h3>IRR (Realized)</h3>
        <p>Annualized return using only actual cash flows and their real dates.</p>
      </div>
      <div>
        <h3>IRR (Since Inception)</h3>
        <p>Same as above, but the latest NAV is treated as a final cash flow on its valuation date.</p>
      </div>
    </section>
  );
}


export default App
