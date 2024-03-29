
import fitz
import base64
import io
import argparse
import json
import re




def pdf_to_b64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    pdf_b64_string = base64.b64encode(pdf_data).decode("utf-8")

    return pdf_b64_string




def pdf_to_text(pdf_path):
    if pdf_path.endswith('.txt'):
        with open(pdf_path, 'r') as f:
            b64_string = f.read()
    else:
        b64_string = pdf_to_b64(pdf_path)

    pdf_as_binary_string = base64.b64decode(b64_string)
    binary_stream = io.BytesIO(pdf_as_binary_string)
    datas = []
    pdf_file = fitz.open(stream=binary_stream, filetype='pdf')
    for page_num in range(pdf_file.page_count):
        page = pdf_file[page_num]
        page_text = page.get_text()
        data = page_text.replace('\n', '|')
        datas.append(data)

    return datas


#RATING GET
def rating_get(data):
    data = ''.join(data).replace('\n','|')

    lst = data.split('|')

    activeDutydict = {
        'Veterane_name':'None',
        'Va_File_Number':'None',
        'SOCIAL SECURITY NR':'None',
        'POA':'None',
        'CLIENT_CASPIO_FK':'',
        'HEADER_DATE':''
        }
    
    lst  = [i for i in lst if i]
    if 'Rating Decision' not in lst:
        if 'COPY TO' not in  lst[-1] and '/'  in lst[-1]:   
            CLIENT_CASPIO_FK = lst[-2]
            activeDutydict['CLIENT_CASPIO_FK'] = CLIENT_CASPIO_FK
            activeDutydict['HEADER_DATE'] = lst[-1]
        if 'COPY TO' not in  lst[-1] and '/' not in lst[-1]:   
            CLIENT_CASPIO_FK = lst[-1]
            activeDutydict['CLIENT_CASPIO_FK'] = CLIENT_CASPIO_FK
        



    if 'Rating Decision'  in lst:
        #get CLIENT_CASPIO_FK
        if 'COPY TO' not in  lst[-1] and '/' not in lst[-1]:   
            CLIENT_CASPIO_FK = lst[-1]
            activeDutydict['CLIENT_CASPIO_FK'] = lst[-1]
        if 'COPY TO' not in  lst[-1] and '/'  in lst[-1]:   
            CLIENT_CASPIO_FK = lst[-2]
            activeDutydict['CLIENT_CASPIO_FK'] = CLIENT_CASPIO_FK
            activeDutydict['HEADER_DATE'] = lst[-1]
        #get HEADER DATE
        for i in lst:
            if 'Page' in i :
                h = lst.index(i)
                h = lst[h+1]
                if h[0].isnumeric() and '/' in h:
                    activeDutydict['HEADER_DATE'] = h.strip()
    #remove ccfk 
    lst = [i for i in lst if CLIENT_CASPIO_FK not in i]
    while True:
        try :
            if len(lst) ==0:
                break
            #VETERANE NAME
            if 'NAME OF VETERAN' in lst[0] and 'VA FILE NUMBER' not in lst[1]:
                activeDutydict['Veterane_name'] = lst[1].rstrip()
                if 'VA FILE NUMBER' not in lst[2]:
                    activeDutydict['Veterane_name'] = activeDutydict['Veterane_name']+' '+lst[2].rstrip()
                del lst[0]
                continue
            #VA NUMBER
            if 'VA FILE NUMBER' in lst[0] and 'SOCIAL SECURITY NR' not in lst[1]:
                activeDutydict['Va_File_Number'] = lst[1]
                del lst[0]
                continue
            #SOCIAL NUMBER
            if 'SOCIAL SECURITY NR' in lst[0] and 'POA' not in lst[1]:
                activeDutydict['SOCIAL SECURITY NR'] = lst[1]
                del lst[0]
                continue
            #POA
            if 'POA' in lst[0] and 'COPY TO' not in lst[1] and '/' not in lst[1]:
                activeDutydict['POA'] = lst[1].rstrip()
                if 'COPY TO' not in lst[2] and '/' not in lst[2] :
                    activeDutydict['POA'] = activeDutydict['POA'] + ' ' + lst[2].rstrip()
                if 'COPY TO' not in lst[3] and '/' not in lst[3]:
                    activeDutydict['POA'] = activeDutydict['POA'] + ' ' + lst[3].rstrip()
            
            del lst[0]
        except IndexError:
            break

    return activeDutydict  


