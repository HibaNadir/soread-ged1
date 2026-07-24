import { useState } from "react";
import MainLayout from "../layouts/MainLayout";

export default function Search() {
  const [searchTerm, setSearchTerm] = useState("");
  const [submittedTerm, setSubmittedTerm] = useState("");
  const [selectedType, setSelectedType] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");

  const documents = [
    {
      id: 1,
      name: "Rapport annuel 2026",
      type: "PDF",
      author: "Sara Lachhab",
      date: "21/07/2026",
      category: "Rapports",
    },
    {
      id: 2,
      name: "Contrat de partenariat",
      type: "DOCX",
      author: "Ahmed Benali",
      date: "19/07/2026",
      category: "Contrats",
    },
    {
      id: 3,
      name: "Présentation projet GED",
      type: "PPTX",
      author: "Malak Khalil",
      date: "17/07/2026",
      category: "Projets",
    },
  ];

  const filteredDocuments = documents.filter((document) =>
    document.name.toLowerCase().includes(submittedTerm.toLowerCase())
    && (!selectedType || document.type === selectedType)
    && (!selectedCategory || document.category === selectedCategory)
  );

  const handleSearch = (event) => {
    event.preventDefault();
    setSubmittedTerm(searchTerm.trim());
  };

  return (
    <MainLayout>
      <div className="search-page">

        <div className="search-header">
          <h1>Recherche documentaire</h1>
          <p>Recherchez rapidement un document dans la plateforme.</p>
        </div>

        <form className="advanced-search" onSubmit={handleSearch}>

          <div className="search-input-wrapper">
            <span>🔎</span>

            <input
              type="text"
              placeholder="Rechercher par nom de document..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <select value={selectedType} onChange={(event) => setSelectedType(event.target.value)}>
            <option value="">Tous les types</option>
            <option value="PDF">PDF</option>
            <option value="DOCX">DOCX</option>
            <option value="PPTX">PPTX</option>
          </select>

          <select value={selectedCategory} onChange={(event) => setSelectedCategory(event.target.value)}>
            <option value="">Toutes les catégories</option>
            <option value="Rapports">Rapports</option>
            <option value="Contrats">Contrats</option>
            <option value="Projets">Projets</option>
          </select>

          <button className="search-button" type="submit">
            Rechercher
          </button>

        </form>

        <div className="results-header">
          <h2>Résultats de recherche</h2>
          <span>{filteredDocuments.length} document(s)</span>
        </div>

        <div className="search-results">

          {filteredDocuments.length > 0 ? (

            filteredDocuments.map((document) => (

              <div className="result-card" key={document.id}>

                <div className="result-icon">
                  📄
                </div>

                <div className="result-info">

                  <h3>{document.name}</h3>

                  <p>
                    {document.type} • {document.category}
                  </p>

                  <small>
                    Créé par {document.author} le {document.date}
                  </small>

                </div>

                <button className="btn-view">
                  Consulter
                </button>

              </div>

            ))

          ) : (

            <div className="no-results">
              Aucun document trouvé.
            </div>

          )}

        </div>

      </div>
    </MainLayout>
  );
}