"""Kotlin literal and typed-object emission for the current content generators.

Historical migration approval/receipt validation is retained in the recovery archive.
This module only converts the retained JSON fields into Kotlin declarations.
"""
import json


def kotlin_string(value):
    def quote(s):
        return json.dumps(s,ensure_ascii=False).replace('$','\\$').replace('\\f','\\u000c')
    if len(value)<=4000:return quote(value)
    return 'listOf('+', '.join(quote(value[i:i+4000]) for i in range(0,len(value),4000))+').joinToString("")'


class Emitter:
    def __init__(self,schema,symbol):
        self.schema,self.symbol=schema,symbol
        self.functions=[]
        self.trace=[]

    def function(self,kind,expression,path,origin):
        name=f'{self.symbol}Node{len(self.functions):06}'
        self.functions.append((name,kind,expression))
        self.trace.append({'symbol':name,'input':path,'origin':origin})
        return name+'()'

    def emit(self,value,kind,path,origin=None):
        kind=self.schema.aliases.get(kind,kind)
        if value is None:return 'null'
        if kind.endswith('?'):return self.emit(value,kind[:-1],path,origin)
        if '<' in kind:
            outer,args=self.schema.generic(kind)
            if outer=='Map':
                terms=[self.emit(k,args[0],path+'/key',origin)+' to '+self.emit(value[k],args[1],path+'/'+k,origin) for k in sorted(value)]
                if len(terms)>20:
                    chunks=[self.function(kind,'mapOf('+', '.join(terms[i:i+20])+')',path,origin) for i in range(0,len(terms),20)]
                    return self.function(kind,' + '.join(chunks),path,origin)
                return 'mapOf('+', '.join(terms)+')'
            terms=[self.emit(x,args[0],path+f'/{i}',origin) for i,x in enumerate(value)]
            if len(terms)>20:
                chunks=[self.function(kind,('setOf' if outer=='Set' else 'listOf')+'('+', '.join(terms[i:i+20])+')',path,origin) for i in range(0,len(terms),20)]
                return self.function(kind,' + '.join(chunks),path,origin)
            return ('setOf' if outer=='Set' else 'listOf')+'('+', '.join(terms)+')'
        if kind=='String':return kotlin_string(value)
        if kind in self.schema.wrappers:return kind+'('+kotlin_string(value)+')'
        if kind=='Int':return str(value)
        if kind=='Boolean':return str(value).lower()
        if kind in self.schema.enums:return kind+'.'+self.schema.enums[kind][value]
        target=self.schema.unions[kind][value['type']] if kind in self.schema.unions else kind
        origin=value.get('origin',value.get('metadata',{}).get('origin',origin))
        terms=[camel+' = '+self.emit(value[field],typ,path+'/'+field,origin) for field,camel,typ in self.schema.classes[target]]
        return self.function(target,target+'('+', '.join(terms)+')',path,origin)
