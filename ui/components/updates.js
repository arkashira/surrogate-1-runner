export function initSecurityUpdates(containerId = 'security-updates') {
  const container = document.getElementById(containerId);
  if (!container) return;

  // Header
  const header = document.createElement('h2');
  header.textContent = 'Security & Compliance Updates';
  container.appendChild(header);

  // Updates list
  const list = document.createElement('ul');
  list.id = 'updates-list';
  container.appendChild(list);

  // Preferences button
  const prefsBtn = document.createElement('button');
  prefsBtn.id = 'prefs-button';
  prefsBtn.textContent = 'Notification Preferences';
  container.appendChild(prefsBtn);

  // Preferences modal (hidden by default)
  const prefsModal = document.createElement('div');
  prefsModal.id = 'prefs-modal';
  prefsModal.className = 'modal hidden';
  prefsModal.innerHTML = `
    <div class="modal-content">
      <span class="close">&times;</span>
      <h3>Notification Preferences</h3>
      <form id="prefs-form">
        <label><input type="checkbox" name="email"> Email</label><br>
        <label><input type="checkbox" name="sms"> SMS</label><br>
        <label><input type="checkbox" name="push"> Push Notification</label><br>
        <button type="submit">Save</button>
      </form>
    </div>
  `;
  document.body.appendChild(prefsModal);

  // Load saved preferences
  const savedPrefs = JSON.parse(localStorage.getItem('securityPrefs') || '{}');
  const form = prefsModal.querySelector('#prefs-form');
  ['email', 'sms', 'push'].forEach(key => {
    const input = form.querySelector(`input[name="${key}"]`);
    if (input) input.checked = !!savedPrefs[key];
  });

  // Event listeners
  prefsBtn.addEventListener('click', () => {
    prefsModal.classList.remove('hidden');
  });

  prefsModal.querySelector('.close').addEventListener('click', () => {
    prefsModal.classList.add('hidden');
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    const newPrefs = {
      email: form.email.checked,
      sms: form.sms.checked,
      push: form.push.checked,
    };
    localStorage.setItem('securityPrefs', JSON.stringify(newPrefs));
    prefsModal.classList.add('hidden');
  });

  // Fetch and render updates
  fetch('/api/security-updates')
    .then(r => {
      if (!r.ok) throw new Error('Network response was not ok');
      return r.json();
    })
    .then(data => {
      // Expected format: [{title, description, date, severity}]
      data.forEach(item => {
        const li = document.createElement('li');
        li.className = `update-item severity-${item.severity || 'info'}`;
        li.innerHTML = `
          <strong>${item.title}</strong> <em>${new Date(item.date).toLocaleDateString()}</em>
          <p>${item.description}</p>
        `;
        list.appendChild(li);
      });
    })
    .catch(err => {
      const errLi = document.createElement('li');
      errLi.textContent = 'Unable to load security updates.';
      list.appendChild(errLi);
      console.error(err);
    });
}