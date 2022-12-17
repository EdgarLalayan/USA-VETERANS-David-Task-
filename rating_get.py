

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
            if lst[2].isupper()==True:
                activeDutydict['POA']=lst[1]+' '+lst[2]
                del lst[0]
                continue
            activeDutydict['POA']=lst[1]
            del lst[0]
            continue
        if 'COPY TO' in lst[0] and lst[1].isnumeric() == False :#NAME
            activeDutydict['Veterane_name']=lst[1]
            del lst[0]
            continue
        if True:
            del lst[0]
    return activeDutydict