#ACTIVE GET
def active_get(data):
    data = ''.join(data).replace('\n','|')
    lst = data.split('|')
    activeDutydict = {
        'EOD_Date':'None',
        'RAD_Date':'None',
        'Branch_Service':'None',
        'Discharge_Type':'None',
        }
    info_dics = []
    checker = False
    for row in lst:
        if row.strip() == '':
            del lst[lst.index(row)]
        if 'CHARACTER OF' in row:
            lst = lst[lst.index(row):]
            checker = True
    if checker == False:
        return 'None'
    
    pattern_date = r'\d{2}/\d{2}/\d{4}'
    while True:
        if 'LEGACY CODES' in lst[1]:
            break
        
        if  '/' not in lst[1] and ('/'and'LEGACY')  not in lst[2]:
            activeDutydict['EOD_Date'] = ' '
            activeDutydict['RAD_Date'] = ' '
            activeDutydict['Branch_Service'] = lst[1]
            activeDutydict['Discharge_Type'] = lst[2]
            del lst[1]
            del lst[1]
            info_dics.append(activeDutydict.copy())
            activeDutydict['EOD_Date'] = 'None'
            activeDutydict['RAD_Date'] = 'None'
            activeDutydict['Branch_Service']= 'None'
            activeDutydict['Discharge_Type']= 'None'
            continue
        if  len(lst[1].split()) == 1 and '/' in lst[1] and '/' in lst[2] and len(lst[2].split()) == 1:
            activeDutydict['EOD_Date'] = lst[1]
            activeDutydict['RAD_Date'] = lst[2]
            #BRANCH 2x
            if (lst[5][:2].isnumeric() ==False)  and 'LEGACY CODES' not in lst[5]:
                activeDutydict['Branch_Service'] = lst[3]+' '+lst[4]
                del lst[4]
                #BRANCH 3x
                if (lst[5][:2].isnumeric() ==False)  and 'LEGACY CODES' not in lst[5]:
                    activeDutydict['Branch_Service'] = activeDutydict['Branch_Service']+' '+lst[4]
                    del lst[4]

            #BRANCH 1x
            else:
                activeDutydict['Branch_Service'] = lst[3]
            
            activeDutydict['Discharge_Type'] = lst[4]
            del lst[1]
            del lst[1]
            del lst[1]
            del lst[1]
            info_dics.append(activeDutydict.copy())
            activeDutydict['EOD_Date'] = 'None'
            activeDutydict['RAD_Date'] = 'None'
            activeDutydict['Branch_Service'] = 'None'
            activeDutydict['Discharge_Type'] = 'None' 
            continue     

        #broken pdfs                                       
        if  len(lst[1].split()) > 1 or len(lst[2].split()) > 1:

            s = lst[1].split()
            
            if  (re.search(pattern_date, lst[2]) and len(lst[2].split()) > 1) and  (re.search(pattern_date, lst[1]) and len(lst[1].split()) == 1):
                activeDutydict['EOD_Date'] = lst[1].strip()
                activeDutydict['RAD_Date'] = re.search(pattern_date, lst[2]).group().strip()
                activeDutydict['Branch_Service']= re.sub(pattern_date, '',lst[2]).strip()
                activeDutydict['Discharge_Type']=lst[3].strip()
                del lst[1]
                del lst[1]
                del lst[1]

            #if Discharge_Type in lst2 and lens == 3
            if len(s) == 3 and '/' in s[0] and '/' in s[1]:
                activeDutydict['EOD_Date'] = s[0].strip()
                activeDutydict['RAD_Date'] = s[1].strip()
                activeDutydict['Branch_Service']=s[2].strip()
                activeDutydict['Discharge_Type']=lst[2].strip()
                del lst[1]
                del lst[1]

            # all in one row and len brach == 1
            if (len(s) == 4 and  '/' in s[0] and '/' in s[1]) and ('/' in lst[2] or 'LEGACY CODES' in lst[2]):
                activeDutydict['EOD_Date'] = s[0].strip()
                activeDutydict['RAD_Date'] = s[1].strip()
                activeDutydict['Branch_Service']=s[2].strip()
                activeDutydict['Discharge_Type']=s[3].strip()
                del lst[1]

            # if Discharge_Type in lst2
            if len(s) == 4 and  '/' in s[0] and '/' in s[1] and '/' not in lst[2]  :
                activeDutydict['EOD_Date'] = s[0]
                activeDutydict['RAD_Date'] = s[1]
                activeDutydict['Branch_Service']=s[2]+' '+s[3]
                activeDutydict['Discharge_Type']=lst[2]
                del lst[1]
                del lst[1]
            # All in one row and len branch == 2
            if len(s) == 5 and  '/' in s[0] and '/' in s[1]:
                activeDutydict['EOD_Date'] = s[0]
                activeDutydict['RAD_Date'] = s[1]
                activeDutydict['Branch_Service']=s[2]+' '+s[3]
                activeDutydict['Discharge_Type']=s[4]
                del lst[1]

            info_dics.append(activeDutydict.copy())
            activeDutydict['EOD_Date'] = 'None'
            activeDutydict['RAD_Date'] = 'None'
            activeDutydict['Branch_Service']= 'None'
            activeDutydict['Discharge_Type']= 'None'
            continue

        
        del lst[0]


    return info_dics


