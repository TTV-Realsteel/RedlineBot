// Dark mode toggle
const toggle = document.getElementById('darkModeToggle');
toggle.addEventListener('change', () => {
  document.body.classList.toggle('dark-mode', toggle.checked);
  localStorage.setItem('darkMode', toggle.checked);
});

// Apply dark mode if saved
if (localStorage.getItem('darkMode') === 'true') {
  toggle.checked = true;
  document.body.classList.add('dark-mode');
}

// Load username
const storedUsername = localStorage.getItem('username') || 'Guest';
document.getElementById('usernameLabel').textContent = `Logged in as: ${storedUsername}`;

// Logout button
function logout() {
  localStorage.removeItem('username');
  localStorage.removeItem('darkMode');
  window.location.href = 'login.html';
}
