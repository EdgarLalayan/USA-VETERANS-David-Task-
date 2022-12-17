

def subject_get(data):
    
    data = ''.join(data).replace('\n','|')
    SUBJECT_AREA = data.split('SUBJECT TO COMPENSATION (1.SC)')[1].split('COMBINED EVALUATION FOR COMPENSATION :')[0]
    lst = SUBJECT_AREA.split('|')
    while True:
        for i in lst:
            if 'Rating Decision' in i :
                ind = lst.index('Rating Decision')
                del lst[ind+1:lst.index('COPY TO')+2]
                del lst[ind]
        if 'Rating Decision' not in lst:
            del lst[0]
            break
    #SUBJECT 
    new = '|'.join(lst)
    lst = new.split('|')
    list_of_dict = []
    res = {
        'Code':'',
        'Description':'',
        'PercentageDate':''
    }
    c = 0 
    if lst[0] == ' ' or lst[0] == '':
        del lst[0]
        
    while True:

        if len(lst)==0:
            res['Description'] = res['Description'][:121]
            res1 = res.copy()
            list_of_dict.append(res1)
            break
        if (lst[0].isnumeric() and len(lst[0]) == 4 or lst[0][:4].isnumeric() and len(lst[0]) == 9) and res['Code']!='':
            res['Description'] = res['Description'][:121]
            res1 = res.copy()
            list_of_dict.append(res1)
            res['Code'] = lst[0]
            res['Description']=''
            res['PercentageDate']=''
            c+=1
            del lst[0]
            continue
        
        if lst[0].isnumeric() and len(lst[0]) == 4 or lst[0].isnumeric() and len(lst[0]) == 9 :#start
            res['Code']=lst[0]
            del lst[0]
            c+=1
            continue
        if lst[0].isupper() == True and res['Description']=='':
            res['Description'] = lst[0]
            del lst[0]
            c+=1
            continue
        if lst[0].isupper() == True and res['Description']!='':
            res['Description'] = res['Description']+' '+lst[0]
            del lst[0]
            c+=1
            continue
        if 'from' in lst[0] and res['PercentageDate']=='':
            res['PercentageDate'] = lst[0]
            del lst[0]
            c+=1
            continue
        if 'from' in lst[0] and res['PercentageDate']!='':
            res['PercentageDate'] = res['PercentageDate']+' '+lst[0]
            del lst[0]
            c+=1
            continue
        if True:
            del lst[0]
            c+=1
            continue

    return list_of_dict

