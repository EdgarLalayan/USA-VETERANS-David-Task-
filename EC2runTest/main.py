
import fitz
import base64
import io
import argparse
import json

#PDF TO TEXT
def pdf_to_text(b64_string):

    if b64_string[:-4:-1] == 'txt':
        with open(f'{b64_string}', 'rb') as f:
            b64_string = f.read()

    pdf_as_binary_string = base64.b64decode(b64_string)
    binary_stream = io.BytesIO(pdf_as_binary_string)
    datas = []
    pdf_file = fitz.open('pdf', binary_stream)
    for page_num in range(pdf_file.page_count):
        page = pdf_file[page_num]
        page_text = page.get_text()
        data = page_text.replace('\n','|')
        datas.append(data) 
    return datas




#RATING GET
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
    while True:
        if 'LEGACY CODES' in lst[1]:
            break

        if 'CHARACTER OF DISCHARGE' in lst[0] and len(lst[1].split())==1:
            activeDutydict['EOD_Date'] = lst[1]
            activeDutydict['RAD_Date'] = lst[2]
            if (lst[5][:2].isnumeric() ==False)  and 'LEGACY CODES' not in lst[5]:
                activeDutydict['Branch_Service'] = lst[3]+' '+lst[4]
                del lst[4]
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

        
        if 'CHARACTER OF DISCHARGE' in lst[0] and len(lst[1].split())>1:
            s = lst[1].split()
            if len(s) == 3:
                activeDutydict['EOD_Date'] = s[0]
                activeDutydict['RAD_Date'] = s[1]
                activeDutydict['Branch_Service']=s[2]
                activeDutydict['Discharge_Type']=lst[2]
                del lst[1]
                del lst[1]
                info_dics.append(activeDutydict.copy())
                activeDutydict['EOD_Date'] = 'None'
                activeDutydict['RAD_Date'] = 'None'
                activeDutydict['Branch_Service']= 'None'
                activeDutydict['Discharge_Type']= 'None'
                continue
        if True:
            del lst[0]


    return info_dics


#SUBJECT


def subject_get(data):
    
    data = ''.join(data).replace('\n','|')
    try:
        SUBJECT_AREA = data.split('SUBJECT TO COMPENSATION (1.SC)')[1].split('COMBINED EVALUATION FOR COMPENSATION :')[0]
    except:
        SUBJECT_AREA = data.split('SUBJECT TO COMPENSATION (1. SC)')[1].split('COMBINED EVALUATION FOR COMPENSATION :')[0]
    
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

    for i in lst:
        if i =='' or i ==' ':
            lst.remove(i)

    while True:
        if len(lst)==0:
            res['Description'] = res['Description'][:121].lstrip().rstrip()
            res1 = res.copy()
            list_of_dict.append(res1)
            break
        if lst[0].strip()=='':
            del lst[0]
            continue

        if (lst[0][:4].isnumeric() and len(lst[0].strip()) == 4 or lst[0][:4].isnumeric() and len(lst[0].strip()) == 9) and res['Code']!='':
            res['Description'] = res['Description'][:121].lstrip().rstrip()
            res1 = res.copy()
            list_of_dict.append(res1)
            res['Code'] = lst[0]
            res['Description']=''
            res['PercentageDate']=''
            c+=1
            del lst[0]
            continue
        
        if lst[0][:4].isnumeric() and len(lst[0].strip()) == 4 or lst[0][:4].isnumeric() and len(lst[0].strip()) == 9 :#start
            res['Code']=lst[0]
            del lst[0]
            c+=1
            continue
        if lst[0].lstrip().split()[0].isupper() == True and res['Description']=='':
            res['Description'] = lst[0]
            del lst[0]
            c+=1
            continue
        if lst[0].lstrip().split()[0].isupper() == True and res['Description']!='':
            res['Description'] = res['Description']+' '+lst[0].lstrip().rstrip()
            del lst[0]
            c+=1
            continue
        if 'from' in lst[0] and res['PercentageDate']=='':
            res['PercentageDate'] = lst[0].lstrip().rstrip()
            del lst[0]
            c+=1
            continue
        if 'from' in lst[0] and res['PercentageDate']!='':
            res['PercentageDate'] = res['PercentageDate']+' '+lst[0].lstrip().rstrip()
            del lst[0]
            c+=1
            continue
        if True:
            if res['Description'].count('[') % 2 !=0 and ']' in lst[0]:
                res['Description'] = res['Description']+' '+lst[0].lstrip().rstrip()
            del lst[0]
            c+=1
            continue

    return list_of_dict


# from pdf_to_text import pdf_to_text
# data = pdf_to_text('info8')
# for i  in subject_get(data):
#     print(i)


# from pdf_to_text import pdf_to_text
# data = pdf_to_text('info6')
# for i in active_get(data):
#     print(i)





def create_data_for_json(rating_res,active_res,subject_res):
    js = {
        'Veteran Name':rating_res['Veterane_name'],
        'VA File Number':rating_res['Va_File_Number'],
        'Social Security Number':rating_res['SS_Number'],
        'POA':rating_res['POA'],
        'Service Dates':active_res,
        'Conditions':subject_res   
    }
    with open('file.json', 'w') as f:
        json.dump(js, f)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--argument', required=True)
    args = parser.parse_args()
    argument_value = args.argument

    data = pdf_to_text(argument_value)
    rating_get_res = rating_get(data)
    active_get_res = active_get(data)
    subject_get_res = subject_get(data)
    create_data_for_json(rating_get_res,active_get_res,subject_get_res)

    with open('file.json', 'r') as f:
        d  = json.load(f)

        # pretty-print the JSON data
        print(json.dumps(d, indent=2))
