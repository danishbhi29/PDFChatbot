import { useState } from "react";
import "./FileUpload.css";
import api from "../Services/api";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      setIsUploading(true);
      const response = await api.post("/upload", formData);

      alert(response.data.message);
    } catch (error) {
      console.log(error);
      console.log(error.response);
      console.log(error.response?.data);

      const message =
        error.response?.data?.detail ||
        error.message ||
        "Upload failed";

      alert(message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <h1>PDF Chatbot</h1>

      <input type="file" accept=".pdf" onChange={handleFileChange} />

      <button onClick={handleUpload} disabled={isUploading}>
        {isUploading ? "Uploading..." : "Upload PDF"}
      </button>
    </div>
  );
}

export default FileUpload;
