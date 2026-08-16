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
const submitButton = contactForm?.querySelector('button[type="submit"]');
const defaultSubmitText = submitButton?.textContent || "Отправить заявку";

function setFormStatus(message, state = "") {
  if (!formNote) return;

  formNote.textContent = message;
  formNote.classList.remove("is-success", "is-error");
  if (state) formNote.classList.add(`is-${state}`);
}

contactForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const data = new FormData(contactForm);
  const requesterName = String(data.get("name") || "Новый запрос").trim();
  data.set("subject", `Заявка North Refresh — ${requesterName}`);

  if (submitButton) {
    submitButton.disabled = true;
    submitButton.textContent = "Отправляем…";
  }
  setFormStatus("Отправляем заявку…");

  try {
    const response = await fetch(contactForm.action, {
      method: "POST",
      body: data,
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Formspree returned ${response.status}`);
    }

    contactForm.reset();
    setPeople(12);
    setFormStatus("Заявка отправлена. Мы свяжемся с вами в течение рабочего дня.", "success");
    if (submitButton) submitButton.textContent = "Заявка отправлена";
  } catch (error) {
    console.error("Form submission failed", error);
    setFormStatus("Не удалось отправить заявку. Попробуйте ещё раз или напишите на hello@northrefresh.ru.", "error");
    if (submitButton) submitButton.textContent = "Повторить отправку";
  } finally {
    if (submitButton) {
      submitButton.disabled = false;
      window.setTimeout(() => {
        submitButton.textContent = defaultSubmitText;
      }, 4000);
    }
  }
});