#SUBJECT
def subject_get(data,client_caspio_num=''):
    data = ''.join(data).replace('\n','|')
    SUBJECT_TO = ''
    COMBINED_TO = ''


    for i in data.split('|'):
        if SUBJECT_TO != '' and COMBINED_TO != '':
            break
        if 'SUBJECT TO COMPENSATION' in i:
            SUBJECT_TO = i
        if 'COMBINED EVALUATION FOR COMPENSATION' in i:
            COMBINED_TO = i
    if SUBJECT_TO == '' or COMBINED_TO == '':
        return "None"

    SUBJECT_AREA = data.split(f'{SUBJECT_TO}')[1].split(f'{COMBINED_TO}')[0]
    lst = SUBJECT_AREA.split('|')
    lst = [i.strip() for i in lst if i.strip() != '']

    #REMOVE CASPIO
    caspio = rating_get(data)['CLIENT_CASPIO_FK']
    if caspio.strip() != '':
        lst = [i for  i in  lst if caspio not in i]
    

    # del rating -> copy to
    new_lst = []
    while True:
        
        if 'Rating Decision' not in lst:
            for i in lst:
                new_lst.append(i)
            break
        
        if 'Rating Decision' in lst[0]:
            ind1 = lst.index('Rating Decision')
            ind2 = lst.index('COPY TO')
            del lst[ind1:ind2+1]
            continue
        new_lst.append(lst[0])
        del lst[0]
        continue

    lst = new_lst

    
    #SUBJECT 
    new = '|'.join(lst)
    lst = new.split('|')
    list_of_dict = []
    res = {
        'Code':'',
        'Description':'',
        'PercentageDate':''
    }

    while True:
        if len(lst)==0:
            res['Description'] = res['Description'][:257].lstrip().rstrip()
            res1 = res.copy()
            list_of_dict.append(res1)
            break
        if lst[0].strip()=='':
            del lst[0]
            continue
        
        # next code
        if lst[0].strip()[:4].isnumeric() and res['Code']!='':
            res['Description'] = res['Description'][:257].strip()
            res1 = res.copy()
            list_of_dict.append(res1)

            code_row = lst[0].strip().split()
            if len(code_row) == 1:
                res['Code'] = lst[0]
                res['Description']=''
                res['PercentageDate']=''
                del lst[0]
                continue
            if len(code_row) > 1:
                res['Code'] = code_row[0]
                desc = ' '.join(code_row[1:])
                res['Description'] = desc
                res['PercentageDate']=''
                del lst[0]
                continue
        
        #Code
        # if code & desc in one row
        if lst[0][:4].isnumeric() and len(lst[0].strip().split()) > 1 :
            row_code = lst[0].split()
            if row_code[0][:4].isnumeric():
                res['Code']= row_code[0]
                desc = ' '.join(row_code[1:])
                res['Description'] = desc
                del lst[0]
                continue
        if len(lst[0].strip().split()) == 1:
            if lst[0][:4].isnumeric(): #and len(lst[0].strip()) == 4 or lst[0][:4].isnumeric() and len(lst[0].strip()) == 9 :#start
                res['Code']=lst[0]
                del lst[0]
                continue

        #Description
        if lst[0].lstrip().split()[0].isupper() == True and res['Description']=='':
            res['Description'] = lst[0]
            del lst[0]
            continue
        if (lst[0].lstrip().split()[0].isupper()  == True or  ('['or']') in lst[0])  and res['Description']!='' :
            res['Description'] = res['Description']+' '+lst[0].strip()
            del lst[0]
            continue
        if res['Description']!= '' and lst[0].strip()[-1] == ']' and res['Description'].count('[') != res['Description'].count(']'):
            res['Description'] = res['Description']+' '+lst[0].strip()
            del lst[0]
            continue
        


        #First percent
        if 'from' in lst[0] and res['PercentageDate']=='':
            res['PercentageDate'] = lst[0].strip()
            del lst[0]
            continue
        #Second percent
        if 'from' in lst[0] and res['PercentageDate']!='':
            res['PercentageDate'] = res['PercentageDate']+' '+lst[0].lstrip().rstrip()
            del lst[0]
            continue

        if res['Description'].count('[') % 2 !=0 and ']' in lst[0]:
            res['Description'] = res['Description']+' '+lst[0].lstrip().rstrip()
        del lst[0]
        continue
    


    #Percent arraw
    for d in list_of_dict:
        date_lst = []
        date_perc = {'percent':'None','date':'None'}
        row = d['PercentageDate'].split()
        while True:
            if len(row)==0:
                if date_perc['percent'] !='None':
                    date_lst.append(date_perc.copy())
                    break
                break
            if date_perc['date'] != 'None' and date_perc['percent'] != 'None':
                date_lst.append(date_perc.copy())
                if 'End_Date' in date_perc.keys():
                    date_perc['End_Date'] = 'None'
                date_perc['date'] = 'None'
                date_perc['percent'] = 'None'
                if len(row) == 0:
                    break
                continue

            if '%' in row[0]:
                date_perc['percent']=row[0].replace('%','')
                del row[0]
                continue
            if row[0].count('/') == 2 and 'to' in row:
                to_ind = row.index('to')
                date_perc['date'] = row[to_ind-1]
                date_perc['End_Date'] = row[to_ind+1]
                del row[0]
                del row[to_ind]
                continue

            if  row[0].count('/') == 2:
                row[0] = row[0].replace(',','')
                date_perc['date'] = row[0]
                del row[0]
                continue
            del row[0]
        d['PercentageDate']=date_lst
    
    #LEFT OR RIGHT
    for row in list_of_dict:
        desc = row['Description']
        if ('LEFT' in desc and 'RIGHT' in desc) or ('Left' in desc and 'Right' in desc) :
            if desc.index('LEFT') < desc.index('RIGHT'):
                row['Left_or_Right_KW'] = 'LEFT'
                continue
            if desc.index('LEFT') > desc.index('RIGHT'):
                row['Left_or_Right_KW'] = 'RIGHT'
                continue
        if 'LEFT' in desc or 'Left' in desc:
            row['Left_or_Right_KW'] = 'LEFT'
            continue
        if 'RIGHT' in desc or 'Right' in desc:
            row['Left_or_Right_KW'] = 'RIGHT'
            continue

    return list_of_dict


