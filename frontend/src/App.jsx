import { useEffect, useState } from 'react'
import { getFundDetail, getFunds } from './api';
import FundTable from './components/FundTable';
import CashFlowChart from './components/CashFlowChart';


function App() {

  const [funds, setFunds] = useState([]);
  const [selectedFundId, setSelectedFundId] = useState(null);
  const [selectedFundDetail, setSelectedFundDetail] = useState(null);

  useEffect(() => {

    async function loadFunds() {
      const data  = await getFunds();
      setFunds(data); 
    }
    loadFunds();

  }, []);

  useEffect(() => {

    if (selectedFundId === null) {
      return;
    }

    async function loadFundDetail() {
      const data = await getFundDetail(selectedFundId);
      setSelectedFundDetail(data);
    }

    loadFundDetail();
  }, [selectedFundId]);


  return (
    <>
    <FundTable funds={funds} onSelectFund={setSelectedFundId} />
    <CashFlowChart fund={selectedFundDetail} />
    </>
  );
}
 

export default App