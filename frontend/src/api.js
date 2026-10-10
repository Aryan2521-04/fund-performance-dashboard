
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
// getFunds()

export async function getFunds() {

    try {
        const response = await fetch(`${API_BASE_URL}/funds`);

        if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`);
        }
    

    const data = await response.json();
    return data;

    } catch (error) {
        console.log(`Fetch error:`, error);
        throw error;
    }

}



// getFundDetail(fundId)

export async function getFundDetail(fundId) {
    
    try {
        const response = await fetch(`${API_BASE_URL}/funds/${fundId}`);

        if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`);
        }
    

    const data = await response.json();
    return data;

    } catch (error) {
        console.log(`Fetch error:`, error);
        throw error;
    }

}


// createCashFlow(fundId, cashFlowData)

export async function createCashFlow(fundId, cashFlowData) {

    const options = {
        method: "POST",
        headers: {"Content-Type": "application/json" }, 
        body: JSON.stringify(cashFlowData)
    }


     try {
        const response = await fetch(`${API_BASE_URL}/funds/${fundId}/cashflows`, options);

        if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`);
        }
    

    const data = await response.json();
    return data;

    } catch (error) {
        console.log(`Fetch error:`, error);
        throw error;
    }
    
}