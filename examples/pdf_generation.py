import pathlib
import typing

import reportlab.pdfgen.canvas
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts
import reportlab.lib.pagesizes
import reportlab.platypus as platypus
import reportlab.platypus.tables
import reportlab.platypus.flowables
import reportlab.lib.styles as styles
import dataclasses

reportlab.pdfbase.pdfmetrics.registerFont(
    reportlab.pdfbase.ttfonts.TTFont("JetBrains Mono", "JetBrainsMono-SemiBold.ttf")
)


@dataclasses.dataclass
class Model:
    """
    Represents a model in a traveler PDF
    """

    name: pathlib.Path
    screenshot: typing.BinaryIO
    dimensions: tuple[float, float, float]


class TravelerPDF:
    """
    Represents a traveler PDF
    """

    _doc: platypus.SimpleDocTemplate
    _story: list[platypus.Flowable]
    _width: int
    _height: int
    _FONT: str = "JetBrains Mono"
    _FONT_SIZE: int = 12
    _SUBHEADING_FONT_SIZE: int = _FONT_SIZE + 2
    _HEADING_FONT_SIZE: int = _FONT_SIZE + 3
    _HEADING_STYLE: styles.ParagraphStyle = styles.ParagraphStyle(
        "Heading", fontName=_FONT, fontSize=_HEADING_FONT_SIZE
    )
    _SUBHEADING_STYLE: styles.ParagraphStyle = styles.ParagraphStyle(
        "Heading", fontName=_FONT, fontSize=_SUBHEADING_FONT_SIZE
    )
    _STYLE: styles.ParagraphStyle = styles.ParagraphStyle(
        "Normal", fontName=_FONT, fontSize=_FONT_SIZE
    )
    _TABLE_STYLE: platypus.tables.TableStyle = platypus.tables.TableStyle(
        [["VALIGN", (0, 0), (-1, -1), "TOP"], ["ALIGN", (0, 0), (-1, -1), "LEFT"]]
    )

    def __init__(self, filepath: pathlib.Path):
        """
        Constructs a TravelerPDF
        :param filepath: The file path of the PDF
        """
        self._doc = platypus.SimpleDocTemplate(
            str(filepath),
            pagesize=reportlab.lib.pagesizes.letter,
            leftMargin=18,
            rightMargin=18,
            topMargin=18,
            bottomMargin=18,
        )
        self._story = []
        self._width, self._height = reportlab.lib.pagesizes.letter

    def add_header(
        self,
        form_file_name: str,
        printer_type: str,
        material: str,
        print_setting: str,
        layer_thickness_mm: str,
        build_volume_image: typing.BinaryIO,
    ) -> None:
        """
        Adds a header tp this TravelerPDF
        :param form_file_name: The name of the .form file this TravelerPDF describes
        :param printer_type: The model of printer this job is to be printed on
        :param material: The material with which this job is to be printed
        :param print_setting: The print setting with which this job is to be printed
        :param layer_thickness_mm: The layer thickness, in mm, with which this job is to be printed
        :param build_volume_image: An image of all models in the build volume
        """
        self._story.append(platypus.Paragraph("Job Summary", self._HEADING_STYLE))

        self._story.append(platypus.Spacer(self._width, 10))

        h1_subdata = [
            [platypus.Paragraph("Name", self._HEADING_STYLE)],
            [platypus.Paragraph(form_file_name, self._STYLE)],
        ]
        h1_subtable = platypus.Table(h1_subdata, hAlign="LEFT")
        h1_data = [
            [platypus.Image(build_volume_image, hAlign="LEFT", lazy=0), h1_subtable]
        ]
        h1_table = platypus.Table(h1_data, style=self._TABLE_STYLE, hAlign="LEFT")
        self._story.append(h1_table)

        self._story.append(platypus.Paragraph(printer_type, self._HEADING_STYLE))

        self._story.append(platypus.Spacer(self._width, 10))

        print_setting_data = [
            [
                platypus.Paragraph("Material", self._SUBHEADING_STYLE),
                platypus.Paragraph("Print Setting", self._SUBHEADING_STYLE),
                platypus.Paragraph("Layer Thickness (mm)", self._SUBHEADING_STYLE),
            ],
            [
                platypus.Paragraph(material, self._STYLE),
                platypus.Paragraph(print_setting, self._STYLE),
                platypus.Paragraph(layer_thickness_mm, self._STYLE),
            ],
        ]
        self._story.append(
            platypus.Table(print_setting_data, style=self._TABLE_STYLE, hAlign="LEFT")
        )

        self._story.append(platypus.Spacer(self._width, 10))

        self._story.append(platypus.Paragraph("Parts:", self._HEADING_STYLE))

    def add_parts(self, parts: typing.Iterable[Model]) -> None:
        """
        Adds a list of parts to this TravelerPDF
        :param parts: A list of parts to add to this TravelerPDF
        """
        self._story.append(platypus.Spacer(self._width, 10))
        self._story.append(
            platypus.ListFlowable(
                map(
                    lambda part: platypus.ListItem(
                        platypus.Paragraph(part.name.stem, self._STYLE)
                    ),
                    parts,
                ),
                bulletType="bullet",
            )
        )
        part_table_data = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                part_table_data.append([])
            dimensions = f"{'x'.join(map(lambda dim: f'{dim:.2f}', part.dimensions))}mm"
            htable_data = [
                [
                    platypus.Image(part.screenshot, hAlign="LEFT", lazy=0),
                    platypus.Paragraph(dimensions, self._STYLE),
                ]
            ]
            htable = platypus.Table(htable_data, style=self._TABLE_STYLE)
            vtable_data = [
                [platypus.Paragraph(part.name.stem, self._SUBHEADING_STYLE)],
                [htable],
            ]
            vtable = platypus.Table(vtable_data, style=self._TABLE_STYLE)
            part_table_data[-1].append(vtable)
        part_table = platypus.Table(
            part_table_data, style=self._TABLE_STYLE, hAlign="LEFT"
        )
        self._story.append(part_table)

    def save(self) -> None:
        """
        Saves this TravelerPDF to a file
        """
        self._doc.build(self._story)
