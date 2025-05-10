async function loadLogs() {
  const res = await fetch('/logs');
  const data = await res.json();
  const container = document.getElementById("logs");

  container.innerHTML = '';
  data.forEach(log => {
    const entry = document.createElement('div');
    entry.classList.add('dashboard-card');
    entry.innerHTML = `
      <strong>[${log.type}]</strong> ${log.user} - ${log.message}
      ${log.old_message ? `<br><em>Old:</em> ${log.old_message} <br><em>New:</em> ${log.new_message}` : ''}
      <hr>`;
    container.appendChild(entry);
  });
}

loadLogs();
