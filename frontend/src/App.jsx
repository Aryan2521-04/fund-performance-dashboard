import { useEffect, useState } from 'react'
import { getFunds } from './api';
import FundTable from './components/FundTable';


function App() {

  const [funds, setFunds] = useState([]);

  useEffect(() => {

    async function loadFunds() {
      const data  = await getFunds();
      setFunds(data); 
    }
    loadFunds();

  }, []);


  return (
    <FundTable funds={funds} />

  );
}
 

export default App