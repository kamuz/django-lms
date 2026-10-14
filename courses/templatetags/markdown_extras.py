import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


def _escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


@register.filter(name='markdown_inline')
@stringfilter
def markdown_inline_filter(value):
    value = _escape_html(value)
    return mark_safe(_inline(value))


@register.filter(name='markdown')
@stringfilter
def markdown_filter(value):
    code_blocks = []

    def _save_code(match):
        code_blocks.append(match.group(1))
        return f'\x00CODE{len(code_blocks) - 1}\x00'

    value = re.sub(r'```[^\n]*\n(.*?)```', _save_code, value, flags=re.DOTALL)

    lines = value.split('\n')
    html_parts = []
    in_ul = False
    paragraph = []

    def flush_paragraph():
        if paragraph:
            html_parts.append('<p>' + _inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()

    def flush_list():
        nonlocal in_ul
        if in_ul:
            html_parts.append('</ul>')
            in_ul = False

    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_paragraph()
            flush_list()
            level = len(m.group(1))
            html_parts.append(f'<h{level}>{_inline(m.group(2))}</h{level}>')
            continue

        if line.startswith('- '):
            flush_paragraph()
            if not in_ul:
                html_parts.append('<ul>')
                in_ul = True
            html_parts.append(f'<li>{_inline(line[2:])}</li>')
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            continue

        if line.strip().startswith('<iframe'):
            flush_paragraph()
            flush_list()
            html_parts.append(line)
            continue

        if line.startswith('\x00CODE'):
            flush_paragraph()
            flush_list()
            html_parts.append(line)
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()

    result = '\n'.join(html_parts)

    for i, code in enumerate(code_blocks):
        result = result.replace(
            f'\x00CODE{i}\x00',
            f'<pre><code>{_escape_html(code)}</code></pre>'
        )

    return mark_safe(result)


@register.filter(name='markdown_safe')
@stringfilter
def markdown_safe_filter(value):
    value = _escape_html(value)
    return markdown_filter(value)