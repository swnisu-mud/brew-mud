#!/usr/bin/env python3
"""Build the accessible BrewMUD student handout as a Word document."""

from __future__ import annotations

import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "STUDENT_INFORMATION_SHEET.md"
OUTPUT = ROOT / "docs" / "BrewMUD_Student_Information_Sheet.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
XML_NS = "http://www.w3.org/XML/1998/namespace"

ET.register_namespace("w", W_NS)
ET.register_namespace("r", R_NS)


def qn(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def w(name: str) -> str:
    return qn(W_NS, name)


def set_val(element: ET.Element, value: str) -> None:
    element.set(w("val"), value)


class DocumentBuilder:
    def __init__(self) -> None:
        self.document = ET.Element(w("document"))
        self.body = ET.SubElement(self.document, w("body"))
        self.relationships: list[tuple[str, str]] = []
        self.next_relationship = 1
        self.ordered_list_ids: list[int] = []
        self.next_list_id = 2

    def add_run(
        self,
        parent: ET.Element,
        text: str,
        *,
        bold: bool = False,
        italic: bool = False,
        code: bool = False,
    ) -> None:
        if not text:
            return
        run = ET.SubElement(parent, w("r"))
        if bold or italic or code:
            properties = ET.SubElement(run, w("rPr"))
            if bold:
                ET.SubElement(properties, w("b"))
            if italic:
                ET.SubElement(properties, w("i"))
            if code:
                fonts = ET.SubElement(properties, w("rFonts"))
                fonts.set(w("ascii"), "Consolas")
                fonts.set(w("hAnsi"), "Consolas")
                size = ET.SubElement(properties, w("sz"))
                set_val(size, "20")
                shade = ET.SubElement(properties, w("shd"))
                shade.set(w("fill"), "F2F2F2")
        node = ET.SubElement(run, w("t"))
        if text[:1].isspace() or text[-1:].isspace():
            node.set(qn(XML_NS, "space"), "preserve")
        node.text = text

    def add_hyperlink(
        self,
        parent: ET.Element,
        label: str,
        target: str,
        *,
        bold: bool = False,
        italic: bool = False,
    ) -> None:
        relationship_id = f"rId{self.next_relationship}"
        self.next_relationship += 1
        self.relationships.append((relationship_id, target))
        link = ET.SubElement(parent, w("hyperlink"))
        link.set(qn(R_NS, "id"), relationship_id)
        link.set(w("history"), "1")
        run = ET.SubElement(link, w("r"))
        properties = ET.SubElement(run, w("rPr"))
        style = ET.SubElement(properties, w("rStyle"))
        set_val(style, "Hyperlink")
        if bold:
            ET.SubElement(properties, w("b"))
        if italic:
            ET.SubElement(properties, w("i"))
        node = ET.SubElement(run, w("t"))
        node.text = label

    def add_inline(
        self,
        parent: ET.Element,
        text: str,
        *,
        bold: bool = False,
        italic: bool = False,
    ) -> None:
        cursor = 0
        while cursor < len(text):
            candidates: list[tuple[int, str]] = []
            for marker, kind in (("[", "link"), ("**", "bold"), ("`", "code"), ("*", "italic")):
                location = text.find(marker, cursor)
                if location >= 0:
                    candidates.append((location, kind))
            if not candidates:
                self.add_run(parent, text[cursor:], bold=bold, italic=italic)
                break

            location, kind = min(candidates, key=lambda item: item[0])
            self.add_run(parent, text[cursor:location], bold=bold, italic=italic)

            if kind == "link":
                match = re.match(r"\[([^]]+)]\(([^)]+)\)", text[location:])
                if match:
                    self.add_hyperlink(
                        parent, match.group(1), match.group(2), bold=bold, italic=italic
                    )
                    cursor = location + match.end()
                    continue
            elif kind == "bold":
                end = text.find("**", location + 2)
                if end >= 0:
                    self.add_inline(
                        parent, text[location + 2:end], bold=True, italic=italic
                    )
                    cursor = end + 2
                    continue
            elif kind == "code":
                end = text.find("`", location + 1)
                if end >= 0:
                    self.add_run(
                        parent, text[location + 1:end], bold=bold, italic=italic, code=True
                    )
                    cursor = end + 1
                    continue
            elif kind == "italic":
                end = text.find("*", location + 1)
                if end >= 0:
                    self.add_inline(
                        parent, text[location + 1:end], bold=bold, italic=True
                    )
                    cursor = end + 1
                    continue

            self.add_run(parent, text[location], bold=bold, italic=italic)
            cursor = location + 1

    def paragraph(
        self,
        text: str = "",
        *,
        style: str | None = None,
        numbered: int | None = None,
        bullet: bool = False,
        code_block: bool = False,
    ) -> ET.Element:
        paragraph = ET.SubElement(self.body, w("p"))
        properties = ET.SubElement(paragraph, w("pPr"))
        if style:
            pstyle = ET.SubElement(properties, w("pStyle"))
            set_val(pstyle, style)
        if numbered is not None or bullet:
            numbering = ET.SubElement(properties, w("numPr"))
            level = ET.SubElement(numbering, w("ilvl"))
            set_val(level, "0")
            num_id = ET.SubElement(numbering, w("numId"))
            set_val(num_id, str(numbered if numbered is not None else 1))
        if code_block:
            spacing = ET.SubElement(properties, w("spacing"))
            spacing.set(w("before"), "0")
            spacing.set(w("after"), "0")
            shade = ET.SubElement(properties, w("shd"))
            shade.set(w("fill"), "F2F2F2")
            self.add_run(paragraph, text, code=True)
        else:
            self.add_inline(paragraph, text)
        return paragraph

    def table(self, headers: list[str], rows: list[list[str]]) -> None:
        table = ET.SubElement(self.body, w("tbl"))
        properties = ET.SubElement(table, w("tblPr"))
        style = ET.SubElement(properties, w("tblStyle"))
        set_val(style, "TableGrid")
        width = ET.SubElement(properties, w("tblW"))
        width.set(w("w"), "0")
        width.set(w("type"), "auto")
        caption = ET.SubElement(properties, w("tblCaption"))
        set_val(caption, "BrewMUD command reference")
        description = ET.SubElement(properties, w("tblDescription"))
        set_val(description, "Keyboard commands and an explanation of what each command does")

        grid = ET.SubElement(table, w("tblGrid"))
        for grid_width in ("2600", "6200"):
            column = ET.SubElement(grid, w("gridCol"))
            column.set(w("w"), grid_width)

        for row_index, values in enumerate([headers, *rows]):
            row = ET.SubElement(table, w("tr"))
            if row_index == 0:
                row_properties = ET.SubElement(row, w("trPr"))
                ET.SubElement(row_properties, w("tblHeader"))
            for value in values:
                cell = ET.SubElement(row, w("tc"))
                cell_properties = ET.SubElement(cell, w("tcPr"))
                cell_width = ET.SubElement(cell_properties, w("tcW"))
                cell_width.set(w("w"), "0")
                cell_width.set(w("type"), "auto")
                paragraph = ET.SubElement(cell, w("p"))
                paragraph_properties = ET.SubElement(paragraph, w("pPr"))
                if row_index == 0:
                    shade = ET.SubElement(cell_properties, w("shd"))
                    shade.set(w("fill"), "F1BE48")
                    run = ET.SubElement(paragraph, w("r"))
                    run_properties = ET.SubElement(run, w("rPr"))
                    ET.SubElement(run_properties, w("b"))
                    node = ET.SubElement(run, w("t"))
                    node.text = value
                else:
                    self.add_inline(paragraph, value)

    def new_ordered_list(self) -> int:
        list_id = self.next_list_id
        self.next_list_id += 1
        self.ordered_list_ids.append(list_id)
        return list_id

    def page_break(self) -> None:
        paragraph = ET.SubElement(self.body, w("p"))
        run = ET.SubElement(paragraph, w("r"))
        page_break = ET.SubElement(run, w("br"))
        page_break.set(w("type"), "page")

    def finish(self) -> None:
        section = ET.SubElement(self.body, w("sectPr"))
        size = ET.SubElement(section, w("pgSz"))
        size.set(w("w"), "12240")
        size.set(w("h"), "15840")
        margins = ET.SubElement(section, w("pgMar"))
        for side, value in {
            "top": "720", "right": "900", "bottom": "720", "left": "900",
            "header": "360", "footer": "360", "gutter": "0",
        }.items():
            margins.set(w(side), value)


def markdown_to_document(markdown: str) -> DocumentBuilder:
    builder = DocumentBuilder()
    lines = markdown.splitlines()
    index = 0
    in_code = False
    ordered_list: int | None = None

    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            in_code = not in_code
            ordered_list = None
            index += 1
            continue
        if in_code:
            builder.paragraph(line, style="CodeBlock", code_block=True)
            index += 1
            continue
        if not line.strip():
            ordered_list = None
            index += 1
            continue
        if line.strip() == "<!-- PAGE BREAK -->":
            builder.page_break()
            ordered_list = None
            index += 1
            continue
        if line.startswith("# "):
            builder.paragraph(line[2:], style="Heading1")
            ordered_list = None
        elif line.startswith("## "):
            builder.paragraph(line[3:], style="Heading2")
            ordered_list = None
        elif line.startswith("### "):
            builder.paragraph(line[4:], style="Heading3")
            ordered_list = None
        elif (
            line.startswith("|")
            and index + 1 < len(lines)
            and re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", lines[index + 1])
        ):
            headers = [cell.strip() for cell in line.strip("|").split("|")]
            rows: list[list[str]] = []
            index += 2
            while index < len(lines) and lines[index].startswith("|"):
                rows.append([cell.strip() for cell in lines[index].strip("|").split("|")])
                index += 1
            builder.table(headers, rows)
            ordered_list = None
            continue
        elif re.match(r"^\d+\.\s+", line):
            if ordered_list is None:
                ordered_list = builder.new_ordered_list()
            text = re.sub(r"^\d+\.\s+", "", line)
            builder.paragraph(text, style="ListParagraph", numbered=ordered_list)
        elif line.startswith("- "):
            builder.paragraph(line[2:], style="ListParagraph", bullet=True)
            ordered_list = None
        else:
            builder.paragraph(line)
            ordered_list = None
        index += 1

    builder.finish()
    return builder


def styles_xml() -> bytes:
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W_NS}">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:lang w:val="en-US"/><w:sz w:val="22"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Aptos Display" w:hAnsi="Aptos Display"/><w:b/><w:color w:val="7C2529"/><w:sz w:val="36"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts w:ascii="Aptos Display" w:hAnsi="Aptos Display"/><w:b/><w:color w:val="7C2529"/><w:sz w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="140" w:after="40"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:rFonts w:ascii="Aptos Display" w:hAnsi="Aptos Display"/><w:b/><w:color w:val="7C2529"/><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="540" w:hanging="270"/><w:contextualSpacing/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock"><w:name w:val="Code Block"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="20"/></w:rPr></w:style>
  <w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:basedOn w:val="DefaultParagraphFont"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/></w:rPr></w:style>
  <w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:uiPriority w:val="59"/><w:qFormat/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="B7B7B7"/><w:left w:val="single" w:sz="4" w:color="B7B7B7"/><w:bottom w:val="single" w:sz="4" w:color="B7B7B7"/><w:right w:val="single" w:sz="4" w:color="B7B7B7"/><w:insideH w:val="single" w:sz="4" w:color="D9D9D9"/><w:insideV w:val="single" w:sz="4" w:color="D9D9D9"/></w:tblBorders><w:tblCellMar><w:top w:w="80" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
