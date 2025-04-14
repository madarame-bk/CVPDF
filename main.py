import xml.etree.ElementTree as ET
from fpdf import FPDF
import os


class CVPDF(FPDF):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.name = data.findtext('personal/name')
        self.title = data.findtext('personal/title')
        self.left_width = 110
        self.right_width = 60
        self.left_margin_indent = self.l_margin + 10
        self.top_margin = self.t_margin
        self.base_font_size = 8  # BASE FONT SIZE

    def name_and_position(self):
        self.ln(10)
        self.set_font("font_a", "B", self.base_font_size * 3)
        self.cell(0, 6, self.name, ln=1)
        self.set_font("font_a", "", self.base_font_size * 1.4)
        self.cell(0, 10, self.title, ln=1)
        self.ln(5)

    def section_title(self, title, icon_path=None):
        if icon_path and os.path.exists(icon_path):
            icon_width = 6
            icon_height = 6
            icon_x = self.get_x()
            icon_y = self.get_y() + (10 - icon_height) / 2
            self.image(icon_path, x=icon_x - 8, y=icon_y, w=icon_width, h=icon_height)

        self.set_font("font_a", "B", self.base_font_size * 1.6)
        self.cell(0, 10, title, ln=1)
        self.set_font("font_a", "", self.base_font_size)

    def right_section_header(self, title):
        self.set_font("font_a", "B", self.base_font_size * 1.2)
        self.cell(self.right_width, 6, title, ln=1)
        self.set_font("font_a", "", self.base_font_size)

    def progress_bar(self, label, value):
        self.set_font("font_a", "", self.base_font_size)
        self.cell(40, 6, label)
        self.ln(6)

        x = self.get_x() + 1
        y = self.get_y()
        bar_width = 57
        bar_height = 1.5

        self.set_fill_color(200, 200, 200)
        self.rect(x, y, bar_width, bar_height, 'F')

        self.set_fill_color(16, 125, 172)
        self.rect(x, y, bar_width * (int(value) / 100), bar_height, 'F')
        self.ln(6)

    def render(self):
        self.add_page()
        self.name_and_position()

        self.set_left_margin(self.left_margin_indent + self.left_width + 10)
        self.set_xy(self.left_margin_indent + self.left_width + 10, self.top_margin + 10)
        self.render_right_column()

        self.set_left_margin(self.left_margin_indent)
        self.set_y(self.top_margin + 30)
        self.render_left_column()

    def render_left_column(self):
        self.set_left_margin(self.left_margin_indent)
        self.set_xy(self.left_margin_indent, self.get_y())
        self.render_profile()
        self.render_employment_history()

    def render_profile(self):
        self.section_title("Profile", "icons/user.png")
        self.set_font("font_a", "", self.base_font_size * 1.1)
        summary = self.data.findtext('profile/summary') or ""
        self.multi_cell(self.left_width - 10, self.base_font_size*0.6, summary)
        self.ln(5)

    def render_employment_history(self):
        self.section_title("Employment History", "icons/briefcase.png")
        for job in self.data.findall("employment/job"):
            title = job.findtext('title') or ''
            company = job.findtext('company') or ''
            self.set_font("font_a", "B", self.base_font_size * 1.1)
            self.cell(self.left_width - 10, 6, f"{title} at {company}", ln=1)

            self.set_font("font_a", "L", self.base_font_size)
            self.set_text_color(100, 100, 100)
            self.cell(self.left_width - 10, 3, job.findtext("dates") or "", ln=1)
            self.set_font("font_a", "", self.base_font_size * 1.1)
            self.set_text_color(0, 0, 0)
            self.ln(2)
            self.multi_cell(self.left_width - 10, self.base_font_size*0.6, job.findtext("description") or "")
            self.ln(5)

    def render_right_column(self):
        self.render_details()
        self.render_skills()
        self.render_languages()
        self.render_hobbies()

    def render_details(self):
        self.right_section_header("Details")
        details = "\n".join([
            self.data.findtext('personal/location') or '',
            self.data.findtext('personal/phone') or '',
            self.data.findtext('personal/email') or ''
        ])
        self.multi_cell(self.right_width, 5, details)
        self.set_y(self.get_y() + 5)

    def render_skills(self):
        self.right_section_header("Skills")
        for skill in self.data.findall("skills/skill"):
            self.progress_bar(skill.attrib.get("name", ""), skill.attrib.get("level", "0"))

    def render_languages(self):
        self.right_section_header("Languages")
        for lang in self.data.findall("languages/language"):
            self.progress_bar(lang.attrib.get("name", ""), lang.attrib.get("level", "0"))

    def render_hobbies(self):
        self.right_section_header("Hobbies")
        hobbies = []
        for h in self.data.findall("hobbies/hobby"):
            if h.text:
                hobbies.append(h.text)
        if len(hobbies) > 0:
            self.multi_cell(self.right_width, 5, ", ".join(hobbies), align="L")
        elif(self.data.findtext("hobbies/about") != ""):
            self.multi_cell(self.right_width, self.base_font_size*0.5, self.data.findtext("hobbies/about"), align="L")

    def XXfooter(self):
        ascii=""".----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
        | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
        | |     ______   | || | ____   ____  | || |   ______     | || |  ________    | || |  _________   | |
        | |   .' ___  |  | || ||_  _| |_  _| | || |  |_   __ \   | || | |_   ___ `.  | || | |_   ___  |  | |
        | |  / .'   \_|  | || |  \ \   / /   | || |    | |__) |  | || |   | |   `. \ | || |   | |_  \_|  | |
        | |  | |         | || |   \ \ / /    | || |    |  ___/   | || |   | |    | | | || |   |  _|      | |
        | |  \ `.___.'\  | || |    \ ' /     | || |   _| |_      | || |  _| |___.' / | || |  _| |_       | |
        | |   `._____.'  | || |     \_/      | || |  |_____|     | || | |________.'  | || | |_____|      | |
        | |              | || |              | || |              | || |              | || |              | |
        | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
        '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
        """.strip("\n")

        self.set_font("Courier", "", 2)
        self.set_text_color(0, 0, 0)
        
        bottom_y = self.h - 50
        self.set_xy(self.l_margin + 5, bottom_y)

        for line in ascii.split("\n"):
            self.cell(0, 1, line, ln=1)


def main(xml_path='contents.xml', output_pdf='cv_from_xml.pdf'):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    pdf = CVPDF(root)
    pdf.add_font("font_a", "", "fonts/sora/Sora-Regular.ttf", uni=True)
    pdf.add_font("font_a", "B", "fonts/sora/Sora-Bold.ttf", uni=True)
    pdf.add_font("font_a", "L", "fonts/sora/Sora-Light.ttf", uni=True)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.render()
    pdf.output(output_pdf)


if __name__ == "__main__":
    main()