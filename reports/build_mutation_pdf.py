from pathlib import Path
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports"
ASSET_DIR = OUT_DIR / "relatorio-assets"
PDF_PATH = OUT_DIR / "relatorio-teste-mutacao.pdf"


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1F3655"),
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#666666"),
            spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "Heading1Custom",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=17,
            textColor=colors.HexColor("#1F3655"),
            spaceBefore=10,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12.2,
            spaceAfter=6,
        ),
        "caption": ParagraphStyle(
            "CaptionCustom",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=9.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#666666"),
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "BulletCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            leftIndent=14,
            bulletIndent=5,
            spaceAfter=3.2,
        ),
    }


def table(data, col_widths):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEFF5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1F3655")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.6),
                ("LEADING", (0, 0), (-1, -1), 10.5),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D1DB")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def para(text, style):
    return Paragraph(text, style)


def bullet(text, style):
    return Paragraph(text, style, bulletText="•")


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawCentredString(letter[0] / 2, letter[1] - 0.38 * inch, "Relatório de Teste de Mutação com StrykerJS")
    canvas.setStrokeColor(colors.HexColor("#D8DEE6"))
    canvas.line(0.55 * inch, letter[1] - 0.46 * inch, letter[0] - 0.55 * inch, letter[1] - 0.46 * inch)
    canvas.drawRightString(letter[0] - 0.55 * inch, 0.36 * inch, str(doc.page))
    canvas.restoreState()