</w:styles>"""
    return xml.encode("utf-8")


def numbering_xml(list_ids: list[int]) -> bytes:
    instances = "".join(
        f'<w:num w:numId="{list_id}"><w:abstractNumId w:val="0"/>'
        f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'
        for list_id in list_ids
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="{W_NS}">
  <w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="540"/></w:tabs><w:ind w:left="540" w:hanging="270"/></w:pPr></w:lvl></w:abstractNum>
  <w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="540"/></w:tabs><w:ind w:left="540" w:hanging="270"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num>
  {instances}
</w:numbering>"""
    return xml.encode("utf-8")


def document_relationships(builder: DocumentBuilder) -> bytes:
    links = "".join(
        f'<Relationship Id="{relationship_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{escape(target)}" TargetMode="External"/>'
        for relationship_id, target in builder.relationships
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rIdNumbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
  {links}
</Relationships>"""
    return xml.encode("utf-8")


def write_docx(builder: DocumentBuilder) -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    content_types = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    root_relationships = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>BrewMUD Student Information Sheet</dc:title>
  <dc:subject>Accessible instructions and study guidance for BrewMUD</dc:subject>
  <dc:creator>BBMB 1200 BrewMUD</dc:creator>
  <dc:description>Student guide to navigating BrewMUD, completing quests, and using pop quizzes as a study guide.</dc:description>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''.encode("utf-8")
    app = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>BrewMUD handout builder</Application><AppVersion>1.0</AppVersion></Properties>'''

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_relationships)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)
        archive.writestr(
            "word/document.xml",
            ET.tostring(builder.document, encoding="utf-8", xml_declaration=True),
        )
        archive.writestr("word/styles.xml", styles_xml())
        archive.writestr("word/numbering.xml", numbering_xml(builder.ordered_list_ids))
        archive.writestr("word/_rels/document.xml.rels", document_relationships(builder))


def main() -> None:
    builder = markdown_to_document(SOURCE.read_text(encoding="utf-8"))
    write_docx(builder)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
