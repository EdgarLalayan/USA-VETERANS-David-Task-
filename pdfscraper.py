from rating_get import rating_get
from active_get import active_get
from subject_get import subject_get
from pdf_to_text import pdf_to_text
from simple_colors import *


if __name__ == '__main__':
    
    pdf_name = input(green('Please, enter the pdf file name : > '))
    data = pdf_to_text(pdf_name)
    RATING_DECISION = rating_get(data)
    ACTIVE_DUTY = active_get(data)
    MEDICAL_CONDNTIONS = subject_get(data)
    print(green('==========RETING DESCITION==========', ['bold']))
    for i in RATING_DECISION.keys():
        print(yellow(f'{i}  {RATING_DECISION[i]}'))
    print(green('==========MEDICAL CONDITIONS==========', ['bold']))
    for i in ACTIVE_DUTY:
        print(yellow(i))
    print(green('==========SERVICE DATES==========', ['bold']))
    for i in MEDICAL_CONDNTIONS:
        print(yellow(i))
    
print(green('Service Dates', ['bold']))
