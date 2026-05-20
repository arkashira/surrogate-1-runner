const inputEl = document.getElementById('input');
const outputEl = document.getElementById('output');

/* ---------- Utility ---------- */
function append(text, { color = 'var(--success)', isPrompt = false } = {}) {
  const el = document.createElement('div');
  el.textContent = text;
  el.style.color = color;
  if (isPrompt) el.style.color = 'var(--prompt)';
  outputEl.appendChild(el);
  outputEl.scrollTop = outputEl.scrollHeight;
}

/* ---------- Client‑side simulator ---------- */
async function simulate(cmd) {
  const parts = cmd.trim().split(/\s+/);
  const command = parts[0];
  const args = parts.slice(1);

  switch (command) {
    case 'ls':
      return 'file1.txt\nfile2.txt\nfolder1\n';
    case 'cd':
      return `Changed directory to ${args[0] || '~'}\n`;
    case 'mkdir':
      return `Created directory ${args[0]}\n`;
    case 'echo':
      return args.join(' ') + '\n';
    case '':
      return '';
    default:
      return `bash: ${command}: command not found\n`;
  }
}

/* ---------- Server‑side execution ---------- */
async function runOnServer(cmd) {
  const resp = await fetch('/shell', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command: cmd })
  });

  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const data = await resp.json();          // Expected { output: string }
  return data.output;
}

/* ---------- Main command handler ---------- */
async function handleCommand(cmd) {
  append(`$ ${cmd}`, { isPrompt: true });

  try {
    const output = await runOnServer(cmd);
    append(output.trimEnd());
  } catch (e) {
    // If server fails, fall back to the simulator
    console.warn('Server error, falling back to client simulation:', e);
    const output = await simulate(cmd);
    append(output.trimEnd(), { color: 'var(--error)' });
  }
}

/* ---------- Event listener ---------- */
inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    const cmd = inputEl.value.trim();
    if (cmd) {
      handleCommand(cmd);
      inputEl.value = '';
    }
  }
});