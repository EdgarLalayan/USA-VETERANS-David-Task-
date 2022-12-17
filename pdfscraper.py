from rating_get import rating_get
from active_get import active_get
from subject_get import subject_get
from pdf_to_text import pdf_to_text

if __name__ == '__main__':
    
    pdf_name = input('ENTER PDF NAME : > ')
    data = pdf_to_text(pdf_name)
    RATING_DECISION = rating_get(data)
    ACTIVE_DUTY = active_get(data)
    MEDICAL_CONDNTIONS = subject_get(data)
    print(MEDICAL_CONDNTIONS)    
