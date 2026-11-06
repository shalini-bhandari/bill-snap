
import { useEffect, useRef, useState } from "react";

const API_URL = "http://127.0.0.1:8000/api/bills/analyze";

function UploadSection({ onBillSaved }) {
  const galleryInput = useRef(null);
  const cameraInput = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");

  // Create and clean up the temporary preview URL
  useEffect(() => {
    if (!selectedFile) {
      setPreview(null);
      return;
    }

    const imageUrl = URL.createObjectURL(selectedFile);
    setPreview(imageUrl);

    return () => URL.revokeObjectURL(imageUrl);
  }, [selectedFile]);

  // Handle image selection
  function handleImageChange(event) {
    const file = event.target.files?.[0];

    if (!file) return;

    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/webp"
    ];

    if (!allowedTypes.includes(file.type)) {
      setError("Please select a JPEG, PNG, or WebP image.");
      event.target.value = "";
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("Image size must be less than 10 MB.");
      event.target.value = "";
      return;
    }

    setSelectedFile(file);
    setAnalysis(null);
    setError("");
  }

  // Send image to FastAPI and analyze using Gemini
  async function handleAnalyze() {
    if (!selectedFile) return;

    setAnalyzing(true);
    setError("");
    setAnalysis(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to analyze the image."
        );
      }

      // Keep editable form values as strings
      setAnalysis({
        ...data,
        merchant_name: data.merchant_name ?? "",
        bill_date: data.bill_date ?? "",
        total_amount:
          data.total_amount == null
            ? ""
            : String(data.total_amount),
        category: data.category ?? ""
      });

    } catch (err) {
      console.error("Bill analysis error:", err);

      setError(
        err.message === "Failed to fetch"
          ? "Cannot connect to Bill Snap server. Please check that the backend is running."
          : err.message
      );

    } finally {
      setAnalyzing(false);
    }
  }

  // Update an individual extracted field
  function handleFieldChange(field, value) {
    setAnalysis((previous) => ({
      ...previous,
      [field]: value
    }));
  }

  // Save the reviewed bill
  function handleSaveBill() {
    if (!analysis) return;

    if (
      !analysis.merchant_name.trim() ||
      !analysis.total_amount.trim() ||
      !analysis.category
    ) {
      setError(
        "Please enter the merchant, total amount, and category before saving."
      );
      return;
    }

    const amount = Number(analysis.total_amount);

    if (!Number.isFinite(amount) || amount < 0) {
      setError("Please enter a valid total amount.");
      return;
    }

    const newBill = {
      id: crypto.randomUUID(),
      merchant_name: analysis.merchant_name.trim(),
      bill_date: analysis.bill_date || null,
      total_amount: amount,
      category: analysis.category,
      created_at: new Date().toISOString()
    };

    onBillSaved(newBill);

    removeImage();
  }

  // Remove the selected image and reset the form
  function removeImage() {
    setSelectedFile(null);
    setAnalysis(null);
    setError("");
    setAnalyzing(false);

    if (galleryInput.current) {
      galleryInput.current.value = "";
    }

    if (cameraInput.current) {
      cameraInput.current.value = "";
    }
  }

  // Display a warning for low-confidence fields
  function confidenceMessage(field) {
    const score = analysis?.confidence?.[field];

    if (typeof score !== "number") return null;

    if (score < 0.8) {
      return "Please review this field — AI is uncertain.";
    }

    return null;
  }

  return (
    <section className="upload-section">

      <div className="section-heading">
        <div>
          <p className="eyebrow">GET STARTED</p>
          <h1>Every bill, <span>one place.</span></h1>
          <p className="section-description">
            Snap a receipt and let AI do the paperwork.
          </p>
        </div>
      </div>

      <div className="upload-card">

        {!selectedFile ? (
          <>
            <div className="upload-illustration">
              <span>▤</span>
              <div className="scan-line"></div>
            </div>

            <h2>Scan your first bill</h2>

            <p className="upload-description">
              Take a photo or upload an existing receipt.
              We'll extract the details for you.
            </p>

            <div className="upload-actions">
              <button
                className="primary-button"
                onClick={() => cameraInput.current?.click()}
              >
                Take a photo
              </button>

              <button
                className="secondary-button"
                onClick={() => galleryInput.current?.click()}
              >
                Choose from gallery
              </button>
            </div>

            <p className="upload-note">
              JPG, PNG or WebP · Maximum 10 MB
            </p>
          </>
        ) : (
          <div className="preview-container">

            <img
              src={preview}
              alt="Selected bill preview"
              className="image-preview"
            />

            <h2>Image selected!</h2>

            <p className="upload-description">
              {selectedFile.name}
            </p>

            {!analysis && (
              <div className="upload-actions">
                <button
                  className="primary-button"
                  onClick={handleAnalyze}
                  disabled={analyzing}
                >
                  {analyzing ? "Analyzing..." : "Analyze bill"}
                </button>

                <button
                  className="secondary-button"
                  onClick={removeImage}
                  disabled={analyzing}
                >
                  Remove image
                </button>
              </div>
            )}

            {analyzing && (
              <p className="upload-note">
                Gemini is examining your image. This may take a few seconds.
              </p>
            )}

            {error && (
              <p className="error-message" role="alert">
                {error}
              </p>
            )}

            {analysis && !analysis.is_bill && (
              <div className="analysis-result">
                <h2>This doesn't look like a bill</h2>

                <p className="upload-description">
                  Please upload a receipt, invoice, or utility bill.
                </p>

                <button
                  className="primary-button"
                  onClick={removeImage}
                >
                  Choose another image
                </button>
              </div>
            )}

            {analysis && analysis.is_bill && (
              <div className="analysis-result">

                <h2>Bill detected!</h2>

                <p className="upload-description">
                  Review the extracted details before saving.
                </p>

                <div className="bill-review-form">

                  <label>
                    Merchant name
                    <input
                      type="text"
                      value={analysis.merchant_name}
                      onChange={(event) =>
                        handleFieldChange(
                          "merchant_name",
                          event.target.value
                        )
                      }
                    />
                    {confidenceMessage("merchant_name") && (
                      <small className="field-warning">
                        {confidenceMessage("merchant_name")}
                      </small>
                    )}
                  </label>

                  <label>
                    Bill date
                    <input
                      type="date"
                      value={analysis.bill_date}
                      onChange={(event) =>
                        handleFieldChange(
                          "bill_date",
                          event.target.value
                        )
                      }
                    />
                    {confidenceMessage("bill_date") && (
                      <small className="field-warning">
                        {confidenceMessage("bill_date")}
                      </small>
                    )}
                  </label>

                  <label>
                    Total amount (₹)
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={analysis.total_amount}
                      onChange={(event) =>
                        handleFieldChange(
                          "total_amount",
                          event.target.value
                        )
                      }
                    />
                    {confidenceMessage("total_amount") && (
                      <small className="field-warning">
                        {confidenceMessage("total_amount")}
                      </small>
                    )}
                  </label>

                  <label>
                    Category
                    <select
                      value={analysis.category}
                      onChange={(event) =>
                        handleFieldChange(
                          "category",
                          event.target.value
                        )
                      }
                    >
                      <option value="">Select category</option>
                      <option value="Food">Food</option>
                      <option value="Utilities">Utilities</option>
                      <option value="Groceries">Groceries</option>
                    </select>
                    {confidenceMessage("category") && (
                      <small className="field-warning">
                        {confidenceMessage("category")}
                      </small>
                    )}
                  </label>

                </div>

                <div className="upload-actions">
                  <button
                    className="primary-button"
                    onClick={handleSaveBill}
                  >
                    Save bill
                  </button>

                  <button
                    className="secondary-button"
                    onClick={removeImage}
                  >
                    Discard
                  </button>
                </div>

                {error && (
                  <p className="error-message" role="alert">
                    {error}
                  </p>
                )}

                <p className="upload-note">
                  Please verify the details before saving.
                </p>

              </div>
            )}

          </div>
        )}

        {!analysis && error && !selectedFile && (
          <p className="error-message" role="alert">
            {error}
          </p>
        )}

      </div>

      {/* Hidden camera input */}
      <input
        ref={cameraInput}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        capture="environment"
        hidden
        onChange={handleImageChange}
      />

      {/* Hidden gallery input */}
      <input
        ref={galleryInput}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        hidden
        onChange={handleImageChange}
      />

    </section>
  );
}

export default UploadSection;
