import os

root = "pdf-song-frontend"
src = os.path.join(root, "src")
components = os.path.join(src, "components")
pages = os.path.join(src, "pages")

files = {
    "package.json": """
{
  "name": "pdf-song-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "axios": "^1.6.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
""",

    "src/index.js": """
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
""",

    "src/App.js": """
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Verify from "./pages/Verify";
import ResetPassword from "./pages/ResetPassword";
import OAuthSuccess from "./pages/OAuthSuccess";
import Compose from "./pages/Compose";
import Songs from "./pages/Songs";
import Analytics from "./pages/Analytics";
import Billing from "./pages/Billing";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/verify" element={<Verify />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/oauth-success" element={<OAuthSuccess />} />

        <Route
          path="/compose"
          element={
            <ProtectedRoute>
              <Compose />
            </ProtectedRoute>
          }
        />

        <Route
          path="/songs"
          element={
            <ProtectedRoute>
              <Songs />
            </ProtectedRoute>
          }
        />

        <Route
          path="/analytics"
          element={
            <ProtectedRoute admin>
              <Analytics />
            </ProtectedRoute>
          }
        />

        <Route
          path="/billing"
          element={
            <ProtectedRoute>
              <Billing />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
""",

    "src/api.js": """
import axios from "axios";

const API = process.env.REACT_APP_API_URL;

export const api = axios.create({
  baseURL: API,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
""",

    "src/auth.js": """
export const login = (token) => {
  localStorage.setItem("token", token);
};

export const logout = () => {
  localStorage.removeItem("token");
};

export const isLoggedIn = () => {
  return !!localStorage.getItem("token");
};
""",

    "src/components/Navbar.js": """
import { Link } from "react-router-dom";
import { isLoggedIn, logout } from "../auth";

export default function Navbar() {
  return (
    <nav>
      <Link to="/">Login</Link>
      <Link to="/register">Register</Link>

      {isLoggedIn() && (
        <>
          <Link to="/compose">Compose</Link>
          <Link to="/songs">Songs</Link>
          <Link to="/billing">Billing</Link>
          <Link to="/analytics">Analytics</Link>
          <button onClick={logout}>Logout</button>
        </>
      )}
    </nav>
  );
}
""",

    "src/components/ProtectedRoute.js": """
import { Navigate } from "react-router-dom";
import { isLoggedIn } from "../auth";
import { api } from "../api";
import { useEffect, useState } from "react";

export default function ProtectedRoute({ children, admin }) {
  const [allowed, setAllowed] = useState(false);

  useEffect(() => {
    if (!isLoggedIn()) return setAllowed(false);

    if (!admin) return setAllowed(true);

    api.get("/analytics/overview")
      .then(() => setAllowed(true))
      .catch(() => setAllowed(false));
  }, [admin]);

  if (!allowed) return <Navigate to="/" />;

  return children;
}
""",

    "src/pages/Login.js": """
import { useState } from "react";
import { api } from "../api";
import { login } from "../auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
    const res = await api.post("/login", { email, password });
    login(res.data.access_token);
    window.location = "/compose";
  };

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="email" onChange={(e) => setEmail(e.target.value)} />
      <input placeholder="password" type="password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={submit}>Login</button>

      <a href={`${process.env.REACT_APP_API_URL}/login/google`}>
        <button>Login with Google</button>
      </a>

      <a href={`${process.env.REACT_APP_API_URL}/login/microsoft`}>
        <button>Login with Microsoft</button>
      </a>
    </div>
  );
}
""",

    "src/pages/Register.js": """
import { useState } from "react";
import { api } from "../api";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
    await api.post("/register", { email, password });
    alert("Check your email to verify.");
  };

  return (
    <div>
      <h2>Register</h2>
      <input placeholder="email" onChange={(e) => setEmail(e.target.value)} />
      <input placeholder="password" type="password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={submit}>Register</button>
    </div>
  );
}
""",

    "src/pages/Verify.js": """
import { useEffect } from "react";
import { api } from "../api";

export default function Verify() {
  const token = new URLSearchParams(window.location.search).get("token");

  useEffect(() => {
    api.get(`/verify?token=${token}`).then(() => {
      alert("Account verified!");
      window.location = "/";
    });
  }, [token]);

  return <p>Verifying...</p>;
}
""",

    "src/pages/ResetPassword.js": """
import { useState } from "react";
import { api } from "../api";

export default function ResetPassword() {
  const token = new URLSearchParams(window.location.search).get("token");
  const [password, setPassword] = useState("");

  const submit = async () => {
    await api.post("/reset-password", { token, new_password: password });
    alert("Password updated");
    window.location = "/";
  };

  return (
    <div>
      <h2>Reset Password</h2>
      <input placeholder="new password" type="password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={submit}>Update</button>
    </div>
  );
}
""",

    "src/pages/OAuthSuccess.js": """
import { useEffect } from "react";
import { login } from "../auth";

export default function OAuthSuccess() {
  const token = new URLSearchParams(window.location.search).get("token");

  useEffect(() => {
    login(token);
    window.location = "/compose";
  }, [token]);

  return <p>Logging you in...</p>;
}
""",

    "src/pages/Compose.js": """
import { useState } from "react";
import { api } from "../api";

export default function Compose() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const submit = async () => {
    const form = new FormData();
    form.append("file", file);

    const res = await api.post("/compose", form);
    setResult(res.data);
  };

  return (
    <div>
      <h2>Compose Song</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={submit}>Generate</button>

      {result && (
        <div>
          <h3>Song Generated</h3>
          <audio controls src={`${process.env.REACT_APP_API_URL}/download-audio?path=${result.audio_file_path}`} />
          <pre>{result.musicxml}</pre>
        </div>
      )}
    </div>
  );
}
""",

    "src/pages/Songs.js": """
import { useEffect, useState } from "react";
import { api } from "../api";

export default function Songs() {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    api.get("/songs").then((res) => setSongs(res.data));
  }, []);

  return (
    <div>
      <h2>Your Songs</h2>

      {songs.map((song) => (
        <div key={song.id}>
          <h3>{song.title}</h3>
          <audio controls src={`${process.env.REACT_APP_API_URL}/download-audio?path=${song.audio_path}`} />
          <pre>{song.musicxml}</pre>
        </div>
      ))}
    </div>
  );
}
""",

    "src/pages/Analytics.js": """
import { useEffect, useState } from "react";
import { api } from "../api";

export default function Analytics() {
  const [overview, setOverview] = useState(null);

  useEffect(() => {
    api.get("/analytics/overview").then((res) => setOverview(res.data));
  }, []);

  if (!overview) return <p>Loading...</p>;

  return (
    <div>
      <h2>Analytics</h2>
      <p>Total Users: {overview.total_users}</p>
      <p>Active Subscriptions: {overview.active_subscriptions}</p>
      <p>Total Songs: {overview.total_songs}</p>
      <p>Avg Render Time: {overview.avg_render_time_ms} ms</p>
    </div>
  );
}
""",

    "src/pages/Billing.js": """
import { api } from "../api";

export default function Billing() {
  const subscribe = async (priceId) => {
    const res = await api.post("/create-checkout-session", { price_id: priceId });
    window.location = res.data.checkout_url;
  };

  return (
    <div>
      <h2>Subscription Plans</h2>

      <button onClick={() => subscribe("price_basic")}>Basic</button>
      <button onClick={() => subscribe("price_pro")}>Pro</button>
      <button onClick={() => subscribe("price_annual")}>Annual</button>
    </div>
  );
}
"""
}

# -------------------------------------------------------------------
# BUILD FOLDERS
# -------------------------------------------------------------------

os.makedirs(root, exist_ok=True)
os.makedirs(src, exist_ok=True)
os.makedirs(components, exist_ok=True)
os.makedirs(pages, exist_ok=True)

# -------------------------------------------------------------------
# WRITE FILES
# -------------------------------------------------------------------

for path, content in files.items():
    full_path = os.path.join(root, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip())

print("Frontend generated successfully in pdf-song-frontend/")
