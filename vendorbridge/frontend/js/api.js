const BASE = "http://localhost:8000";

function getToken() {
  return localStorage.getItem("token");
}

async function apiFetch(endpoint, method = "GET", body = null) {
  const headers = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${getToken()}`
  };
  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);
  const res = await fetch(BASE + endpoint, options);
  if (res.status === 401) {
    localStorage.clear();
    window.location.href = "index.html";
  }
  return res.json();
}