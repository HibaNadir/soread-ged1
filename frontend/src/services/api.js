const API_URL = "/api";

export async function apiRequest(path, options = {}) {
	const headers = new Headers(options.headers || {});
	const token = localStorage.getItem("access_token");

	if (token) {
		headers.set("Authorization", `Bearer ${token}`);
	}

	const response = await fetch(`${API_URL}${path}`, {
		...options,
		headers,
	});

	if (!response.ok) {
		let message = "Une erreur est survenue.";

		try {
			const error = await response.json();
			message = error.detail || error.message || Object.values(error).flat().join(" ") || message;
		} catch {
			// Keep the generic message when the server does not return JSON.
		}

		throw new Error(message);
	}

	if (response.status === 204) {
		return null;
	}

	const contentType = response.headers.get("content-type") || "";
	return contentType.includes("application/json")
		? response.json()
		: response.blob();
}

export { API_URL };
