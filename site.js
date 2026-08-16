const priceMap = {
  12: { perPerson: 120000, total: 1440000 },
  15: { perPerson: 100000, total: 1500000 },
  18: { perPerson: 90000, total: 1620000 },
  24: { perPerson: 80000, total: 1920000 },
};

const money = new Intl.NumberFormat("ru-RU", {
  style: "currency",
  currency: "RUB",
  maximumFractionDigits: 0,
});

const peopleOptions = document.querySelectorAll("[data-people]");
const perPersonOutput = document.querySelector("[data-price-person]");
const totalOutput = document.querySelector("[data-price-total]");
const participantsField = document.querySelector("#participants");

function setPeople(count) {
  const price = priceMap[count];
  if (!price) return;

  peopleOptions.forEach((option) => {
    const active = Number(option.dataset.people) === count;
    option.classList.toggle("active", active);
    option.setAttribute("aria-pressed", String(active));
  });

  perPersonOutput.textContent = money.format(price.perPerson);
  totalOutput.textContent = money.format(price.total);

  if (participantsField && !participantsField.value) {
    participantsField.value = String(count);
  }
}

peopleOptions.forEach((option) => {
  option.addEventListener("click", () => setPeople(Number(option.dataset.people)));
});

setPeople(12);

const menuToggle = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".site-nav");

function closeMenu() {
  menuToggle?.classList.remove("active");
  menuToggle?.setAttribute("aria-expanded", "false");
  navigation?.classList.remove("open");
  document.body.classList.remove("menu-open");
}

menuToggle?.addEventListener("click", () => {
  const open = !navigation.classList.contains("open");
  menuToggle.classList.toggle("active", open);
  menuToggle.setAttribute("aria-expanded", String(open));
  navigation.classList.toggle("open", open);
  document.body.classList.toggle("menu-open", open);
});

navigation?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", closeMenu);
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 760) closeMenu();
});

const contactForm = document.querySelector("#contact-form");
const formNote = document.querySelector("#form-note");

contactForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = new FormData(contactForm);
  const subject = `Заявка North Refresh — ${data.get("name") || "новый запрос"}`;
  const lines = [
    "Здравствуйте! Хочу обсудить ретрит North Refresh.",
    "",
    `Имя: ${data.get("name") || "—"}`,
    `Компания / проект: ${data.get("company") || "—"}`,
    `Формат: ${data.get("format") || "—"}`,
    `Количество участников: ${data.get("participants") || "—"}`,
    `Желаемые даты: ${data.get("dates") || "—"}`,
    `Телефон / Telegram / email: ${data.get("contact") || "—"}`,
    "",
    "Задача:",
    data.get("task") || "—",
  ];

  formNote.textContent = "Открываем ваше почтовое приложение с заполненной заявкой…";
  window.location.href = `mailto:hello@northrefresh.ru?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
});

document.querySelector("[data-copy-email]")?.addEventListener("click", async (event) => {
  event.preventDefault();
  const email = "hello@northrefresh.ru";

  try {
    await navigator.clipboard.writeText(email);
    event.currentTarget.textContent = "Email скопирован";
    setTimeout(() => {
      event.currentTarget.textContent = email;
    }, 1800);
  } catch {
    window.location.href = `mailto:${email}`;
  }
});
