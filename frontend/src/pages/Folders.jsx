import { useEffect, useState } from "react";
import MainLayout from "../layouts/MainLayout";
import { createFolder, getFolders } from "../services/folderService";

export default function Folders() {
  const [folders, setFolders] = useState([]);
  const [folderName, setFolderName] = useState("");
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getFolders()
      .then(setFolders)
      .catch((loadError) => setError(loadError.message))
      .finally(() => setIsLoading(false));
  }, []);

  const handleCreate = async (event) => {
    event.preventDefault();
    const name = folderName.trim();

    if (!name) {
      setError("Le nom du dossier est obligatoire.");
      return;
    }

    setIsCreating(true);
    setError("");

    try {
      const folder = await createFolder(name);
      setFolders((currentFolders) => [...currentFolders, folder]);
      setFolderName("");
      setIsFormOpen(false);
    } catch (createError) {
      setError(createError.message);
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <MainLayout>
      <div className="folders-page">
        <div className="folders-header">
          <div>
            <h1>Dossiers</h1>
            <p>Organisez vos documents dans des espaces faciles à retrouver.</p>
          </div>

          <button className="btn-add" onClick={() => setIsFormOpen(true)}>
            + Créer un dossier
          </button>
        </div>

        {error && <div className="page-error">{error}</div>}

        {isFormOpen && (
          <form className="folder-create-form" onSubmit={handleCreate}>
            <label htmlFor="folder-name">Nom du dossier</label>
            <div className="folder-form-row">
              <input
                id="folder-name"
                type="text"
                value={folderName}
                onChange={(event) => setFolderName(event.target.value)}
                placeholder="Ex. Rapports 2026"
                autoFocus
              />
              <button className="btn-add" type="submit" disabled={isCreating}>
                {isCreating ? "Création..." : "Créer"}
              </button>
              <button className="folder-cancel" type="button" onClick={() => setIsFormOpen(false)}>
                Annuler
              </button>
            </div>
          </form>
        )}

        {isLoading ? (
          <div className="folders-empty"><p>Chargement des dossiers...</p></div>
        ) : folders.length === 0 ? (
          <div className="folders-empty">
            <div className="folders-empty-icon">📁</div>
            <h2>Vos dossiers apparaîtront ici</h2>
            <p>Créez votre premier dossier pour structurer votre espace documentaire.</p>
            <button className="btn-open" onClick={() => setIsFormOpen(true)}>Créer mon premier dossier</button>
          </div>
        ) : (
          <div className="folders-grid">
            {folders.map((folder) => (
              <div className="folder-card" key={folder.id}>
                <div className="folders-empty-icon">📁</div>
                <div>
                  <h2>{folder.name}</h2>
                  <p>Créé le {new Date(folder.created_at).toLocaleDateString("fr-FR")}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  );
}