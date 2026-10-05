"""Build dependency-free GitHub Pages pages from shared components."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
VERSION = '20261005-team-session'
NAV = [('/#result', 'Результат'), ('/kak-my-rabotaem/', 'Как работаем'), ('/programma/', 'Программа'), ('/podbor-eksperta/', 'Эксперт'), ('/#price', 'Бюджет')]

def header(path):
    links = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url == path else '')+f'>{name}</a>' for url, name in NAV)
    return f'''<a class="skip-link" href="#content">Перейти к содержанию</a>
<header class="site-header"><div class="container header-inner">
<a class="brand" href="/" aria-label="North Refresh — главная"><span class="brand-mark" aria-hidden="true">NR</span><span>North Refresh</span></a>
<nav id="site-nav" class="site-nav" aria-label="Основная навигация">{links}<a class="nav-contact" href="/kontakty/">Контакты</a></nav>
<a class="header-action" href="#contact">Обсудить задачу <span aria-hidden="true">↗</span></a>
<button class="menu-toggle" type="button" aria-controls="site-nav" aria-label="Открыть меню" aria-expanded="false"><span></span></button>
</div></header>'''

def footer():
    return '''<footer class="site-footer"><div class="container footer-grid">
<div><a class="brand" href="/"><span class="brand-mark" aria-hidden="true">NR</span><span>North Refresh</span></a><p>Выездные стратегические сессии <br>для собственников и управленческих команд.</p></div>
<nav aria-label="Навигация в подвале"><a href="/kak-my-rabotaem/">Как мы работаем</a><a href="/programma/">Программа и результаты</a><a href="/podbor-eksperta/">Подбор эксперта</a><a href="/kontakty/">Контакты</a></nav>
<div class="footer-contact"><a href="#contact">Обсудить задачу</a><p>Ленинградская область и Карелия. <br>Площадку выбираем под задачу команды.</p></div>
</div><div class="container footer-bottom"><span>© North Refresh, 2026</span><span>Подготовка · Сессия · План исполнения</span></div></footer>'''

def contact(compact=False):
    content = '''<section class="section contact-section" id="contact" aria-labelledby="contact-title"><div class="container contact-grid">
<div><p class="eyebrow light">Первый разговор</p><h2 id="contact-title">Обсудим задачу <br>вашей команды.</h2><p class="contact-lead">Расскажите, что нужно решить и кто участвует. Обсудим программу и подготовим предложение.</p></div>
<form id="contact-form" class="contact-form" action="https://formspree.io/f/moeangbe" method="post">
<h3>Оставьте контакт</h3><p class="form-intro">Свяжемся, чтобы обсудить задачу и формат работы.</p>
<div class="honeypot" aria-hidden="true"><label for="website">Оставьте это поле пустым</label><input id="website" name="_gotcha" type="text" tabindex="-1" autocomplete="off"></div>
<div class="form-row"><label for="name">Имя <span>*</span><input id="name" name="name" autocomplete="name" placeholder="Как к вам обращаться" required maxlength="120"></label><label for="company">Компания<input id="company" name="company" autocomplete="organization" placeholder="Название компании" maxlength="180"></label></div>
<label for="contact-detail">Email, телефон или Telegram <span>*</span><input id="contact-detail" name="contact" autocomplete="off" placeholder="Удобный способ связи" required minlength="5" maxlength="180" aria-describedby="contact-hint"></label><p class="field-hint" id="contact-hint">Достаточно одного контакта.</p>
<label for="task">Коротко о задаче <span class="optional">необязательно</span><textarea id="task" name="task" rows="3" placeholder="Что нужно обсудить или согласовать?" maxlength="4000"></textarea></label>
<p class="form-privacy">Контактные данные используем для ответа на запрос.</p>
<button class="button button-primary button-full" type="submit">Обсудить задачу <span aria-hidden="true">↗</span></button>
<p class="form-note" id="form-note" role="status" aria-live="polite">Обязательные поля — имя и контакт.</p>
<noscript><p class="form-note">После отправки откроется страница подтверждения заявки.</p></noscript>
</form></div></section>'''
    if compact:
        content = content.replace('Обсудим задачу <br>вашей команды.', 'Первый разговор')
    return content

def heading(kicker, title, lead=''):
    return f'<div class="section-heading"><p class="eyebrow">{kicker}</p><div><h2>{title}</h2>'+(f'<p class="section-lead">{lead}</p>' if lead else '')+'</div></div>'

def pagehero(kicker, title, lead, aside=''):
    return f'<section class="container page-hero"><p class="breadcrumb"><a href="/">Главная</a><span aria-hidden="true"> / </span>{kicker}</p><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="page-lead">{lead}</p><div class="hero-actions"><a class="button button-primary" href="#contact">Обсудить задачу <span aria-hidden="true">↗</span></a>{aside}</div></section>'

def write(path, title, description, content):
    schema = {'@context':'https://schema.org', '@graph':[{'@type':'Organization','@id':'https://northrefresh.ru/#organization','name':'North Refresh','url':'https://northrefresh.ru/'}, {'@type':'WebPage','name':title,'url':'https://northrefresh.ru'+path,'inLanguage':'ru-RU','publisher':{'@id':'https://northrefresh.ru/#organization'}}]}
    html = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | North Refresh</title><meta name="description" content="{description}"><meta name="theme-color" content="#173d31">
<link rel="canonical" href="https://northrefresh.ru{path}"><link rel="icon" href="/favicon.svg?v={VERSION}" type="image/svg+xml" sizes="any">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="North Refresh"><meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:url" content="https://northrefresh.ru{path}"><meta property="og:image" content="https://northrefresh.ru/north-real-fog.webp">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{description}"><meta name="twitter:image" content="https://northrefresh.ru/north-real-fog.webp">
<link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/cormorant-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/site.css?v={VERSION}"><script defer src="/site.js?v={VERSION}"></script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>
<body>{header(path)}<main id="content">{content}</main>{footer()}</body></html>'''
    dest = ROOT / path.strip('/') / 'index.html' if path != '/' else ROOT / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)

HOME = '''
<section class="container hero home-hero" id="top" aria-labelledby="hero-title">
<div class="hero-copy"><p class="eyebrow">North Refresh · для собственников, CEO и команд</p><h1 id="hero-title">Выездные стратегические сессии под задачу вашего бизнеса.</h1><p class="hero-lead">Готовим программу, подбираем эксперта и организуем выезд. Через групповую работу и разбор управленческих ситуаций команда осваивает инструменты управления, договаривается о решениях и планирует следующие шаги.</p><div class="hero-actions"><a class="button button-primary" href="#contact">Обсудить задачу</a><a class="text-link" href="#about">Как устроен продукт</a></div><p class="hero-note">Ленинградская область и Карелия · базовый формат — 3 дня</p></div>
<figure class="home-hero-image"><img src="/north-real-hero.webp" alt="Северное озеро и сосновый лес на закате" width="1200" height="1800" fetchpriority="high"></figure>
</section>
<section class="section home-about" id="about"><div class="container product-grid"><div><p class="eyebrow">Что такое North Refresh</p><h2>Сессия и весь выезд <br>в одном проекте.</h2><p class="section-lead">Три дня для работы команды в комфортной обстановке. Индивидуальная программа, эксперт, проживание, питание и время для общения вне рабочих встреч.</p><p>Эксперт работает с вашей задачей: взаимодействием руководителей, ответственностью, приоритетами или изменениями в компании. Продюсер организует выезд и координирует работу на месте.</p><a class="text-link" href="/kak-my-rabotaem/">Как организуем работу</a></div><div class="home-situations"><h3>Когда это нужно</h3><ul><li>У руководителей разные приоритеты, а ресурсы общие.</li><li>Важное решение откладывается от совещания к совещанию.</li><li>Задачи переходят между отделами без ответственного за результат.</li><li>Предстоят изменения, для которых нужен согласованный план.</li></ul></div></div></section>
<section class="section result-section" id="result"><div class="container">'''+heading('Результат для компании', 'С чем команда возвращается <br>в работу')+'''
<div class="result-grid"><article><h3>Приоритеты</h3><p>Какие задачи команда берёт в работу в первую очередь.</p></article><article><h3>Решения</h3><p>О чём договорились и что решили изменить.</p></article><article><h3>План действий</h3><p>Кто за что отвечает, что делает и к какому сроку.</p></article></div><div class="section-tail"><p>На своих задачах команда отрабатывает инструменты постановки целей, делегирования и обратной связи.</p><a class="text-link" href="/programma/">Пример работы с командой</a></div></div></section>
<section class="section" id="process"><div class="container">'''+heading('Как работаем', 'Как проходит работа.')+'''
<ol class="process-list"><li><span class="number">01</span><h3>Разбираем запрос</h3><p>Уточняем вопрос, участников и данные для решения.</p></li><li><span class="number">02</span><h3>Готовим сессию</h3><p>Согласуем специалиста, программу и ожидаемый результат.</p></li><li><span class="number">03</span><h3>Проводим выезд</h3><p>Эксперт проводит групповые упражнения и разбор ситуаций. Команда обсуждает решения.</p></li><li><span class="number">04</span><h3>Фиксируем действия</h3><p>Передаём итоги и план. По запросу проводим контрольные встречи.</p></li></ol><div class="section-tail"><p>Задачу, специалиста, программу и состав результатов согласуем с вами до выезда.</p><a class="text-link" href="/podbor-eksperta/">Как выбираем эксперта</a></div></div></section>
<section class="section budget-section home-budget" id="price"><div class="container budget-grid"><div><p class="eyebrow">Формат и стоимость</p><h2>Премиальный выезд <br>для вашей команды</h2><p class="section-lead">Индивидуальная программа и эксперт, площадка с отдельным пространством для сессий, комфортное проживание и питание. Продюсер координирует весь проект.</p><a class="text-link" href="/kak-my-rabotaem/#scope">Состав проекта</a><img class="budget-landscape" src="/north-real-fog.webp" alt="Туман над лесом и озером на Севере" loading="lazy" width="1200" height="800"></div><div class="budget-card"><p class="eyebrow">Стоимость участия</p><strong class="budget-number participant-price"><span class="price-from">от</span> 80 000 <span class="price-unit">₽ / участника</span></strong><p class="budget-base">3 дня · 2 ночи · 12–24 участника</p><div class="budget-divider"></div><p class="project-total">Ориентир за проект для команды из <strong>12–24 участников: 1,44–1,92 млн ₽.</strong> Три дня, две ночи.</p><p>Стоимость за участника зависит от размера команды, программы и площадки.</p><p>Транспорт и сопровождение после выезда рассчитываются отдельно. Договор с перевозчиком заказчик оформляет напрямую.</p><p class="small-note">Для небольшой команды или другой длительности — индивидуальный расчёт.</p><a class="button button-primary button-full" href="#contact">Обсудить задачу и бюджет</a></div></div></section>
<section class="section faq-section" id="faq"><div class="container faq-grid"><div><p class="eyebrow">Перед первым разговором</p><h2>Четыре вопроса <br>о работе с нами.</h2></div><div class="faq-list">
<details><summary>Можно приехать небольшой командой?</summary><p>Да. Состав зависит от того, кто принимает и исполняет решения. Для команды меньше 12 человек подготовим отдельную программу и смету.</p></details>
<details><summary>Кто работает с командой?</summary><p>После разбора задачи предложим эксперта. Его опыт, подход и роль согласуем с вами до подтверждения программы.</p></details>
<details><summary>Как работать с конфиденциальными данными?</summary><p>До передачи материалов согласуем условия конфиденциальности, доступ к данным и порядок фиксации и хранения результатов.</p></details>
<details><summary>Что происходит после выезда?</summary><p>Передаём итоговые материалы. При необходимости согласуем контрольные встречи, чтобы разобрать выполнение плана и препятствия. Объём и стоимость сопровождения указываем отдельно.</p></details>
</div></div></section>'''+contact()

PROCESS = pagehero('Как мы работаем', 'От запроса собственника <br>до плана исполнения', 'Согласуем задачу и ожидаемый результат до выезда. Подготовка, эксперт и программа должны соответствовать вопросу, который предстоит решить.')+'''
<section class="section section-topless"><div class="container steps-detail">
<article><div><span class="number">01 / ДИАГНОСТИКА</span><h2>Определить задачу</h2></div><div><p>На первой встрече обсудим задачу компании, состав команды и ожидаемый результат. На этой основе предложим программу и площадку.</p><ul><li>Ожидаемый результат и границы вопроса.</li><li>Участники, их полномочия и разные позиции.</li><li>Исходные данные и ограничения по ресурсам.</li></ul><p class="step-output"><strong>На выходе:</strong> задача сессии и список материалов для подготовки.</p></div></article>
<article><div><span class="number">02 / ПРОЕКТИРОВАНИЕ</span><h2>Собрать программу</h2></div><div><p>Подбираем эксперта под задачу команды. Предлагаем групповые упражнения и разборы ситуаций, которые помогут команде проработать задачу.</p><p>Длительность определяется задачей. Базовый выезд — три дня и две ночи; для другого состава команды и объёма работы делаем отдельный расчёт.</p><p class="step-output"><strong>На выходе:</strong> кандидат специалиста, программа, состав результатов и предварительная смета.</p><a class="text-link" href="/podbor-eksperta/">Порядок подбора эксперта <span aria-hidden="true">→</span></a></div></article>
<article><div><span class="number">03 / ПОДГОТОВКА</span><h2>Подготовить команду</h2></div><div><p>Согласуем необходимые интервью, материалы и данные компании. Уточняем вопросы, по которым позиции участников различаются, и правила работы с конфиденциальной информацией.</p><p>Продюсер параллельно согласует площадку, размещение, питание и график. Все включённые услуги и доплаты отражаются в предложении.</p><p class="step-output"><strong>На выходе:</strong> материалы для сессии, подробная программа и подтверждённые организационные условия.</p></div></article>
<article><div><span class="number">04 / СЕССИЯ</span><h2>Принять решения</h2></div><div><p>Эксперт проводит групповые упражнения, разбор управленческих ситуаций и совместное обсуждение. Участники пробуют инструменты управления на своих задачах и фиксируют договорённости.</p><p>Обсуждаем, что изменить в работе команды, кто отвечает за первые шаги и как отслеживать их выполнение.</p><p class="step-output"><strong>На выходе:</strong> выбранные приоритеты, протокол решений и план действий.</p></div></article>
<article><div><span class="number">05 / ПОСЛЕ ВЫЕЗДА</span><h2>Проверить исполнение</h2></div><div><p>Оформляем и передаём итоговые материалы. При согласованном сопровождении проводим контрольные встречи: проверяем первые действия, обсуждаем препятствия и обновляем план.</p><p>Количество встреч, период сопровождения, состав участников и стоимость определяются в предложении. </p><p class="step-output"><strong>На выходе:</strong> обновлённый план и график контрольных встреч.</p></div></article>
</div></section>
<section class="section result-section" id="scope"><div class="container">'''+heading('Состав проекта', 'Что согласуем <br>до подтверждения')+'''
<div class="scope-grid"><article><h3>Содержательная работа</h3><ul><li>Диагностика запроса и объём подготовки.</li><li>Программа и эксперт по задаче команды.</li><li>Проведение рабочих сессий.</li><li>Протокол решений и план исполнения.</li><li>Состав и бюджет последующего сопровождения.</li></ul></article><article><h3>Организация выезда</h3><ul><li>Площадка и закрытое рабочее пространство.</li><li>Проживание и тип размещения.</li><li>Питание и перерывы между сессиями.</li><li>Материалы, оборудование и координация.</li><li>Время прибытия и условия дополнительных услуг.</li></ul></article></div><div class="scope-note"><strong>Транспорт — отдельный договор.</strong><p>Помогаем выбрать перевозчика и согласовать расписание. Заказчик заключает договор и оплачивает перевозку напрямую. Дополнительные ночи, одноместное размещение и другие услуги указываем в смете; их состав зависит от выбранной комплектации.</p></div></div></section>
<section class="section"><div class="container responsibility-grid"><div><p class="eyebrow">Ответственность</p><h2>У каждой части <br>есть ответственный</h2></div><div><article><h3>Продюсер North Refresh</h3><p>Координирует проект, площадку, подрядчиков и организационные условия. Держит единый график подготовки и проведения.</p></article><article><h3>Эксперт стратегической сессии</h3><p>Готовит программу, проводит групповые упражнения и разборы ситуаций. Помогает команде освоить инструменты управления и оформить договорённости.</p></article><article><h3>Заказчик и управленческая команда</h3><p>Предоставляют исходные данные, принимают решения в рамках своих полномочий и выполняют согласованный план.</p></article></div></div></section>'''+contact()

EXPERT = pagehero('Подбор эксперта', 'Эксперт для задачи <br>вашей команды', 'Подбираем эксперта с опытом работы по вашему запросу. До сессии знакомим с его подходом и согласуем программу.')+'''
<section class="section section-topless"><div class="container">'''+heading('Эксперты North Refresh', 'Кого подбираем <br>для вашей команды')+'''
<div class="expert-topics expert-profiles">
<article><h3>Эксперт по управлению командой</h3><p>Помогает руководителям выстроить постановку задач, делегирование и контроль.</p><p><strong>Задачи:</strong> снять зависимость от постоянного участия руководителя, распределить ответственность, договориться о правилах работы.</p></article>
<article><h3>Эксперт по групповой динамике</h3><p>Работает с тем, как участники взаимодействуют, договариваются и принимают решения.</p><p><strong>Задачи:</strong> разобрать разногласия, наладить работу между отделами, отработать совместное решение задач.</p></article>
<article><h3>Эксперт по развитию руководителей</h3><p>Разбирает управленческие ситуации участников и помогает отработать новые способы работы с людьми.</p><p><strong>Задачи:</strong> обратная связь, сложные разговоры, постановка ожиданий и взаимодействие собственника с руководителями.</p></article>
<article><h3>Эксперт по стратегическому планированию</h3><p>Помогает команде выбрать приоритеты и определить шаги развития компании.</p><p><strong>Задачи:</strong> согласовать направление, расставить приоритеты и перевести решения в план действий.</p></article>
<article><h3>Эксперт по организационным изменениям</h3><p>Работает с изменениями в структуре, ролях и управлении командой.</p><p><strong>Задачи:</strong> определить новые зоны ответственности, договориться о взаимодействии и подготовить команду к изменениям.</p></article>
</div></div></section>
<section class="section result-section"><div class="container">'''+heading('Как выбираем', 'Опыт на похожих задачах')+'''
<div class="expert-selection"><p>Смотрим на опыт работы с собственниками и руководителями, задачи прошлых проектов и методы работы с группой.</p><p>Показываем профиль эксперта, обсуждаем программу и организуем знакомство. Кандидатуру утверждаете вы.</p></div></div></section>'''+contact()

PROGRAM = pagehero('Программа и результаты', 'Как команда работает <br>на сессии', 'Пример задачи: руководители отделов по-разному понимают ответственность. Общие задачи задерживаются, собственнику приходится вмешиваться.')+'''
<section class="section section-topless"><div class="container">'''+heading('Пример программы', 'Разобрать взаимодействие <br>и договориться о работе')+'''
<p class="demo-label program-demo">Пример программы. Рабочие ситуации и упражнения подбираем под задачу компании.</p>
<div class="day-grid"><article><span class="number">ДЕНЬ 1</span><h3>Увидеть, где застревает работа</h3><p>Участники разбирают ситуацию, в которой задача потерялась между отделами. В групповом упражнении эксперт наблюдает, как команда распределяет роли и принимает решения.</p><div class="day-output"><strong>Итог</strong><p>Команда видит повторяющиеся проблемы во взаимодействии.</p></div></article><article><span class="number">ДЕНЬ 2</span><h3>Попробовать другой подход</h3><p>Эксперт предлагает инструменты постановки задач, делегирования и обратной связи. Участники пробуют их на своих ситуациях и обсуждают, что подходит команде.</p><div class="day-output"><strong>Итог</strong><p>Рабочие приёмы и договорённости о распределении ответственности.</p></div></article><article><span class="number">ДЕНЬ 3</span><h3>Выбрать первые изменения</h3><p>Команда определяет, что начнёт делать после возвращения: какие правила вводит, кто отвечает и когда обсуждает первые результаты.</p><div class="day-output"><strong>Итог</strong><p>Список решений и план действий с ответственными и сроками.</p></div></article></div>
<p class="small-note">В графике есть время на рабочие блоки, питание, перерывы и общение команды.</p></div></section>
<section class="section result-section" id="roadmap"><div class="container">'''+heading('После сессии', 'Как договорённости <br>переходят в работу')+'''
<div class="management-example"><p class="demo-label">Иллюстрация для этой задачи</p><h3>Общие задачи между отделами</h3><p>Команда договаривается: у каждой общей задачи есть один ответственный. Он фиксирует следующий шаг и срок, а на еженедельной встрече сообщает о ходе работы.</p><dl><div><dt>Первый шаг</dt><dd>Выбрать одну текущую задачу и применить новый порядок.</dd></div><div><dt>Ответственный</dt><dd>Руководитель, которого назначила команда.</dd></div><div><dt>Проверка</dt><dd>На следующей встрече разобрать, что сработало и где нужна корректировка.</dd></div></dl></div>
<div class="section-tail"><p>План на следующие 90 дней команда составляет по своим задачам. Контрольные встречи с экспертом можно включить в сопровождение.</p><a class="text-link" href="/kak-my-rabotaem/">Подготовка и сопровождение</a></div></div></section>'''+contact()

CONTACTS = '<section class="container page-hero contact-page-hero"><p class="breadcrumb"><a href="/">Главная</a> / Контакты</p><h1>Обсудить задачу.</h1></section>'+contact(compact=True)

write('/', 'Выездные стратегические сессии для собственников и команд', 'North Refresh: диагностика задачи, подбор эксперта, организация выездной сессии и план на 90 дней с ответственными, сроками и метриками.', HOME)
write('/kak-my-rabotaem/', 'Как мы готовим и проводим стратегическую сессию', 'Диагностика, программа, эксперт, подготовка команды, проведение и сопровождение. Состав работы и ответственность North Refresh.', PROCESS)
write('/podbor-eksperta/', 'Подбор эксперта для управленческой команды', 'Эксперты по управлению, командному взаимодействию, лидерству и изменениям. Примеры задач и порядок подбора North Refresh.', EXPERT)
write('/programma/', 'Программа стратегической сессии и работа с командой', 'Групповые упражнения, управленческие инструменты и план действий. Пример трёхдневной работы с командой North Refresh.', PROGRAM)
write('/kontakty/', 'Обсудить задачу управленческой команды', 'Свяжитесь с North Refresh для обсуждения выездной стратегической сессии. Задача, ожидаемые результаты, состав команды и бюджет.', CONTACTS)

# Legacy routes retain inbound links without retaining the previous product copy.
for path, target in [('/korporativnyy-retrit/', '/'), ('/strategicheskaya-sessiya/', '/')]:
    dest = ROOT / path.strip('/') / 'index.html'
    dest.write_text(f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>North Refresh — стратегические сессии</title><link rel="canonical" href="https://northrefresh.ru{target}"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url={target}"></head><body><p>Страница обновлена. <a href="{target}">Перейти на сайт North Refresh</a></p></body></html>''')

notfound = pagehero('Страница не найдена', 'Вернёмся <br>к вашей задаче.', 'Возможно, адрес изменился. На главной странице — продукт, процесс работы и способы связи.', '<a class="text-link" href="/">На главную <span aria-hidden="true">→</span></a>')
write('/404/', 'Страница не найдена', 'Перейти на главную страницу North Refresh.', notfound)
(ROOT/'404.html').write_text((ROOT/'404/index.html').read_text())
urls = ['/', '/kak-my-rabotaem/', '/podbor-eksperta/', '/programma/', '/kontakty/']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>https://northrefresh.ru{p}</loc></url>\n' for p in urls)+'</urlset>\n')
print('Built 5 pages, 2 legacy redirects and 404; updated sitemap.')
