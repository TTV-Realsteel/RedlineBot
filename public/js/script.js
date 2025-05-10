// Check if dark mode is saved and apply it on page load
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
  }
  
  // Toggle Dark Mode when button clicked
  function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    
    // Store the current theme in localStorage
    const mode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', mode);
  }
  
  // Update the username on all pages (optional, if you have a username display)
  document.addEventListener('DOMContentLoaded', () => {
    const usernameLabel = document.getElementById('usernameLabel');
    const storedUsername = localStorage.getItem('username') || 'Guest';
    if (usernameLabel) {
      usernameLabel.textContent = `Logged in as: ${storedUsername}`;
    }
  });
  
  // Logout function
  function logout() {
    localStorage.removeItem('username');
    window.location.href = 'login.html';
  }
  