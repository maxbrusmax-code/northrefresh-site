const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const code = fs.readFileSync('site.js','utf8');
function setup({calculator=true,response={ok:true,json:async()=>({ok:true})},failure=null}={}) {
 const listeners={};let sent=null;let reset=0;
 const cls={add(){},remove(){},toggle(){},contains(){return false;}};
 const participant={value:''};const person={textContent:''};const total={textContent:''};
 const buttons=calculator?[12,15,18,24].map(n=>({dataset:{people:String(n)},classList:cls,setAttribute(){},addEventListener(){}})):[];
 const submit={textContent:'Отправить заявку',disabled:false};const note={textContent:'',classList:cls};
 const form={action:'https://formspree.io/f/moeangbe',querySelector:()=>submit,reportValidity:()=>true,addEventListener:(name,fn)=>listeners[name]=fn,reset:()=>{reset++;participant.value='';}};
 const values={'#participants':calculator?participant:null,'[data-price-person]':calculator?person:null,'[data-price-total]':calculator?total:null,'#contact-form':form,'#form-note':note};
 const context={Intl,FormData:class extends Map {constructor(){super([['name','Test']]);}},AbortController,Error,console:{error(){}},document:{querySelector:s=>values[s]||null,querySelectorAll:()=>buttons,addEventListener(){},body:{classList:cls}},window:{location:{origin:'https://northrefresh.ru',pathname:'/'},setTimeout:()=>1,clearTimeout(){},addEventListener(){}},fetch:async(url,opts)=>{sent=opts;if(failure)throw failure;return response;}};
 vm.createContext(context);vm.runInContext(code,context);
 return {context,participant,person,total,note,submit,listeners,getSent:()=>sent,getReset:()=>reset};
}
(async()=>{
 const c=setup();for(const n of [12,15,18,24]){vm.runInContext(`setPeople(${n})`,c.context);assert.equal(c.participant.value,String(n));assert.ok(c.person.textContent.length);}
 assert.match(c.total.textContent,/1.*920.*000/);
 await c.listeners.submit({preventDefault(){}});assert.equal(c.getReset(),1);assert.match(c.note.textContent,/Сервис принял/);assert.equal(c.submit.disabled,false);assert.equal(c.getSent().body.get('page'),'https://northrefresh.ru/');
 const rejected=setup({response:{ok:false,status:422,json:async()=>({errors:[{message:'Invalid email'}]})}});await rejected.listeners.submit({preventDefault(){}});assert.equal(rejected.getReset(),0);assert.match(rejected.note.textContent,/Invalid email/);assert.equal(rejected.submit.disabled,false);
 const network=setup({failure:new Error('Failed to fetch')});await network.listeners.submit({preventDefault(){}});assert.equal(network.getReset(),0);assert.match(network.note.textContent,/соединиться/);
 const uncertain=setup({response:{ok:true,json:async()=>({})}});await uncertain.listeners.submit({preventDefault(){}});assert.equal(uncertain.getReset(),0);assert.match(uncertain.note.textContent,/не подтвердил/);
 setup({calculator:false});
 console.log('PASS: all 4 group sizes, successful acknowledgement, rejection, network failure, unconfirmed response, shared script without calculator. Mocked transport; no real submissions sent.');
})();
