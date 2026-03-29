from fpdf import FPDF
import tempfile
import datetime

def create_pdf_report(predicted_class, confidence, plan, image):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(200, 10, txt="Corn Doctor Pro - Diagnostic Report", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 5, txt=f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}", ln=True, align='R')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt=f"Diagnosis: {plan.get('name', predicted_class)}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 8, txt=f"Pathogen: {plan.get('scientific_name', 'N/A')}", ln=True)
    pdf.cell(200, 8, txt=f"AI Confidence: {confidence:.2f}%", ln=True)
    pdf.ln(5)
    
    if image:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            if image.mode in ('RGBA', 'P'): image = image.convert('RGB')
            image.thumbnail((300, 300))
            image.save(tmp.name)
            pdf.image(tmp.name, x=10, w=70)
            pdf.ln(5)
            
    current_y = max(pdf.get_y(), 80)
    pdf.set_y(current_y + 5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Symptoms:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 6, txt=plan.get('symptoms', 'N/A'))
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Recommended Treatment:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 6, txt=f"Prevention:\n{plan.get('prevention', 'N/A')}\n\nOrganic:\n{plan.get('organic', 'N/A')}\n\nChemical:\n{plan.get('chemical', 'N/A')}")
    
    pdf.set_y(-50) 
    pdf.set_font("Times", 'I', 16)
    pdf.cell(190, 8, txt="karan kumawat", ln=True, align='R')
    pdf.line(140, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 5, txt="Founder & Chairman", ln=True, align='R')
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(190, 5, txt="Corn Doctor AI Diagnostics", ln=True, align='R')

    return pdf.output(dest='S').encode('latin-1')