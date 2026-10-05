/* Browser integration checks. Form submissions are intercepted, never sent. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const base = process.env.NR_BASE_URL || 'http://127.0.0.1:8000';
const out = process.env.NR_QA_DIR || '/tmp/northrefresh-qa';
const paths = ['/', '/kak-my-rabotaem/', '/podbor-eksperta/', '/programma/', '/kontakty/'];
const sizes = [{width:1440,height:1000},{width:1366,height:768},{width:1024,height:768},{width:768,height:1024},{width:390,height:844},{width:375,height:812},{width:320,height:740}];
(async()=>{
 fs.mkdirSync(out,{recursive:true});
 const bundled = process.env.NR_CHROMIUM_MODULE ? (await import(process.env.NR_CHROMIUM_MODULE)).default : null;
 const browser = await chromium.launch(bundled ? {headless:true, executablePath:await bundled.executablePath(), args:bundled.args} : {headless:true, ...(process.env.NR_CHROMIUM_PATH ? {executablePath:process.env.NR_CHROMIUM_PATH} : {})});
 const page = await browser.newPage();
 const errors=[]; page.on('pageerror',e=>errors.push(e.message));
 const broken=[];page.on('response',r=>{if(r.status()>=400 && r.url().startsWith(base))broken.push(r.url())});
 const links = new Set();
 for(const size of sizes){
  await page.setViewportSize(size);
  for(const path of paths){
   const response=await page.goto(base+path);assert.equal(response.status(),200);
   await page.evaluate(()=>document.fonts.ready);
   for(const image of await page.locator("img").all()){await image.scrollIntoViewIfNeeded();await image.evaluate(i=>i.complete ? null : new Promise(resolve=>{i.addEventListener("load",resolve,{once:true});i.addEventListener("error",resolve,{once:true})}));}
   await page.evaluate(()=>window.scrollTo({top:0,behavior:"instant"}));
   const state=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,h1:document.querySelectorAll('h1').length,text:document.body.innerText,links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),images:[...document.images].map(i=>i.complete&&i.naturalWidth>0)}));
   assert.equal(state.h1,1,path);assert.ok(state.scroll<=state.width+1,`Overflow ${path} at ${size.width}: ${state.scroll}`);
   assert.ok(!/ретрит|корпоратив|телесн|коуч|под вашим брендом/i.test(state.text),`Old positioning ${path}`);
   assert.ok(!/[↗→]/.test(state.text),`Arrow remains ${path}`);
   assert.ok(!state.text.includes('из Санкт-Петербурга'),`Restricted audience ${path}`);
   assert.ok(state.images.every(Boolean),`Images ${path}`);
   state.links.filter(x=>x.startsWith('/')||x.startsWith('#')).forEach(x=>links.add(new URL(x,base+path).href));
   if(size.width===1440||size.width===390)await page.screenshot({path:`${out}/${path==='/'?'home':path.split('/')[1]}-${size.width}.png`,fullPage:true});
  }
 }
 for(const url of links){await page.goto(url);const anchor=new URL(url).hash;if(anchor)assert.ok(await page.locator(anchor).count(),`Missing anchor ${url}`)}
 for(const path of ['/404/', '/404.html']) {
  await page.goto(base+path);
  assert.equal(await page.locator('meta[name="robots"]').getAttribute('content'), 'noindex,follow');
  assert.equal(await page.locator('a[href="#contact"]').count(), 0);
  assert.equal(await page.locator('a[href="/#contact"]').count(), 3);
 }
 for(const path of ['/korporativnyy-retrit/','/strategicheskaya-sessiya/']){await page.goto(base+path);await page.waitForURL(base+'/');}
 await page.setViewportSize({width:390,height:844});await page.goto(base+'/');
 await page.getByRole('button',{name:'Открыть меню'}).click();assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'true');
 await page.keyboard.press('Escape');assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'false');
 await page.getByRole('button',{name:'Открыть меню'}).click();await page.locator('.site-nav').getByRole('link',{name:'Как работаем',exact:true}).click();await page.waitForURL(base+'/kak-my-rabotaem/');assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'false');
 await page.goto(base+'/');await page.locator('.hero-actions').getByRole('link',{name:/Обсудить задачу/}).click();await page.waitForFunction(()=>document.querySelector('#contact').getBoundingClientRect().top<150);assert.ok(await page.locator('#contact-form').isVisible());
 await page.locator('summary').first().click();assert.equal(await page.locator('details').first().getAttribute('open'),'');
 let submission=null;
 await page.route('https://formspree.io/**',async route=>{submission=route.request().postData();await route.fulfill({status:200,contentType:'application/json',body:'{"ok":true}'})});
 await page.locator('#contact-form button').click();assert.equal(submission,null,'Empty form submitted');
 for(const path of paths){
  await page.goto(base+path);await page.locator('#name').fill('Тестовая проверка');await page.locator('#contact-detail').fill('qa@example.com');await page.locator('#task').fill('Автоматическая проверка, без реальной отправки.');await page.locator('#contact-form button').click();await page.waitForFunction(()=>document.querySelector('#form-note').classList.contains('is-success'));assert.ok(submission.includes('qa@example.com'));assert.equal(await page.locator('#name').inputValue(),'');
 }
 await page.goto(base+'/?utm_source=qa&utm_medium=test&utm_campaign=launch&unrelated=excluded');
 await page.getByRole('button',{name:'Открыть меню'}).click();
 await page.locator('.site-nav').getByRole('link',{name:'Эксперт',exact:true}).click();
 await page.waitForURL(base+'/podbor-eksperta/');
 await page.locator('#name').fill('Проверка источника');await page.locator('#contact-detail').fill('qa@example.com');
 await page.locator('#contact-form button').click();await page.waitForFunction(()=>document.querySelector('#form-note').classList.contains('is-success'));
 assert.ok(/name="utm_source"\r\n\r\nqa/.test(submission));
 assert.ok(/name="utm_campaign"\r\n\r\nlaunch/.test(submission));
 assert.ok(!submission.includes('unrelated'));
 await page.unroute('https://formspree.io/**');
 for(const reply of [{status:422,body:'{"errors":[{"message":"Rejected"}]}'},{status:200,body:'{}'}]){
  await page.route('https://formspree.io/**',route=>route.fulfill({status:reply.status,contentType:'application/json',body:reply.body}));
  await page.locator('#name').fill('Тест');await page.locator('#contact-detail').fill('@test_contact');await page.locator('#contact-form button').click();await page.waitForFunction(()=>document.querySelector('#form-note').classList.contains('is-error'));assert.equal(await page.locator('#name').inputValue(),'Тест');assert.equal(await page.locator('#contact-form button').isEnabled(),true);await page.unroute('https://formspree.io/**');
 }
 await page.route('https://formspree.io/**',route=>route.abort());await page.locator('#contact-form button').click();await page.waitForFunction(()=>document.querySelector('#form-note').classList.contains('is-error'));assert.equal(await page.locator('#name').inputValue(),'Тест');
 assert.deepEqual(errors,[]);assert.deepEqual(broken,[]);
 console.log(`PASS: 5 pages × 7 viewports, ${links.size} internal links/anchors, legacy redirects, mobile menu/Escape, CTA, FAQ, form validation/success/rejection/unconfirmed/network error. No real submissions.`);
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
