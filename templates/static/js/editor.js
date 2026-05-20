
/**
 * Lightweight template editor.
 *
 * Features:
 *   • GET /api/templates/<id>/   → {id, name, content, version}
 *   • POST /api/templates/<id>/  → {version}
 *
 * The server must inject `window.TEMPLATE_ID` in the page.
 */

document.addEventListener('DOMContentLoaded', () => {
  const id = window.TEMPLATE_ID;
  const form = document.getElementById('template-form');
  const status = document.getElementById('status');

  // Helper: show a message
  const setStatus = (msg, type = 'info') => {
    status.textContent = msg;
    status.className = type;          // 'info', 'success', 'error'
  };

  // Load the current template
  const load = async () => {
    try {
      const res = await fetch(`/api/templates/${id}/`);
      if (!res.ok) throw new Error(`Load failed: ${res.statusText}`);
      const data = await res.json();
      form.elements.name.value = data.name;
      form.elements.content.value = data.content;
      form.dataset.version = data.version;   // store current version
      setStatus('Template loaded.', 'info');
    } catch (e) {
      setStatus(e.message, 'error');
    }
  };

  // Save the edited template
  const save = async (e) => {
    e.preventDefault();
    setStatus('Saving…', 'info');

    const payload = {
      name: form.elements.name.value,
      content: form.elements.content.value,
      version: Number(form.dataset.version),
    };

    try {
      const res = await fetch(`/api/templates/${id}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.status === 409) {
        throw new Error('Version conflict – please reload and try again.');
      }
      if (!res.ok) throw new Error(`Save failed: ${res.statusText}`);

      const data = await res.json();
      form.dataset.version = data.version;   // bump to new version
      setStatus('Template saved successfully.', 'success');
    } catch (e) {
      setStatus(e.message, 'error');
    }
  };

  form.addEventListener('submit', save);
  load();
});