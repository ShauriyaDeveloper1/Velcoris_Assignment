const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
if (toggle && nav) toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  toggle.setAttribute('aria-expanded', String(open));
});
const form = document.querySelector('#enquiry-form');
if (form) form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = form.querySelector('button[type="submit"]');
  const status = document.querySelector('#form-message');
  button.disabled = true; button.textContent = 'Sending…'; status.textContent = '';
  try {
    let response = await fetch('/api/enquiries', { method: 'POST', body: new FormData(form), headers: {'Accept':'application/json'} });
    let text = await response.text();
    let result = {};
    try {
      result = JSON.parse(text);
    } catch (parseErr) {
      // Fallback in case of serverless rewrite route mismatch
      response = await fetch('/', { method: 'POST', body: new FormData(form), headers: {'Accept':'application/json'} });
      text = await response.text();
      result = JSON.parse(text);
    }

    if (!response.ok) {
      throw new Error(Object.values(result.errors || {}).join(' ') || result.message || 'Unable to send enquiry.');
    }
    form.reset();
    status.innerHTML = `<strong>${result.message}</strong><br><a href="/admin/login" class="view-admin-link">→ Open Admin Portal to view your query in database ↗</a>`;
    status.className = 'form-note success-message';
  } catch (error) {
    status.textContent = error.message || 'Something went wrong. Please try again.';
    status.className = 'form-note error-message';
  } finally {
    button.disabled = false;
    button.innerHTML = 'Send enquiry <span>↗</span>';
  }
});
