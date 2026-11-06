import { useEffect, useState } from "react";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import RecentBills from "./components/RecentBills";
import { getAllBills, saveBill, deleteBill } from "./db/billDB";
import "./App.css";

function App() {
  const [bills, setBills] = useState([]);
  const [loadingBills, setLoadingBills] = useState(true);
  const [storageError, setStorageError] = useState("");

  // Load previously saved bills when the app starts
  useEffect(() => {
    async function loadBills() {
      try {
        const savedBills = await getAllBills();
        setBills(savedBills);
      } catch (error) {
        console.error("Unable to load saved bills:", error);
        setStorageError("Unable to load your saved bills.");
      } finally {
        setLoadingBills(false);
      }
    }

    loadBills();
  }, []);

  // Save a new bill to IndexedDB
  async function handleBillSaved(newBill) {
    try {
      await saveBill(newBill);

      setBills((previousBills) => [
        newBill,
        ...previousBills
      ]);

      setStorageError("");
    } catch (error) {
      console.error("Unable to save bill:", error);
      throw new Error("Could not save this bill on your device.");
    }
  }

  async function handleBillDeleted(billId) {
    try {
      await deleteBill(billId);

      setBills((previousBills) =>
        previousBills.filter((bill) => bill.id !== billId)
      );

      setStorageError("");
    } catch (error) {
      console.error("Unable to delete bill:", error);
      setStorageError("Unable to delete this bill. Please try again.");
    }
  }

  return (
    <div className="app-container">

      <Header />

      <main className="main-content">

        <UploadSection onBillSaved={handleBillSaved} />

        {storageError && (
          <p className="error-message" role="alert">
            {storageError}
          </p>
        )}

        {loadingBills ? (
          <p>Loading your saved bills...</p>
        ) : (
          <RecentBills 
            bills={bills}
            onBillDeleted={handleBillDeleted} 
          />
        )}

      </main>

      <footer className="footer">
        Made for smarter everyday spending.
      </footer>

    </div>
  );
}

export default App;
