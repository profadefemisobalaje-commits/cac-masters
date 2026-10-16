-- Pandoc Lua filter: maps semantic Markdown structures to the Typst book template.
--
--   # Title {.part num="I" img="/images/part1.jpg" summary="..."}
--   # Title {.chapter num="5" short="Petroleum Law"}
--   # Title {.front}      front-matter heading (roman pages)
--   # Title {.back}       back-matter heading
--   # Title {.appendix letter="A"}
--   ::: casebox | keypoint | objectives | exercise | research | summary | reading |
--       comparative | instrument | practice | illustration   (optional title="...")
--   Other headings are shifted down one level (## -> level 3, etc.).

local function to_typst_inline(inlines)
  local doc = pandoc.Pandoc({ pandoc.Plain(inlines) })
  local out = pandoc.write(doc, 'typst')
  return (out:gsub('%s+$', ''))
end

local function esc(s)
  return (s:gsub('\\', '\\\\'):gsub('"', '\\"'))
end

local callouts = {
  objectives = true, casebox = true, keypoint = true, comparative = true,
  exercise = true, research = true, summary = true, reading = true,
  instrument = true, practice = true, illustration = true,
}

function Header(el)
  local a = el.attributes
  if el.classes:includes('part') then
    local img = a.img and ('"' .. esc(a.img) .. '"') or 'none'
    local summary = a.summary and to_typst_inline(pandoc.read(a.summary, 'markdown').blocks[1].content) or ''
    return pandoc.RawBlock('typst', string.format(
      '#part-page(num: "%s", title: [%s], img: %s, summary: [%s])',
      esc(a.num or ''), to_typst_inline(el.content), img, summary))
  elseif el.classes:includes('chapter') then
    return pandoc.RawBlock('typst', string.format(
      '#chapter-open(num: "%s", title: [%s], short: "%s")',
      esc(a.num or ''), to_typst_inline(el.content), esc(a.short or pandoc.utils.stringify(el.content))))
  elseif el.classes:includes('appendix') then
    return pandoc.RawBlock('typst', string.format(
      '#appendix-open(letter: "%s", title: [%s])',
      esc(a.letter or ''), to_typst_inline(el.content)))
  elseif el.classes:includes('front') or el.classes:includes('back') then
    local outlined = el.classes:includes('unlisted') and 'false' or 'true'
    local mt = el.classes:includes('back') and '#matter.update("back")\n' or ''
    return pandoc.RawBlock('typst', string.format(
      '%s#front-heading([%s], outlined: %s, runhead: "%s")',
      mt, to_typst_inline(el.content), outlined, esc(pandoc.utils.stringify(el.content))))
  end
  el.level = el.level + 1
  return el
end

function Div(el)
  for _, c in ipairs(el.classes) do
    if callouts[c] then
      local title = el.attributes.title
      local t = title and ('[' .. to_typst_inline(pandoc.read(title, 'markdown').blocks[1].content) .. ']') or 'none'
      local blocks = { pandoc.RawBlock('typst', string.format('#callout(kind: "%s", title: %s)[', c, t)) }
      for _, b in ipairs(el.content) do table.insert(blocks, b) end
      table.insert(blocks, pandoc.RawBlock('typst', ']'))
      return blocks
    end
    if c == 'pagebreak' then
      return pandoc.RawBlock('typst', '#pagebreak()')
    end
    if c == 'raw-typst' then
      return el.content
    end
  end
  return nil
end
