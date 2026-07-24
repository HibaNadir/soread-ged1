import { useLocation, useNavigate, useParams } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";

const fallbackSpaces = {
	1: {
		name: "Équipe Informatique",
		description: "Espace dédié à l'équipe informatique",
		members: 12,
		documents: 24,
		type: "Public",
	},
	2: {
		name: "Projet GED",
		description: "Espace de travail du projet GED",
		members: 4,
		documents: 18,
		type: "Privé",
	},
	3: {
		name: "Ressources Humaines",
		description: "Documents et informations RH",
		members: 8,
		documents: 35,
		type: "Privé",
	},
};

export default function SpaceDetails() {
	const navigate = useNavigate();
	const { id } = useParams();
	const { state } = useLocation();
	const space = state?.space || fallbackSpaces[id];

	if (!space) {
		return (
			<MainLayout>
				<div className="space-details-empty">
					<h1>Espace introuvable</h1>
					<p>Cet espace n'existe plus ou n'est pas accessible.</p>
					<button className="btn-open" onClick={() => navigate("/spaces")}>Retour aux espaces</button>
				</div>
			</MainLayout>
		);
	}

	return (
		<MainLayout>
			<div className="space-details-page">
				<button className="back-link" onClick={() => navigate("/spaces")}>← Retour aux espaces</button>

				<div className="space-details-hero">
					<div className="space-details-icon">📁</div>
					<div>
						<span className={space.type === "Public" ? "badge-public" : "badge-private"}>{space.type}</span>
						<h1>{space.name}</h1>
						<p>{space.description}</p>
					</div>
				</div>

				<div className="space-details-stats">
					<div><strong>{space.members}</strong><span>Membres</span></div>
					<div><strong>{space.documents}</strong><span>Documents</span></div>
					<div><strong>{space.type}</strong><span>Visibilité</span></div>
				</div>

				<div className="space-details-panel">
					<h2>Contenu de l'espace</h2>
					<p>Les documents et les échanges de cet espace apparaîtront ici.</p>
					<button className="btn-add" onClick={() => navigate("/documents")}>Voir les documents</button>
				</div>
			</div>
		</MainLayout>
	);
}
