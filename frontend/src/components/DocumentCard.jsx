export default function DocumentCard({ document, onDelete }) {
  return (
    <div className="document-card">

      <div className="document-icon">
        {document.type === "PDF" ? "📕" : "📄"}
      </div>

      <div className="document-info">

        <h3>{document.name}</h3>

        <p>
          Propriétaire : <strong>{document.owner}</strong>
        </p>

        <p>
          Modifié le : {document.date}
        </p>

        <span className="document-type">
          {document.type}
        </span>

      </div>

      <div className="document-actions">

        <button className="btn-view">
          Voir
        </button>

        <button className="btn-download">
          Télécharger
        </button>

        <button
          className="btn-delete"
          onClick={() => onDelete(document.id)}
        >
          Supprimer
        </button>

      </div>

    </div>
  );
}