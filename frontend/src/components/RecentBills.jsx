
function RecentBills({ bills = [] }) {
  return (
    <section className="recent-section">

      <div className="recent-heading">
        <div>
          <p className="eyebrow">YOUR COLLECTION</p>
          <h2>Recent bills</h2>
        </div>

        <span className="bill-count">
          {bills.length} {bills.length === 1 ? "bill" : "bills"}
        </span>
      </div>

      {bills.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">▤</div>

          <h3>No bills yet</h3>

          <p>
            Your saved receipts will appear here.
            Start by scanning your first bill!
          </p>
        </div>
      ) : (
        <div className="bills-list">
          {bills.map((bill) => (
            <article className="bill-item" key={bill.id}>

              <div className="bill-item-icon">▤</div>

              <div className="bill-item-details">
                <h3>{bill.merchant_name}</h3>

                <p>
                  {bill.bill_date || "Date unavailable"}
                  {" · "}
                  {bill.category}
                </p>
              </div>

              <div className="bill-item-amount">
                ₹{Number(bill.total_amount).toFixed(2)}
              </div>

            </article>
          ))}
        </div>
      )}

    </section>
  );
}

export default RecentBills;
