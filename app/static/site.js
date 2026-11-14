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
    const response = await fetch('/api/enquiries', { method: 'POST', body: new FormData(form), headers: {'Accept':'application/json'} });
    const result = await response.json();
    if (!response.ok) throw new Error(Object.values(result.errors || {}).join(' ' ) || result.message || 'Unable to send enquiry.');
    form.reset(); status.textContent = result.message; status.className = 'form-note success-message';
  } catch (error) {
    status.textContent = error.message || 'Something went wrong. Please try again.'; status.className = 'form-note error-message';
  } finally { button.disabled = false; button.innerHTML = 'Send enquiry <span>↗</span>'; }
});