#GET EVALUTION
def evaluation(data):

    data = ''.join(data).replace('\n','|')
    if 'SPECIAL MONTHLY COMPENSATION' not in data:
        evaluation_area = data.split('COMBINED EVALUATION FOR COMPENSATION')[1]
        evaluation_area = ''.join(evaluation_area).split('|NOT SERVICE CONNECTED')[0]
        evaluation_area = ''.join(evaluation_area).split('|')
        evaluation_res = [i.strip() for i in evaluation_area if 'from' in i ]
        return evaluation_res
    if 'SPECIAL MONTHLY COMPENSATION' in data:
        evaluation_area = data.split('COMBINED EVALUATION FOR COMPENSATION')[1]
        evaluation_area = ''.join(evaluation_area).split('|SPECIAL MONTHLY')[0]
        evaluation_area = ''.join(evaluation_area).split('|')
        evaluation_res = [i.strip() for i in evaluation_area if 'from' in i ]
        return evaluation_res


#GET NO COMPESATION
def noCompesation(data):
    list_of_dict = []    
    data = ''.join(data).replace('\n','|')
    lst = data.split('|')
    lst = [i for i in lst if i != ' ' and i != '']
    #start no comp area

    while True:
        try:# if NOT SERVICE CONNECTED not in  data:return None
            if 'NOT SERVICE CONNECTED' in lst[0]:
                del lst[0]
                break
        except IndexError:
            return list_of_dict
        del lst[0]

    caspio = rating_get(data)['CLIENT_CASPIO_FK']

    #REMOVE CASPIO
    if caspio.strip() != '':
        lst = [i.strip() for  i in  lst if caspio not in i and i != ''] 

    new_lst = []
    while True:
        
        if 'Rating Decision' not in lst:
            for i in lst:
                new_lst.append(i)
            break
        
        if 'Rating Decision' in lst[0]:
            ind2 = lst.index('COPY TO')
            del lst[:ind2+1]
            continue
        new_lst.append(lst[0])
        del lst[0]
        continue

    lst = new_lst

    res ={
        'Code':'',
        'Description':''
    }
    while True:

        #STOP ITER
        if len(lst)==0:
            if (res['Code'] and res['Code']) != '':
                res_copy = res.copy()
                list_of_dict.append(res_copy)
            break

        if 'Not Service' in lst[0]:
            res_copy = res.copy()
            list_of_dict.append(res_copy)
            res['Code']=''
            res['Description']=''
            del lst[0]
            continue
        
        # #STOP KEYS
        # if 'ANCILLARY' in lst[0] or 'TREATMENT PURPOSES ONLY' in lst[0] or 'NOT SERVICE CONNECTED' in lst[0] or '____' in lst[0]:
        #     break
        
        strings_to_check = ('TREATMENT PURPOSES ONLY', 'NOT SERVICE CONNECTED', 'DEFERRED ISSUES', '___')

        if any(string in lst[0] for string in strings_to_check):
            break

        #Code
        # if code & desc in one row
        if lst[0][:4].isnumeric() and len(lst[0].strip().split()) > 1 :
            row_code = lst[0].split()
            if row_code[0][:4].isnumeric():
                res['Code']= row_code[0]
                desc = ' '.join(row_code[1:])
                res['Description'] = desc
                del lst[0]
                continue
        if len(lst[0].strip().split()) == 1:
            if lst[0][:4].isnumeric(): #and len(lst[0].strip()) == 4 or lst[0][:4].isnumeric() and len(lst[0].strip()) == 9 :#start
                res['Code']=lst[0]
                del lst[0]
                continue

        #DESCRIPTION
        if (lst[0].lstrip().split()[0].isupper() == True and res['Description']== '') and res['Code'] != '':
            res['Description'] = lst[0].rstrip()
            del lst[0]
            continue
        if ((lst[0].lstrip().split()[0].isupper() == True  or  ('[' or ']'or '(' or ')') in lst[0]) and res['Description']!='') and res['Code'] != '':
            res['Description'] = res['Description']+' '+lst[0].strip()
            del lst[0]
            continue



        if res['Description'].count('[') % 2 !=0 and ']' in lst[0]:
            res['Description'] = res['Description']+' '+lst[0].strip()
        del lst[0]
        continue



    #LEFT OR RIGHT
    for row in list_of_dict:
        desc = row['Description']
        if ('LEFT' in desc and 'RIGHT' in desc) or ('Left' in desc and 'Right' in desc) :
            if desc.index('LEFT') < desc.index('RIGHT'):
                row['Left_or_Right_KW'] = 'LEFT'
                continue
            if desc.index('LEFT') > desc.index('RIGHT'):
                row['Left_or_Right_KW'] = 'RIGHT'
                continue
        if 'LEFT' in desc or 'Left' in desc:
            row['Left_or_Right_KW'] = 'LEFT'
            continue
        if 'RIGHT' in desc or 'Right' in desc:
            row['Left_or_Right_KW'] = 'RIGHT'
            continue

    return list_of_dict


