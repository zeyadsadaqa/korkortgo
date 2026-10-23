// Capture only this task's emulator playback; no host microphone or external service.
import fs from 'node:fs/promises';
import http2 from 'node:http2';
import path from 'node:path';

const [metadataFile,output,secondsText='15']=process.argv.slice(2);
const settings=Object.fromEntries((await fs.readFile(metadataFile,'utf8')).split('\n').filter(x=>x.includes('=')).map(x=>{const i=x.indexOf('=');return [x.slice(0,i),x.slice(i+1)];}));
if(settings['avd.id']!=='16_KB_test')throw Error('Refusing to record another emulator');
const seconds=Number(secondsText),pcm=[];
let buffer=Buffer.alloc(0),failure;
function varint(bytes,offset){let n=0,shift=0,b;do{b=bytes[offset++];n+=(b&127)*2**shift;shift+=7;}while(b&128);return [n,offset];}
function audioPayload(packet){let offset=0;while(offset<packet.length){let [tag,next]=varint(packet,offset);offset=next;const field=tag>>3,wire=tag&7;if(wire===2){let [length,start]=varint(packet,offset);if(field===3)return packet.subarray(start,start+length);offset=start+length;}else if(wire===0){[,offset]=varint(packet,offset);}else throw Error('Unexpected audio wire format');}return Buffer.alloc(0);}
const session=http2.connect('http://127.0.0.1:'+settings['grpc.port']);
const request=session.request({':method':'POST',':path':'/android.emulation.control.EmulatorController/streamAudio','content-type':'application/grpc','te':'trailers','authorization':'Bearer '+settings['grpc.token']});
request.on('response',headers=>{if(headers['grpc-status'] && headers['grpc-status']!=='0')failure=String(headers['grpc-message']||headers['grpc-status']);});
request.on('trailers',headers=>{if(headers['grpc-status'] && headers['grpc-status']!=='0')failure=String(headers['grpc-message']||headers['grpc-status']);});
request.on('data',chunk=>{buffer=Buffer.concat([buffer,chunk]);while(buffer.length>=5){const length=buffer.readUInt32BE(1);if(buffer.length<5+length)break;if(buffer[0]!==0)throw Error('Compressed audio unsupported');pcm.push(audioPayload(buffer.subarray(5,5+length)));buffer=buffer.subarray(5+length);}});
const format=Buffer.from([8,128,125,24,1]); // 16kHz, mono, signed little-endian16.
const framed=Buffer.alloc(5+format.length);framed.writeUInt32BE(format.length,1);format.copy(framed,5);request.end(framed);
await new Promise(resolve=>{const timer=setTimeout(resolve,seconds*1000);request.on('end',()=>{clearTimeout(timer);resolve();});request.on('error',error=>{failure=error.message;clearTimeout(timer);resolve();});});
request.close(http2.constants.NGHTTP2_CANCEL);session.close();
if(failure)throw Error('Emulator audio: '+failure);
const data=Buffer.concat(pcm);if(!data.length)throw Error('No emulator audio packets received');
const header=Buffer.alloc(44);header.write('RIFF');header.writeUInt32LE(36+data.length,4);header.write('WAVEfmt ',8);header.writeUInt32LE(16,16);header.writeUInt16LE(1,20);header.writeUInt16LE(1,22);header.writeUInt32LE(16000,24);header.writeUInt32LE(32000,28);header.writeUInt16LE(2,32);header.writeUInt16LE(16,34);header.write('data',36);header.writeUInt32LE(data.length,40);
await fs.mkdir(path.dirname(output),{recursive:true});await fs.writeFile(output,Buffer.concat([header,data]));
let peak=0,squares=0;for(let i=0;i+1<data.length;i+=2){const sample=data.readInt16LE(i);peak=Math.max(peak,Math.abs(sample));squares+=sample*sample;}
const record={scope:'Task-owned emulator playback only; no microphone capture',method:'EmulatorController.streamAudio',sample_rate:16000,channels:1,sample_bits:16,pcm_bytes:data.length,seconds:data.length/32000,peak,rms:Math.sqrt(squares/(data.length/2)),file:output};
await fs.writeFile(output+'.json',JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify(record));
