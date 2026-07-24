import { apiRequest } from "./api";

export function getProfile() {
  return apiRequest("/accounts/me/");
}

export function updateProfile(profile) {
  return apiRequest("/accounts/me/", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
}