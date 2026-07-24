import MainLayout from "../layouts/MainLayout";
import logo from "../assets/logo2m.png";

export default function Dashboard() {
  const statistics = [
    {
      icon: "📄",
      number: "248",
      label: "Documents",
      description: "Documents disponibles",
      className: "blue",
    },
    {
      icon: "📁",
      number: "36",
      label: "Dossiers",
      description: "Dossiers organisés",
      className: "orange",
    },
    {
      icon: "👥",
      number: "18",
      label: "Espaces",
      description: "Espaces collaboratifs",
      className: "green",
    },
    {
      icon: "🔔",
      number: "7",
      label: "Notifications",
      description: "Notifications non lues",
      className: "purple",
    },
  ];

  const recentDocuments = [
    {
      name: "Rapport annuel 2026",
      type: "PDF",
      author: "Sara Lachhab",
      date: "Aujourd'hui",
    },
    {
      name: "Présentation projet GED",
      type: "PPTX",
      author: "Malak Khalil",
      date: "Hier",
    },
    {
      name: "Contrat de partenariat",
      type: "DOCX",
      author: "Ahmed Benali",
      date: "Il y a 2 jours",
    },
  ];

  return (
    <MainLayout>
      <div className="dashboard">

        {/* Header */}
        <div className="dashboard-welcome">

          <div>
            <span className="welcome-label">
              ESPACE DE TRAVAIL
            </span>

            <h1>
              Bonjour Sara 👋
            </h1>

            <p>
              Voici un aperçu de votre activité sur la plateforme SOREAD GED.
            </p>
          </div>

          <div className="dashboard-logo-container">
            <img
              src={logo}
              alt="Logo 2M"
              className="dashboard-logo"
            />
          </div>

        </div>

        {/* Statistiques */}
        <div className="statistics-grid">

          {statistics.map((statistic) => (

            <div
              className={`stat-card ${statistic.className}`}
              key={statistic.label}
            >

              <div className="stat-icon">
                {statistic.icon}
              </div>

              <div className="stat-content">

                <h2>
                  {statistic.number}
                </h2>

                <h3>
                  {statistic.label}
                </h3>

                <p>
                  {statistic.description}
                </p>

              </div>

            </div>

          ))}

        </div>

        {/* Actions rapides */}
        <div className="dashboard-section">

          <div className="section-title">

            <div>
              <h2>
                Actions rapides
              </h2>

              <p>
                Accédez rapidement aux fonctionnalités principales.
              </p>
            </div>

          </div>

          <div className="quick-actions">

            <button className="quick-action blue-action">
              <span>📤</span>
              <div>
                <strong>Ajouter un document</strong>
                <small>Importer un nouveau fichier</small>
              </div>
            </button>

            <button className="quick-action orange-action">
              <span>📁</span>
              <div>
                <strong>Créer un dossier</strong>
                <small>Organiser vos documents</small>
              </div>
            </button>

            <button className="quick-action green-action">
              <span>👥</span>
              <div>
                <strong>Rejoindre un espace</strong>
                <small>Collaborer avec une équipe</small>
              </div>
            </button>

          </div>

        </div>

        {/* Documents récents et activité */}
        <div className="dashboard-columns">

          <div className="dashboard-section documents-recent">

            <div className="section-title">

              <div>
                <h2>
                  Documents récents
                </h2>

                <p>
                  Les derniers documents ajoutés.
                </p>
              </div>

              <a href="/documents">
                Voir tout
              </a>

            </div>

            <div className="recent-documents">

              {recentDocuments.map((document) => (

                <div
                  className="recent-document"
                  key={document.name}
                >

                  <div className="document-file-icon">
                    📄
                  </div>

                  <div className="document-details">

                    <h3>
                      {document.name}
                    </h3>

                    <p>
                      {document.type} • {document.author}
                    </p>

                  </div>

                  <span className="document-date">
                    {document.date}
                  </span>

                </div>

              ))}

            </div>

          </div>

          <div className="dashboard-section activity-section">

            <div className="section-title">

              <div>
                <h2>
                  Activité récente
                </h2>

                <p>
                  Les dernières actions.
                </p>
              </div>

            </div>

            <div className="activity-list">

              <div className="activity-item">
                <span className="activity-dot blue-dot"></span>

                <div>
                  <strong>
                    Nouveau document ajouté
                  </strong>

                  <small>
                    Il y a 10 minutes
                  </small>
                </div>
              </div>

              <div className="activity-item">
                <span className="activity-dot green-dot"></span>

                <div>
                  <strong>
                    Invitation à un espace
                  </strong>

                  <small>
                    Il y a 1 heure
                  </small>
                </div>
              </div>

              <div className="activity-item">
                <span className="activity-dot orange-dot"></span>

                <div>
                  <strong>
                    Document partagé avec vous
                  </strong>

                  <small>
                    Hier
                  </small>
                </div>
              </div>

            </div>

          </div>

        </div>

      </div>
    </MainLayout>
  );
}