#JSON FILE CREATOR
def create_data_for_json(rating_res,active_res,subject_res,no_compes):
    js = {
        'Veteran Name':rating_res['Veterane_name'],
        'VA File Number':rating_res['Va_File_Number'],
        'Social Security Number':rating_res['SOCIAL SECURITY NR'],
        'POA':rating_res['POA'],
        'CLIENT_CASPIO_FK':rating_res['CLIENT_CASPIO_FK'],
        'HEADER_DATE':rating_res['HEADER_DATE'],
        'Service Dates':active_res,
        'Compensation':subject_res,   
        'No Compensation':no_compes
    }
    with open('file.json', 'w') as f:
        json.dump(js, f)






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--argument', required=False)
    args = parser.parse_args()
    argument_value = args.argument

    data = pdf_to_text(argument_value)

    rating_get_res = rating_get(data)
    active_get_res = active_get(data)
    CLIENT_CASPIO_FK = rating_get_res['CLIENT_CASPIO_FK']
    subject_get_res = subject_get(data,CLIENT_CASPIO_FK)
    #evaluation_get_res = evaluation(data)
    no_compes_get_res = noCompesation(data)
    create_data_for_json(rating_get_res,active_get_res,subject_get_res,no_compes_get_res)
    with open('file.json', 'r') as f:
        d  = json.load(f)
        #pretty-print the JSON data
        print(json.dumps(d, indent=2))



# data = pdf_to_text('/Users/edgarlalayan/Desktop/Veteran /parser1.4/No SC/2NKTLYHC.pdf')
# print(data)
# print(json.dumps(rating_get(data), indent=2))
# print(json.dumps(noCompesation(data), indent=2))
# print(json.dumps(active_get(data), indent=2))
# print(json.dumps(subject_get(data), indent=2))
