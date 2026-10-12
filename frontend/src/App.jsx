import { useEffect, useState } from 'react'
import { getFundDetail, getFunds } from './api';
import FundTable from './components/FundTable';
import CashFlowChart from './components/CashFlowChart';


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

  if (error) {
    return <p>Page has an error, {error}</p>
  }

  if (loading) {
    return <p>Page is loading . . .</p>
  }


  return (
    <>
    <FundTable funds={funds} onSelectFund={setSelectedFundId} />
    {detailError ? <p>{detailError}</p> : <CashFlowChart fund={selectedFundDetail}/>}
    </>
  );
}
 

export default App