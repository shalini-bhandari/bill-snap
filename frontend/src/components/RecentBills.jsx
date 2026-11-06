import { useEffect, useState } from "react";

function RecentBills({ bills = [], onBillDeleted }) {
  const [selectedBill, setSelectedBill] = useState(null);
  const [receiptUrl, setReceiptUrl] = useState(null);

  useEffect(() => {
    if (!selectedBill?.image) {
      setReceiptUrl(null);
      return;
    }

    const url = URL.createObjectURL(selectedBill.image);
    setReceiptUrl(url);

    return () => URL.revokeObjectURL(url);
  }, [selectedBill]);

  async function handleDelete(bill) {
    const confirmed = window.confirm(
      `Are you sure you want to delete the bill from ${bill.merchant_name}?`
    );

    if (!confirmed) return;

    await onBillDeleted(bill.id);

    if (selectedBill?.id === bill.id) {
      setSelectedBill(null);
    }
  }

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

                <div className="bill-metadata">
                  <span>{bill.bill_date || "Date unavailable"}</span>
                  <span className="category-tag">
                    {bill.category}
                  </span>
                </div>
              </div>

              <div className="bill-item-right">
                <strong className="bill-item-amount">
                  ₹{Number(bill.total_amount).toFixed(2)}
                </strong>

                <div className="bill-actions">
                  <button
                    className="view-bill-button"
                    onClick={() => setSelectedBill(bill)}
                  >
                    View receipt
                  </button>

                  <button
                    className="delete-bill-button"
                    onClick={() => handleDelete(bill)}
                    aria-label={`Delete bill from ${bill.merchant_name}`}
                  >
                    Delete
                  </button>
                </div>
              </div>

            </article>
          ))}
        </div>
      )}

      {/* Receipt image modal */}
      {selectedBill && (
        <div
          className="receipt-modal-overlay"
          onClick={() => setSelectedBill(null)}
        >
          <div
            className="receipt-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="receipt-modal-heading">
              <div>
                <h3>{selectedBill.merchant_name}</h3>
                <p>Original receipt</p>
              </div>

              <button
                className="modal-close-button"
                onClick={() => setSelectedBill(null)}
                aria-label="Close receipt"
              >
                ×
              </button>
            </div>

            {receiptUrl ? (
              <img
                src={receiptUrl}
                alt={`Receipt from ${selectedBill.merchant_name}`}
                className="receipt-modal-image"
              />
            ) : (
              <p className="receipt-unavailable">
                Original receipt image is unavailable.
              </p>
            )}
          </div>
        </div>
      )}

    </section>
  );
}

export default RecentBills;
