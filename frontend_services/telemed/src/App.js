import React, { useState, useEffect, useMemo, useRef } from 'react';

const API_BASE = 'http://127.0.0.1:8000';

const ConsultationMessenger = () => {
  const [roles, setRoles] = useState([]);
  const [consultations, setConsultations] = useState([]);
  const [messages, setMessages] = useState([]);

  const [selectedConsultation, setSelectedConsultation] = useState('');
  const [selectedRoleFilter, setSelectedRoleFilter] = useState('');
  const [sendAsUser, setSendAsUser] = useState('');
  const [messageContent, setMessageContent] = useState('');

  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const pollRef = useRef(null);

  useEffect(() => {
    fetchRoles();
    fetchConsultations();
  }, []);

  useEffect(() => {
    if (selectedConsultation) {
      fetchMessages();

      clearInterval(pollRef.current);
      pollRef.current = setInterval(fetchMessages, 10000);
      return () => clearInterval(pollRef.current);
    } else {
      setMessages([]);
      clearInterval(pollRef.current);
    }
  }, [selectedConsultation, selectedRoleFilter]);

  const fetchRoles = async () => {
    try {
      const res = await fetch(`${API_BASE}/roles/all/`);
      const data = await res.json();
      setRoles(data.results || []);
    } catch {
      setError('Failed to load roles');
    }
  };

  const fetchConsultations = async () => {
    try {
      const res = await fetch(`${API_BASE}/consultations/all/`);
      const data = await res.json();
      const sorted = (data.results || []).slice().sort((a, b) => new Date(b.date_created) - new Date(a.date_created));
      setConsultations(sorted);
    } catch {
      setError('Failed to load consultations');
    }
  };

  const fetchMessages = async () => {
    if (!selectedConsultation) return;
    setLoading(true);
    try {
      let url = `${API_BASE}/consultation-messages/all/?consultation=${selectedConsultation}`;
      if (selectedRoleFilter) url += `&role=${selectedRoleFilter}`;
      const res = await fetch(url);
      const data = await res.json();
      const list = (data.results || []).slice().sort((a, b) => new Date(a.date_created) - new Date(b.date_created));
      setMessages(list);
      setError('');
    } catch {
      setError('Failed to load messages');
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    setError('');

    if (!messageContent.trim() || !selectedConsultation || !sendAsUser) {
      setError('Select consultation, choose sender, and type a message.');
      return;
    }

    const { userId, role } = JSON.parse(sendAsUser);

    const roleData = roles.find(r => r.title === role);
    if (!roleData) {
      setError('Invalid sender role.');
      return;
    }

    const payload = {
      consultation: Number(selectedConsultation),
      author: userId,
      author_role: roleData.id,
      content: messageContent.trim(),
    };

    setSending(true);
    try {
      const res = await fetch(`${API_BASE}/consultation-messages/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        setError('Failed to send message');
        return;
      }

      setMessageContent('');
      await fetchMessages();
    } catch {
      setError('Error sending message');
    } finally {
      setSending(false);
    }
  };

  const formatDate = (iso) =>
    new Date(iso).toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });

  const getConsultationLabel = (c) => {
    const date = new Date(c.date_created);
    const formattedDate = date.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
    return `${formattedDate} : Between ${c.doctor_username} and ${c.patient_username}`;
  };

  const roleById = useMemo(() => {
    const m = new Map();
    roles.forEach(r => m.set(r.id, r.title));
    return m;
  }, [roles]);

  return (
    <div style={sx.page}>
      <section style={sx.card}>
        <div style={sx.grid2}>
          <div>
            <label style={sx.label}>Consultation</label>
            <select
              value={selectedConsultation}
              onChange={(e) => setSelectedConsultation(e.target.value)}
              style={sx.select}
            >
              <option value="">Select a consultation</option>
              {consultations.map((c) => (
                <option key={c.id} value={c.id}>
                  {getConsultationLabel(c)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label style={sx.label}>Role Filter (optional)</label>
            <select
              value={selectedRoleFilter}
              onChange={(e) => setSelectedRoleFilter(e.target.value)}
              style={sx.select}
              disabled={!selectedConsultation}
            >
              <option value="">All roles</option>
              {roles.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.title}
                </option>
              ))}
            </select>
          </div>
        </div>
      </section>

      {error && <div style={sx.error}>{error}</div>}

      <section style={sx.card}>
        {loading ? (
          <div style={sx.loading}>Loading messages…</div>
        ) : !selectedConsultation ? (
          <div style={sx.empty}>Pick a consultation to view messages.</div>
        ) : messages.length === 0 ? (
          <div style={sx.empty}>No messages found{selectedRoleFilter ? ' for this role.' : '.'}</div>
        ) : (
          <ul style={sx.list}>
            {messages.map((m) => (
              <li
                key={m.id}
                style={{
                  ...sx.msgItem,
                  ...(m.author_role_title === 'Doctor' ? sx.msgDoctor : sx.msgPatient),
                }}
              >
                <div style={sx.row}>
                  <strong>{m.author_username}</strong>
                  <span style={sx.roleTag}>
                    {m.author_role_title || roleById.get(m.author_role) || '—'}
                  </span>
                  <span style={sx.time}>{formatDate(m.date_created)}</span>
                </div>
                <p style={sx.msg}>{m.content}</p>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section style={sx.card}>
        <form onSubmit={handleSendMessage}>
          <div style={sx.grid2}>
            <div>
              <label style={sx.label}>Send as</label>
              <select
                value={sendAsUser}
                onChange={(e) => setSendAsUser(e.target.value)}
                style={sx.select}
                required
                disabled={!selectedConsultation}
              >
                <option value="">Select user</option>
                {selectedConsultation &&
                  (() => {
                    const c = consultations.find(
                      (x) => x.id === Number(selectedConsultation)
                    );
                    if (!c) return null;
                    return (
                      <>
                        <option
                          value={JSON.stringify({
                            userId: c.doctor,
                            role: 'Doctor',
                          })}
                        >
                          {c.doctor_username} (Doctor)
                        </option>
                        <option
                          value={JSON.stringify({
                            userId: c.patient,
                            role: 'Patient',
                          })}
                        >
                          {c.patient_username} (Patient)
                        </option>
                      </>
                    );
                  })()}
              </select>
            </div>

            <div>
              <label style={sx.label}>Message</label>
              <textarea
                value={messageContent}
                onChange={(e) => setMessageContent(e.target.value)}
                placeholder="Type your message…"
                rows={3}
                style={sx.textarea}
                required
                disabled={!selectedConsultation}
              />
            </div>
          </div>

          <button type="submit" style={sx.button} disabled={sending || !selectedConsultation}>
            {sending ? 'Sending…' : 'Send Message'}
          </button>
        </form>
      </section>
    </div>
  );
};

const sx = {
  page: {
    maxWidth: 920,
    margin: '0 auto',
    padding: '24px',
    background: '#fafafa',
    minHeight: '100vh',
    color: '#222',
  },
  card: {
    background: '#fff',
    border: '1px solid #e7e7e7',
    borderRadius: 10,
    padding: 16,
    marginBottom: 16,
  },
  grid2: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 16,
  },
  label: { display: 'block', fontSize: 13, color: '#444', marginBottom: 6 },
  select: {
    width: '100%',
    padding: '10px 12px',
    fontSize: 15,
    border: '1px solid #dcdcdc',
    borderRadius: 8,
    background: '#fff',
    outline: 'none',
  },
  error: {
    padding: '10px 12px',
    borderRadius: 8,
    background: '#fff4f4',
    color: '#b00020',
    border: '1px solid #ffd6d6',
    marginBottom: 16,
    fontSize: 14,
  },
  loading: { textAlign: 'center', padding: 40, color: '#666' },
  empty: { textAlign: 'center', padding: '48px 8px', color: '#888' },
  list: { listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 12 },
  msgItem: {
    border: '1px solid #eee',
    borderRadius: 10,
    padding: 12,
  },
  msgDoctor: { background: '#f3f8ff', borderLeft: '3px solid #2f7ed8' },
  msgPatient: { background: '#f9f9f9', borderLeft: '3px solid #6aa84f' },
  row: { display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' },
  roleTag: {
    fontSize: 12,
    padding: '2px 8px',
    borderRadius: 999,
    border: '1px solid #ddd',
    color: '#555',
  },
  time: { marginLeft: 'auto', fontSize: 12, color: '#777' },
  msg: { margin: '8px 0 0', lineHeight: 1.5 },
  textarea: {
    width: '100%',
    padding: 10,
    fontSize: 15,
    border: '1px solid #dcdcdc',
    borderRadius: 8,
    resize: 'vertical',
    outline: 'none',
    boxSizing: 'border-box',
  },
  button: {
    marginTop: 12,
    width: '100%',
    padding: '12px 16px',
    fontSize: 15,
    fontWeight: 600,
    border: '1px solid #2f7ed8',
    background: '#2f7ed8',
    color: '#fff',
    borderRadius: 8,
    cursor: 'pointer',
  },
};

export default ConsultationMessenger;
