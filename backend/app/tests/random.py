from pathlib import Path
from backend.app.parse import parse

def test_parse_pdf():
    pdf_path = Path(__file__).parent / "resources" / "random.pdf"

    text = parse(pdf_path)

