



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





