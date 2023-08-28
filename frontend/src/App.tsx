import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [upload, setUpload] = useState<
    { ok: boolean; msg: string } | { ok: null } | null
  >(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedFile(event.target.files![0]);
  };

  const handleUpload = async () => {
    if (selectedFile) {
      setUpload({ ok: null });
      try {
        const imageContent = await selectedFile.arrayBuffer();
        const response = await fetch("/predict", {
          method: "POST",
          headers: {
            "Content-Type": "image/jpeg", // Change this to match the actual image type
          },
          body: imageContent,
        });

        if (response.ok) {
          const data = await response.text();
          setUpload({ ok: true, msg: data });
        } else {
          setUpload({ ok: false, msg: "error" });
        }
      } catch (error) {
        console.error("Error uploading image:", error);
        setUpload({ ok: false, msg: "error" });
      }
    }
  };

  const tryAnother = (e: React.MouseEvent) => {
    e.preventDefault();
    setSelectedFile(null);
    setUpload(null);
  };

  return (
    <div className="App">
      <h1>Image Upload and Recognition</h1>
      {selectedFile && (
        <p>
          <img
            style={{ maxWidth: 400 }}
            src={URL.createObjectURL(selectedFile)}
          />
        </p>
      )}
      {upload ? (
        upload.ok === null ? (
          "..."
        ) : (
          <>
            <p>Label: {upload.msg}</p>
            <a href="/" onClick={tryAnother}>
              Try another
            </a>
          </>
        )
      ) : (
        <>
          <input type="file" onChange={handleFileChange} />
          <button disabled={!selectedFile} onClick={handleUpload}>
            Upload
          </button>
        </>
      )}
    </div>
  );
}

export default App;
