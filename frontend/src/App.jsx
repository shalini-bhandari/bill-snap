import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import RecentBills from "./components/RecentBills";
import "./App.css";

function App() {
  return (
    <div className="app-container">

      <Header />

      <main className="main-content">
        <UploadSection />
        <RecentBills />
      </main>

      <footer className="footer">
        Made for smarter everyday spending.
      </footer>

    </div>
  );
}

export default App;