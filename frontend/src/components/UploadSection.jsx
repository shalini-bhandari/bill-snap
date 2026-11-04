
import { useEffect, useRef, useState } from "react";

function UploadSection() {

  const galleryInput = useRef(null);
  const cameraInput = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);

  // Clean up temporary image URLs
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

    if (!file.type.startsWith("image/")) {
      alert("Please select a valid image.");
      event.target.value = "";
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert("Image size must be less than 10 MB.");
      event.target.value = "";
      return;
    }

    setSelectedFile(file);
  }

  function removeImage() {
    setSelectedFile(null);

    if (galleryInput.current) {
      galleryInput.current.value = "";
    }

    if (cameraInput.current) {
      cameraInput.current.value = "";
    }
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

            <button
              className="secondary-button"
              onClick={removeImage}
            >
              Remove image
            </button>

            <p className="upload-note">
              AI analysis will be available in our next milestone.
            </p>

          </div>
        )}

      </div>

      {/* Hidden camera input */}
      <input
        ref={cameraInput}
        type="file"
        accept="image/*"
        capture="environment"
        hidden
        onChange={handleImageChange}
      />

      {/* Hidden gallery input */}
      <input
        ref={galleryInput}
        type="file"
        accept="image/*"
        hidden
        onChange={handleImageChange}
      />

    </section>
  );
}

export default UploadSection;
