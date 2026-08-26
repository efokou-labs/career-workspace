"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

type Application = {
  id: number;
  company: string;
  role: string;
  status: string;
};

export default function Page() {
  const [items, setItems] = useState<Application[]>([]);
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    const res = await fetch("/api/applications");
    if (!res.ok) {
      throw new Error("Could not load applications");
    }
    setItems(await res.json());
  }, []);

  useEffect(() => {
    refresh().catch((err: unknown) => {
      setError(err instanceof Error ? err.message : "Could not load applications");
    });
  }, [refresh]);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setError("");
    const res = await fetch("/api/applications", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company, role }),
    });
    if (!res.ok) {
      setError("Could not create application");
      return;
    }
    setCompany("");
    setRole("");
    await refresh();
  }

  return (
    <main>
      <h1>Career workspace</h1>
      <p>Track job applications.</p>

      <form onSubmit={onSubmit}>
        <label>
          Company
          <input
            name="company"
            value={company}
            onChange={(event) => setCompany(event.target.value)}
            required
          />
        </label>
        <label>
          Role
          <input
            name="role"
            value={role}
            onChange={(event) => setRole(event.target.value)}
            required
          />
        </label>
        <button type="submit">Add application</button>
      </form>

      {error ? <p className="error">{error}</p> : null}

      {items.length === 0 ? (
        <p className="empty">No applications yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Company</th>
              <th>Role</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.company}</td>
                <td>{item.role}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
