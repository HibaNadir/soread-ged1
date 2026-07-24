import { apiRequest } from "./api";

export function getFolders() {
  return apiRequest("/folders/");
}

export function createFolder(name, parent = null) {
  return apiRequest("/folders/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, parent }),
  });
}