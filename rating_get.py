

def rating_get(data):
    data = ''.join(data).replace('\n','|')

    lst = data.split('|')

        

    activeDutydict = {
        'Veterane_name':'None',
        'Va_File_Number':'None',
        'SS_Number':'None',
        'POA':'None',
        }
    while True:
        if  activeDutydict['POA']!='None' and activeDutydict['Veterane_name']!='None':#Petqa avelacnel SSnumber and...
              break
        if 'POA'in lst[0]:#POA
            poa = ''
            while True:#POA
                if 'COPY TO' in lst[1]:
                    activeDutydict['POA'] = poa
                    break
                if lst[1].strip() == '':
                    del lst[1]
                    continue
                if lst[1].isupper():
                    if activeDutydict['POA']!='None':
                        poa += ' '
                    poa+=' '+lst[1]
                    del lst[1] 
            while True:#NAME
                if 'COPY TO' in lst[-1] and len(lst)==2:
                    activeDutydict['Veterane_name'] = ''
                    break
                if 'ACTIVE DUTY' in lst[2] or lst[2][:4].isnumeric() == True:
                    activeDutydict['Veterane_name'] = ''
                    break
                if lst[2].strip() == '':
                    del lst[2]
                    continue
                if 'Service' not in lst[2] and 'Static' not in lst[2] and lst[2][0].isnumeric()==False:
                    activeDutydict['Veterane_name'] = lst[2]
                    break
                else:
                    activeDutydict['Veterane_name'] = ''
                    break

        if True:
            del lst[0]
    return activeDutydict
 
# from pdf_to_text import pdf_to_text
# data = pdf_to_text('info8')
# print(rating_get(data))