"""Schema-1 structure derived from the reviewed common Kotlin model declarations."""
import re

MODEL_PATHS = (
    'composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt',
    'composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt',
)
UNIONS = ('TeachingLink', 'InlineContent', 'BlockPayload', 'LegacyLookup', 'AliasOutcome')


def snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def balanced(text, start, opening, closing):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == opening:
            depth += 1
        elif text[i] == closing:
            depth -= 1
            if not depth:
                return i
    raise ValueError('Unbalanced Kotlin model declaration')


class Schema:
    def __init__(self, root):
        self.classes, self.enums, self.wrappers, self.unions = {}, {}, set(), {}
        for path in MODEL_PATHS:
            text = (root / path).read_text()
            spans = []
            for union in UNIONS:
                match = re.search(r'sealed interface ' + union + r'\s*\{', text)
                if match:
                    begin = text.index('{', match.start())
                    spans.append((begin, balanced(text, begin, '{', '}'), union))
                    self.unions[union] = {}
            for match in re.finditer(r'data class (\w+)\s*\(', text):
                name = match[1]
                parent = next((u for a, b, u in spans if a < match.start() < b), None)
                qualified = f'{parent}.{name}' if parent else name
                begin = text.index('(', match.start())
                body = text[begin + 1:balanced(text, begin, '(', ')')]
                fields = list(re.finditer(r'\bval\s+(\w+)\s*:\s*', body))
                result = []
                for i, field in enumerate(fields):
                    end = fields[i+1].start() if i+1 < len(fields) else len(body)
                    kind = body[field.end():end].strip().rstrip(',').split('=', 1)[0].strip().rstrip(',').strip()
                    result.append((snake(field[1]), field[1], kind))
                self.classes[qualified] = result
                if parent:
                    self.unions[parent][snake(name)] = qualified
            self.wrappers.update(re.findall(r'value class (\w+)\(', text))
            for match in re.finditer(r'enum class (\w+)', text):
                begin = text.index('{', match.end())
                body = text[begin+1:balanced(text, begin, '{', '}')]
                entries = (['VEHICLE', 'ENVIRONMENT', 'SAFETY', 'RULES', 'PERSONAL']
                           if match[1] == 'Category' else re.findall(r'\b[A-Z][A-Z_]*\b', body))
                self.enums[match[1]] = {v.lower(): v for v in entries}
        self.aliases = {'RichText': 'List<InlineContent>'}

    @staticmethod
    def generic(kind):
        name, args = kind.split('<', 1)
        parts, level, begin = [], 0, 0
        args = args[:-1]
        for i, c in enumerate(args):
            level += (c == '<') - (c == '>')
            if c == ',' and level == 0:
                parts.append(args[begin:i].strip())
                begin = i+1
        parts.append(args[begin:].strip())
        return name, parts
