import { useEffect, useRef, useState } from "react";
import MainLayout from "../layouts/MainLayout";
import {
  createDocument,
  deleteDocument,
  downloadDocument,
  getDocuments,
  viewDocument,
} from "../services/documentService";

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  useEffect(() => {
    getDocuments()
      .then(setDocuments)
      .catch((loadError) => setError(loadError.message))
      .finally(() => setIsLoading(false));
  }, []);

  const handleUpload = async (event) => {
    const file = event.target.files?.[0];
    event.target.value = "";

    if (!file) return;

    setIsUploading(true);
    setError("");

    try {
      const document = await createDocument(file, file.name);
      setDocuments((currentDocuments) => [document, ...currentDocuments]);
    } catch (uploadError) {
      setError(uploadError.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (document) => {
    if (!window.confirm(`Supprimer « ${document.title} » ?`)) return;

    try {
      await deleteDocument(document.id);
      setDocuments((currentDocuments) =>
        currentDocuments.filter((item) => item.id !== document.id)
      );
    } catch (deleteError) {
      setError(deleteError.message);
    }
  };

  const handleView = async (document) => {
    try {
      await viewDocument(document);
    } catch (viewError) {
      setError(viewError.message);
    }
  };

  const filteredDocuments = documents.filter((document) =>
    document.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <MainLayout>
      <div className="documents-header">
        <div>
          <h1>Gestion documentaire</h1>
          <p>Ajoutez, consultez et gérez vos documents depuis un seul espace.</p>
        </div>

        <button className="btn-add" onClick={() => fileInputRef.current?.click()} disabled={isUploading}>
          {isUploading ? "Ajout en cours..." : "+ Ajouter un document"}
        </button>
        <input ref={fileInputRef} type="file" hidden onChange={handleUpload} />
      </div>

      {error && <div className="page-error">{error}</div>}

      <div className="search-container">
        <input
          type="text"
          placeholder="Rechercher un document..."
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
        />
      </div>

      <table className="documents-table">

        <thead>

          <tr>

            <th>Nom</th>

            <th>Type</th>

            <th>Auteur</th>

            <th>Date</th>

            <th>Actions</th>

          </tr>

        </thead>

        <tbody>
          {isLoading ? (
            <tr><td colSpan="5">Chargement des documents...</td></tr>
          ) : filteredDocuments.length === 0 ? (
            <tr><td colSpan="5">Aucun document trouvé.</td></tr>
          ) : filteredDocuments.map((document) => (
            <tr key={document.id}>
              <td>{document.title}</td>
              <td>{document.file?.split(".").pop()?.toUpperCase() || "-"}</td>
              <td>{document.owner || "Vous"}</td>
              <td>{new Date(document.created_at).toLocaleDateString("fr-FR")}</td>
              <td>
                <button className="btn-view" onClick={() => handleView(document)}>Voir</button>
                <button className="btn-download" onClick={() => downloadDocument(document)}>Télécharger</button>
                <button className="btn-delete" onClick={() => handleDelete(document)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>

      </table>

    </MainLayout>
  );
}