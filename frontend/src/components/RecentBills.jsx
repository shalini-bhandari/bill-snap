function RecentBills() {
  return (
    <section className="recent-section">

      <div className="recent-heading">
        <div>
          <p className="eyebrow">YOUR COLLECTION</p>
          <h2>Recent bills</h2>
        </div>

        <span className="bill-count">0 bills</span>
      </div>

      <div className="empty-state">
        <div className="empty-icon">▤</div>

        <h3>No bills yet</h3>

        <p>
          Your saved receipts will appear here.
          Start by scanning your first bill!
        </p>
      </div>

    </section>
  );
}

export default RecentBills;