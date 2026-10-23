export function createKeyboardRunner({fs,base}) {
 return async function(tab,theme,scale) {
  const key=theme+'-'+scale, out=base+'/11D4';
  const observe=()=>tab.getAXState({disableDiffing:true,emit:false});
  const click=async label=>{for(let i=0;i<12;i++){const ax=await observe();const l=ax.split('\n').find(l=>l.trim().replace(/^\d+ button /,'').replace(/\s+/g,' ')===label);if(l){await tab.click(Number(l.trim().split(' ')[0]));await observe();return;}await tab.playwright.domSnapshot();}throw Error('Missing '+label);};
  await tab.goto('http://127.0.0.1:51109/#sign-recognise-S1/accepted-replacements/'+theme+'/'+scale);await tab.reload();await tab.playwright.getByText('Exact question images ready',{exact:true}).waitFor({state:'visible',timeoutMs:20000});
  let ax=await observe();let radio=ax.split('\n').find(l=>/\d+ radio button/.test(l));await tab.click(Number(radio.trim().split(' ')[0]));await observe();await click('Enlarge option A image');await tab.playwright.getByText(/100%/).waitFor({state:'visible',timeoutMs:10000});
  await tab.click([180,420]);await observe();await tab.pressKey(null,'Tab');await observe();await tab.pressKey(null,'Tab');await observe();await tab.pressKey(null,'shift+Tab');await observe();await tab.pressKey(null,'Tab');await observe();
  await tab.pressKey(null,'=');await tab.playwright.getByText(/150%/).waitFor({state:'visible',timeoutMs:5000});ax=await observe();if(ax.includes('Next fixture')||ax.includes('Confirm answer'))throw Error('Background exposed');
  await fs.writeFile(out+'/keyboard-'+key+'-zoom.png',await tab.screenshot({fullPage:false}));await tab.pressKey(null,'Right');await observe();await fs.writeFile(out+'/keyboard-'+key+'-pan.png',await tab.screenshot({fullPage:false}));
  await tab.pressKey(null,'Home');await tab.playwright.getByText(/100%/).waitFor({state:'visible',timeoutMs:5000});await tab.pressKey(null,'Escape');await tab.playwright.getByRole('button',{name:'Close',exact:true}).waitFor({state:'hidden',timeoutMs:5000});ax=await observe();if(!/radio button .*Value: 1/.test(ax))throw Error('Selection lost');
  await tab.pressKey(null,'Return');await tab.playwright.getByText(/100%/).waitFor({state:'visible',timeoutMs:5000});ax=await observe();if(!ax.includes('Blue square with a white inset containing a red fire extinguisher.'))throw Error('Wrong restored trigger');
  await tab.pressKey(null,'Escape');await tab.playwright.getByRole('button',{name:'Close',exact:true}).waitFor({state:'hidden',timeoutMs:5000});await observe();await fs.writeFile(out+'/keyboard-'+key+'-return.png',await tab.screenshot({fullPage:false}));
  return {theme,font_scale:scale,question_id:'sign-recognise-S1',tab_and_reverse_tab_issued:true,keyboard_zoom150_reset100:true,keyboard_pan_capture:true,background_excluded:true,escape_and_return_reopens_exact_trigger:true,selection_retained:true};
 };
}