def main():
    s = styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=0.62 * inch,
        rightMargin=0.62 * inch,
        topMargin=0.68 * inch,
        bottomMargin=0.55 * inch,
    )

    story = []
    story.append(para("Relatório de Teste de Mutação", s["title"]))
    story.append(para("Projeto operacoes-mutante | StrykerJS + Jest", s["subtitle"]))
    story.append(
        table(
            [
                ["Campo", "Informação"],
                ["Disciplina", "Testes de Software"],
                ["Trabalho", "Análise e melhoria de suíte por teste de mutação"],
                ["Aluno(a)", "[preencher nome completo]"],
                ["Matrícula", "[preencher matrícula]"],
                ["Data", date.today().strftime("%d/%m/%Y")],
                ["Repositório GitHub", "[inserir link do fork do projeto]"],
            ],
            [1.55 * inch, 5.15 * inch],
        )
    )
    story.append(Spacer(1, 0.08 * inch))
    story.append(para("1. Análise inicial", s["h1"]))
    story.append(
        para(
            "A suíte inicial possuía 50 testes, um para cada função exportada. A cobertura de código parecia alta: "
            "85,41% de statements, 58,82% de branches, 100% de funções e 98,64% de linhas. Apesar disso, a primeira "
            "execução do Stryker mostrou uma pontuação de mutação bem menor: 73,71% no score total e 78,11% considerando "
            "apenas código coberto.",
            s["body"],
        )
    )
    story.append(
        table(
            [
                ["Métrica", "Resultado inicial"],
                ["Cobertura de linhas", "98,64%"],
                ["Cobertura de funções", "100,00%"],
                ["Cobertura de branches", "58,82%"],
                ["Mutation score", "73,71%"],
                ["Mutantes mortos / timeout", "154 mortos + 3 timeout"],
                ["Mutantes sobreviventes", "44"],
                ["Mutantes sem cobertura", "12"],
            ],
            [2.2 * inch, 4.5 * inch],
        )
    )
    story.append(Spacer(1, 0.07 * inch))
    story.append(
        para(
            "A discrepância ocorreu porque cobertura mede se uma linha foi executada, mas não mede se a asserção é forte o "
            "bastante para detectar uma mudança de comportamento. Muitos testes verificavam apenas o caminho feliz, como "
            "números positivos, casos verdadeiros e arrays ímpares.",
            s["body"],
        )
    )

    story.append(PageBreak())
    story.append(para("2. Análise de mutantes críticos", s["h1"]))
    story.append(
        para(
            "Foram selecionados três mutantes da primeira execução por representarem falhas típicas da suíte: ausência de "
            "casos negativos, ausência de testes de fronteira e ausência de cobertura em ramos específicos.",
            s["body"],
        )
    )
    for idx, name in enumerate(["mutante-isprimo.png", "mutante-maior.png"], start=1):
        story.append(Image(str(ASSET_DIR / name), width=6.15 * inch, height=3.4 * inch))
        story.append(para(f"Figura {idx}. Captura/reprodução do mutante sobrevivente na primeira execução.", s["caption"]))

    story.append(PageBreak())
    story.append(Image(str(ASSET_DIR / "mutante-mediana.png"), width=6.15 * inch, height=3.4 * inch))
    story.append(para("Figura 3. Captura/reprodução do mutante relacionado à mediana.", s["caption"]))
    story.append(
        para(
            "No caso de isPrimo, a mutação no laço sobreviveu porque a suíte só testava um número primo. Sem isPrimo(4), "
            "o teste não demonstrava que números compostos deveriam retornar false. Em isMaiorQue, trocar > por >= não "
            "altera o resultado quando a entrada é 10 e 5; o caso que revela o erro é a igualdade. Em medianaArray, os "
            "testes originais não passavam por arrays pares nem verificavam ordenação.",
            s["body"],
        )
    )
    story.append(para("3. Solução implementada", s["h1"]))
    for item in [
        "Mensagens e caminhos de erro: exceções em divisão por zero, raiz negativa, fatorial negativo, arrays vazios e inverso de zero.",
        "Fronteiras: fatorial(0), fatorial(1), raizQuadrada(0) e mediaArray([]).",
        "Booleanos em ambos os sentidos: isPar(101), isImpar(8), isDivisivel(10, 3), comparações falsas e igualdade.",
        "Números e limites: isPrimo(1), isPrimo(4), produtoArray([]), clamp abaixo, acima e exatamente nos limites.",
        "Mediana: arrays desordenados e pares, como [7, 1, 3, 5], cujo resultado esperado é 4.",
    ]:
        story.append(bullet(item, s["bullet"]))

    story.append(PageBreak())
    story.append(para("4. Resultados finais", s["h1"]))
    story.append(
        table(
            [
                ["Métrica", "Resultado final"],
                ["Testes Jest", "56 testes passando"],
                ["Cobertura", "100% statements, branches, funções e linhas"],
                ["Mutation score", "100,00%"],
                ["Mutantes mortos / timeout", "199 mortos + 3 timeout"],
                ["Mutantes sobreviventes", "0"],
                ["Mutantes sem cobertura", "0"],
            ],
            [2.2 * inch, 4.5 * inch],
        )
    )
    story.append(Spacer(1, 0.08 * inch))
    story.append(
        para(
            "A meta de pontuação de mutação superior a 98% foi atingida. O relatório final do Stryker foi gerado em "
            "reports/mutation/mutation.html e apresenta 100,00% de mutation score. Alguns mutantes restantes eram "
            "equivalentes, como fatorial(0/1), produtoArray([]) e clamp(valor === min/max), e foram marcados com comentários "
            "específicos do Stryker explicando o motivo técnico.",
            s["body"],
        )
    )
    story.append(para("5. Conclusão", s["h1"]))
    story.append(
        para(
            "O teste de mutação mostrou que uma suíte pode ter cobertura alta e ainda assim ser fraca. A cobertura inicial "
            "indicava que quase todas as linhas eram executadas, mas o Stryker revelou que muitos testes não tinham asserções "
            "capazes de distinguir o comportamento correto de pequenas alterações. Ao adicionar casos de fronteira, ramos "
            "negativos e entradas mais representativas, a suíte passou a validar melhor a intenção do código. Por isso, teste "
            "de mutação é uma ferramenta importante para avaliar a qualidade dos testes, não apenas a quantidade de código percorrido.",
            s["body"],
        )
    )

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(PDF_PATH)


if __name__ == "__main__":
    main()
