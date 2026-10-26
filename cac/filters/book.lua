-- Pandoc Lua filter: maps semantic Markdown structures to the CAC handbook template.
--
--   # Title {.part num="I" img="/images/part1.jpg" summary="..."}
--   # Title {.chapter num="701" short="Counseling Theories"
--                     code="CAC. 701" semester="1st" units="1.6"}
--   # Title {.unit num="1" week="1" hours="12"}      lecture unit inside a chapter
--   # Title {.front}      front-matter heading (roman pages)
--   # Title {.back}       back-matter heading
--   # Title {.appendix letter="A"}
--   ::: objectives | casebox | keypoint | comparative | exercise | research | summary |
--       reading | instrument | practice | illustration | safeguard | vignette | skills |
--       assessment                      (optional title="...")
--   ::: refs                            APA 7th reference list (hanging indent)
--   Other headings are shifted down one level (## -> level 3, etc.).

local function to_typst_inline(inlines)
  local doc = pandoc.Pandoc({ pandoc.Plain(inlines) })
  local out = pandoc.write(doc, 'typst')
  return (out:gsub('%s+$', ''))
end

local function esc(s)
  return (s:gsub('\\', '\\\\'):gsub('"', '\\"'))
end

-- Heading depth context: front/back matter keeps markdown levels (H1 front
-- heading, then H2/H3), main matter shifts +1 so that week sections sit under
-- the unit heading. Skipping a level would violate PDF/UA-1.
local in_front = false

local callouts = {
  objectives = true, casebox = true, keypoint = true, comparative = true,
  exercise = true, research = true, summary = true, reading = true,
  instrument = true, practice = true, illustration = true,
  safeguard = true, vignette = true, skills = true, assessment = true,
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
    local function opt(k, d) return a[k] and ('"' .. esc(a[k]) .. '"') or d end
    return pandoc.RawBlock('typst', string.format(
      '#chapter-open(num: "%s", title: [%s], short: "%s", code: [%s], semester: %s, units: %s)',
      esc(a.num or ''), to_typst_inline(el.content),
      esc(a.short or pandoc.utils.stringify(el.content)),
      to_typst_inline(pandoc.read(a.code or '', 'markdown').blocks[1].content),
      opt('semester', 'none'), opt('units', 'none')))
  elseif el.classes:includes('unit') then
    local function opt(k) return a[k] and ('"' .. esc(a[k]) .. '"') or 'none' end
    return pandoc.RawBlock('typst', string.format(
      '#unit-open(num: "%s", title: [%s], week: %s, hours: %s)',
      esc(a.num or ''), to_typst_inline(el.content), opt('week'), opt('hours')))
  elseif el.classes:includes('appendix') then
    return pandoc.RawBlock('typst', string.format(
      '#appendix-open(letter: "%s", title: [%s])',
      esc(a.letter or ''), to_typst_inline(el.content)))
  elseif el.classes:includes('front') or el.classes:includes('back') then
    in_front = true
    local outlined = el.classes:includes('unlisted') and 'false' or 'true'
    local mt = el.classes:includes('back') and '#matter.update("back")\n' or ''
    return pandoc.RawBlock('typst', string.format(
      '%s#front-heading([%s], outlined: %s, runhead: "%s")',
      mt, to_typst_inline(el.content), outlined, esc(pandoc.utils.stringify(el.content))))
  end
  if el.classes:includes('part') or el.classes:includes('chapter')
     or el.classes:includes('unit') or el.classes:includes('appendix') then
    in_front = false
  end
  if in_front then
    return el
  end
  el.level = el.level + 1
  return el
end

function Div(el)
  for _, c in ipairs(el.classes) do
    if callouts[c] then
      local title = el.attributes.title
      -- fence syntax cannot carry quoted values (pandoc smart quotes break the
      -- attribute parse), so titles are written with underscores: restore spaces
      if title then title = title:gsub('_', ' ') end
      local t = title and ('[' .. to_typst_inline(pandoc.read(title, 'markdown').blocks[1].content) .. ']') or 'none'
      local blocks = { pandoc.RawBlock('typst', string.format('#callout(kind: "%s", title: %s)[', c, t)) }
      for _, b in ipairs(el.content) do table.insert(blocks, b) end
      table.insert(blocks, pandoc.RawBlock('typst', ']'))
      return blocks
    end
    if c == 'refs' then
      local blocks = { pandoc.RawBlock('typst', '#apa-refs[') }
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
