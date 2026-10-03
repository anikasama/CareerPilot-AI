import { useRef } from "react";

export default function UploadBox({
  file,
  setFile,
}) {
  const inputRef = useRef(null);

  function handleFileChange(event) {
    const selected = event.target.files?.[0];

    if (!selected) {
      return;
    }

    if (
      selected.type !== "application/pdf" &&
      !selected.name.toLowerCase().endsWith(".pdf")
    ) {
      alert("Please upload a PDF resume.");
      return;
    }

    if (selected.size > 5 * 1024 * 1024) {
      alert("Maximum file size is 5 MB.");
      return;
    }

    setFile(selected);
  }

  function removeFile() {
    setFile(null);

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  }

  return (
    <div className="upload-wrapper">
      <div
        className={`upload-box ${
          file ? "upload-box-selected" : ""
        }`}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          hidden
        />

        <div className="upload-icon">
          {file ? "✓" : "↑"}
        </div>

        {file ? (
          <>
            <h3>{file.name}</h3>

            <p>
              {(file.size / 1024 / 1024).toFixed(2)} MB
              {" • "}
              PDF
            </p>

            <button
              type="button"
              className="remove-file"
              onClick={(event) => {
                event.stopPropagation();
                removeFile();
              }}
            >
              Remove file
            </button>
          </>
        ) : (
          <>
            <h3>Upload your resume</h3>

            <p>
              Drop your PDF here or click to browse
            </p>

            <small>
              PDF only • Maximum 5 MB
            </small>
          </>
        )}
      </div>
    </div>
  );
}