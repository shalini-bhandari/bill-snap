import { useEffect, useState } from "react";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import RecentBills from "./components/RecentBills";
import { getAllBills, saveBill } from "./db/billDB";
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
          <RecentBills bills={bills} />
        )}

      </main>

      <footer className="footer">
        Made for smarter everyday spending.
      </footer>

    </div>
  );
}

export default App;
