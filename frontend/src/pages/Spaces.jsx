import { useNavigate } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";

export default function Spaces() {
  const navigate = useNavigate();
  const spaces = [
    {
      id: 1,
      name: "Équipe Informatique",
      description: "Espace dédié à l'équipe informatique",
      members: 12,
      documents: 24,
      type: "Public",
    },
    {
      id: 2,
      name: "Projet GED",
      description: "Espace de travail du projet GED",
      members: 4,
      documents: 18,
      type: "Privé",
    },
    {
      id: 3,
      name: "Ressources Humaines",
      description: "Documents et informations RH",
      members: 8,
      documents: 35,
      type: "Privé",
    },
  ];

  return (
    <MainLayout>
      <div className="spaces-header">
        <div>
          <h1>Espaces collaboratifs</h1>
          <p>Travaillez et partagez des documents avec vos équipes.</p>
        </div>

        <button className="btn-add">
          + Créer un espace
        </button>
      </div>

      <div className="spaces-grid">
        {spaces.map((space) => (
          <div className="space-card" key={space.id}>

            <div className="space-icon">
              📁
            </div>

            <div className="space-content">

              <div className="space-title">
                <h2>{space.name}</h2>

                <span className={space.type === "Public" ? "badge-public" : "badge-private"}>
                  {space.type}
                </span>
              </div>

              <p>{space.description}</p>

              <div className="space-info">
                <span>👥 {space.members} membres</span>
                <span>📄 {space.documents} documents</span>
              </div>

              <button className="btn-open" onClick={() => navigate(`/spaces/${space.id}`, { state: { space } })}>
                Ouvrir l'espace
              </button>

            </div>

          </div>
        ))}
      </div>
    </MainLayout>
  );
}