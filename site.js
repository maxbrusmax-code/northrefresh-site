'use strict';
const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.site-nav');
function closeMenu() {
  menuToggle?.classList.remove('active');
  menuToggle?.setAttribute('aria-expanded', 'false');
  menuToggle?.setAttribute('aria-label', 'Открыть меню');
  navigation?.classList.remove('open');
  document.body.classList.remove('menu-open');
}
menuToggle?.addEventListener('click', () => {
  const open = !navigation.classList.contains('open');
  menuToggle.classList.toggle('active', open);
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
  navigation.classList.toggle('open', open);
  document.body.classList.toggle('menu-open', open);
});
navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.querySelector('.header-action')?.addEventListener('click', closeMenu);
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation?.classList.contains('open')) { closeMenu(); menuToggle?.focus(); }
  if (event.key === 'Tab' && navigation?.classList.contains('open')) {
    const items = [document.querySelector('.brand'), ...navigation.querySelectorAll('a'), document.querySelector('.header-action'), menuToggle].filter(Boolean);
    if (event.shiftKey && document.activeElement === items[0]) { event.preventDefault(); items.at(-1).focus(); }
    else if (!event.shiftKey && document.activeElement === items.at(-1)) { event.preventDefault(); items[0].focus(); }
  }
});
window.addEventListener('resize', () => { if (window.innerWidth > 900) closeMenu(); });
// Keep the campaign source while the visitor moves between pages. No form content
// or arbitrary query parameters are stored here; storage denial is non-blocking.
function readAttribution() {
  const key = 'northrefresh:source';
  const params = new URLSearchParams(window.location.search);
  const campaignKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  let saved = {};
  try { saved = JSON.parse(sessionStorage.getItem(key) || '{}') || {}; } catch (_) {}
  const campaign = {};
  campaignKeys.forEach(name => {
    const value = params.get(name)?.trim();
    if (value) campaign[name] = value.slice(0, 200);
  });
  if (!saved.landing_page || Object.keys(campaign).length) {
    let referrer = '';
    try {
      const source = new URL(document.referrer);
      if (source.origin !== window.location.origin) referrer = source.origin;
    } catch (_) {}
    saved = {landing_page: window.location.pathname, referrer, ...campaign};
    try { sessionStorage.setItem(key, JSON.stringify(saved)); } catch (_) {}
  }
  return saved;
}
const attribution = readAttribution();
// Events expose funnel stages without transmitting form content to analytics.
function track(name) {
  window.dispatchEvent(new CustomEvent(`northrefresh:${name}`, {detail: {page: window.location.pathname}}));
}
document.querySelectorAll('a[href$="#contact"]').forEach(link => link.addEventListener('click', () => track('contact_click')));
const form = document.querySelector('#contact-form');
const note = document.querySelector('#form-note');
const submitButton = form?.querySelector('button[type="submit"]');
let formStarted = false;
form?.addEventListener('input', () => { if (!formStarted) { formStarted = true; track('form_start'); } });
function setStatus(message, state = '') {
  if (!note) return;
  note.textContent = message;
  note.classList.remove('is-success', 'is-error');
  if (state) note.classList.add(`is-${state}`);
}
form?.addEventListener('submit', async event => {
  event.preventDefault();
  if (submitButton?.disabled || !form.reportValidity()) return;
  const data = new FormData(form);
  const contact = String(data.get('contact') || '').trim();
  const name = String(data.get('name') || '').trim();
  if (!name || !contact) { setStatus('Укажите имя и удобный контакт для связи.', 'error'); return; }
  data.set('name', name);
  data.set('contact', contact);
  data.set('page', window.location.origin + window.location.pathname);
  ['landing_page', 'referrer', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(key => {
    if (typeof attribution[key] === 'string' && attribution[key]) data.set(key, attribution[key].slice(0, 200));
  });
  data.set('subject', `Запрос North Refresh — ${name}`);
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact)) data.set('email', contact);
  submitButton.disabled = true;
  submitButton.textContent = 'Отправляем…';
  setStatus('Отправляем запрос…');
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 20000);
  try {
    const response = await fetch(form.action, {method:'POST', body:data, signal:controller.signal, headers:{Accept:'application/json'}});
    if (!response.ok) throw new Error('rejected');
    const result = await response.json();
    if (result.ok !== true) throw new Error('unconfirmed');
    form.reset();
    formStarted = false;
    track('form_success');
    setStatus('Запрос получен. Свяжемся по указанному контакту, чтобы обсудить задачу, состав команды и формат выезда.', 'success');
    submitButton.textContent = 'Запрос отправлен';
  } catch (error) {
    track('form_error');
    setStatus(error?.name === 'AbortError'
      ? 'Отправка заняла больше времени. Данные сохранены в форме. Попробуйте позже.'
      : 'Не удалось подтвердить отправку. Данные сохранены в форме. Попробуйте ещё раз.', 'error');
    submitButton.textContent = 'Повторить отправку';
  } finally { window.clearTimeout(timeout); submitButton.disabled = false; }
});
