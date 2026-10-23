export function createPendingCapture({fs,base,rows}) {
 return async function capture(tab,row) {
  const key=row.question_id+'-'+row.theme+'-'+row.font_scale;
  const out=base+'/11D4/captures';
  const diagnostics=base+'/11D4/scroll-capture-diagnostics';
  await fs.mkdir(diagnostics,{recursive:true});
  const url='http://127.0.0.1:51109/#'+row.question_id+'/accepted-replacements/'+row.theme+'/'+row.font_scale;
  if(await tab.url()!==url)await tab.goto(url);
  await tab.reload();
  await tab.playwright.getByText('Exact question images ready',{exact:true}).waitFor({state:'visible',timeoutMs:20000});
  // Native accessibility actions can activate off-screen options. Capture only
  // once the first option has a visible rendered rectangle near its top.
  for(let n=0;n<8;n++){
   const rect=await tab.playwright.evaluate(()=>{const e=document.body.shadowRoot.querySelector('#cmp_a11y_root [role="radio"]');const r=e.getBoundingClientRect();return {y:r.y,h:r.height};});
   if(rect.h>=35 && rect.y>120)break;
   await tab.scroll([195,700],'down',0.05);await tab.getAXState({emit:false});
   if(n===7)throw Error('Selected card not visible '+key);
  }
  let ax=await tab.getAXState({disableDiffing:true,emit:false});
  if(!ax.includes('(disabled) Confirm answer'))throw Error('Pre-answer confirmation enabled: '+key);
  for(const suffix of ['pre-answer','pending']) {
   const file=key+'-'+suffix+'.png';
   await fs.copyFile(out+'/'+file,diagnostics+'/'+file);
  }
  await fs.writeFile(out+'/'+key+'-pre-answer.png',await tab.screenshot({fullPage:false}));
  const radio=ax.split('\n').find(l=>/\d+ radio button/.test(l));
  await tab.click(Number(radio.trim().split(' ')[0]));
  ax=await tab.getAXState({disableDiffing:true,emit:false});
  const selected=await tab.playwright.evaluate(()=>Array.from(document.body.shadowRoot.querySelectorAll('#cmp_a11y_root [role="radio"]')).map(e=>e.getAttribute('aria-checked')));
  if(selected[0]!=='true'||selected.filter(x=>x==='true').length!==1||ax.includes('Correct answer'))throw Error('Pending state '+key);
  await fs.writeFile(out+'/'+key+'-pending.png',await tab.screenshot({fullPage:false}));
  row.capture_position='first rendered radio visible before selection';
  row.pending_capture_revalidated=true;
  await fs.writeFile(out+'/rows.json',JSON.stringify(rows,null,2));
  return key;
 };
}
