import { useState } from "react";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import RecentBills from "./components/RecentBills";
import "./App.css";

function App() {
  const [bills, setBills] = useState([]);

  function handleBillSaved(newBill) {
    setBills((previousBills) => [
      newBill,
      ...previousBills
    ]);
  }
  return (
    <div className="app-container">

      <Header />

      <main className="main-content">
        <UploadSection onBillSaved={handleBillSaved} />
        <RecentBills bills={bills} />
      </main>

      <footer className="footer">
        Made for smarter everyday spending.
      </footer>

    </div>
  );
}

export default App;