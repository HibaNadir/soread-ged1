import { apiRequest, API_URL } from "./api";

export function getDocuments() {
	return apiRequest("/documents/");
}

export function createDocument(file, title, description = "") {
	const formData = new FormData();
	formData.append("title", title || file.name);
	formData.append("description", description);
	formData.append("file", file);

	return apiRequest("/documents/", {
		method: "POST",
		body: formData,
	});
}

export function deleteDocument(id) {
	return apiRequest(`/documents/${id}/`, { method: "DELETE" });
}

export function getDocumentUrl(id) {
	return `${API_URL}/documents/${id}/download/`;
}

export async function downloadDocument(document) {
	const blob = await apiRequest(`/documents/${document.id}/download/`);
	const url = URL.createObjectURL(blob);
	const link = window.document.createElement("a");

	link.href = url;
	link.download = document.title || "document";
	link.click();
	URL.revokeObjectURL(url);
}

export async function viewDocument(document) {
	const blob = await apiRequest(`/documents/${document.id}/download/`);
	const url = URL.createObjectURL(blob);
	window.open(url, "_blank", "noopener,noreferrer");
}
