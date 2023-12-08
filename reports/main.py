from jiratools import JiraTools
import requests
import traceback
#from dotenv import load_dotenv
from pathlib import os

FLOW_UPSTREAM = 'upstream'
FLOW_DOWNSTREAM = 'downstream'
GROUP_PO = 'po'
GROUP_TEAM = 'team'


def report(request, flow, grouper, data_update = True):
    try:

        # Tente obter dados da sessão
        resultJQL = request.session.get('resultJQL')

        if resultJQL is None or data_update:
            jira = JiraTools(request)
            jira.connect()
            
            # Get the information of the child Issues
            jql = str(os.getenv('JQL'))
            resultJQL = jira.search_with_pagination(jql_query=jql)
            # Armazene os dados na sessão
            request.session['resultJQL'] = resultJQL

    except requests.exceptions.HTTPError as e:
        # Handling for the specific HTTPError error
        print("Ocorreu um erro HTTP:", e)
        # Perform additional treatment actions if necessary
        # Redirect to a success page or another page
        return e

    status_upstream = ['business definition', 'under review', 'waiting for approval',
                       'to do', 'kick off', 'work in progress']
    status_downstream = ['in progress', 'ship', 'tweak']

    status_others = ['done', 'reject', 'open', 'backlog', 'selected for development', 'planning', 
                     'waiting for customer', 'resolved', 'waiting for support', 'pending']

    initiatives = []
    initiatives_up = []
    initiatives_down = []
    epics = []
    epics_up = []
    epics_down = []
    service_request_up = []

    # Lê o resultado e separa as Iniciativas e Épicos e faz a classificação de é Upstream ou Downstream
    count = 0
    for issue in resultJQL:
        issue_type = issue['fields']['issuetype']['name']
        issue_status = issue['fields']['status']['name'].lower()
        count += 1
        
        if issue_type == 'Initiative':
            initiatives.append(issue)
            if issue_status in status_upstream:
                initiatives_up.append(issue)
            elif issue_status in status_downstream:
                initiatives_down.append(issue)
            elif issue_status not in status_others:
                print('Status não mapeado: ', issue_status)
        elif issue_type == 'Epic':
            epics.append(issue)
            if issue_status in status_upstream:
                epics_up.append(issue)
            elif issue_status in status_downstream:
                epics_down.append(issue)
            elif issue_status not in status_others:
                print('Status não mapeado: ', issue_status)
        else:
            if issue_status in status_upstream:
                service_request_up.append(issue)
            elif issue_status in status_downstream:
                pass
            elif issue_status not in status_others:
                print('Status não mapeado: ', issue_status)

             
    print(count) 

    try:

        if flow == FLOW_UPSTREAM:
            initiatives = initiatives_up
            epics = epics_up
            service_request = service_request_up
        else:
            initiatives = initiatives_down
            epics = epics_down
            service_request = None

        data_dict = report_builder(initiatives, epics, grouper, service_request)
        
    except Exception as e:
        # Generic handling for other exceptions that may occur
        # Imprimir o traceback completo
        traceback.print_exc()
        print("Ocorreu um erro:", e)
        return e

    return data_dict

def report_builder(initiatives, epics, group, service_request=None):
    data_dict = {}
    
    # separa os épicos em upstream por team e pega as Iniciativas Pai
    # user_dict = {agrupador:[{keyIni:int, fieldsIni:{}, epics:[]}]}
    for epic in epics:
        group_by = 'Não Informado'

        if group == GROUP_TEAM:    
            if epic['fields']['customfield_10001'] is not None:
                group_by = epic['fields']['customfield_10001']['name']
        else:
            if epic['fields']['assignee'] is not None:
                group_by = epic['fields']['assignee']['displayName']

 
        if group_by in data_dict:
            encontraId = False
            for disct in data_dict[group_by]:
                if disct['keyIni'] == epic['fields']['parent']['key']:
                    disct['epics'].append(epic)
                    encontraId = True
                    break

            if not encontraId:
                data_dict[group_by].append(
                    {'keyIni': epic['fields']['parent']['key'],
                     'fieldsIni': epic['fields']['parent']['fields'],
                     'epics': [epic]
                     }
                )

        else:
            data_dict[group_by] = [{'keyIni': epic['fields']['parent']['key'],
                                  'fieldsIni': epic['fields']['parent']['fields'],
                                  'epics': [epic]
                                  }]
    


    print('--------------------------')
    print(data_dict.keys())
    print('--------------------------')

    print('Initiative Upstream')

    #Adiciona as Iniciativas que estão em downstream mas nao tem épico sendo executado 
    for initiative in initiatives:
        #print(initiative['fields']['summary'])
        group_by = 'Não Informado'

        if group == GROUP_TEAM:    
            if initiative['fields']['customfield_10001'] is not None:
                group_by = initiative['fields']['customfield_10001']['name']
        else:
            if initiative['fields']['assignee'] is not None:
                group_by = initiative['fields']['assignee']['displayName']
        
        if group_by in data_dict:
            encontraId = False
            for disct in data_dict[group_by]:
                if disct['keyIni'] == initiative['key']:
                    encontraId = True
                    break

            if not encontraId:
                data_dict[group_by].append(
                    {'keyIni': initiative['key'],
                     'fieldsIni': initiative['fields'],
                     'epics': []
                     }
                ) 

        else:
            data_dict[group_by] = [{'keyIni': initiative['key'],
                                  'fieldsIni': initiative['fields'],
                                  'epics': []
                                  }]
            
    #Adiciona os Service requests que estão em upstream
    if service_request is not None and group == GROUP_PO:
        for service_request in service_request:
            assigne = "SEM PO"
            if service_request['fields']['assignee'] is not None:
                assigne = service_request['fields']['assignee']['displayName']
            

            if assigne in data_dict:
                data_dict[assigne].append(
                    {'keyIni': service_request['key'],
                        'fieldsIni': service_request['fields'],
                        'epics': []
                        }
                ) 

            else:
                data_dict[assigne] = [{'keyIni': service_request['key'],
                                    'fieldsIni': service_request['fields'],
                                    'epics': []
                                    }]

    # for user_ini in data_dict:
    #     print('==========================')
    #     print(user_ini) 
    #     print('==========================')

    #     for ini in data_dict[user_ini]:
    #         print( ini['keyIni']," - ", ini['fieldsIni']['summary'],'-->', ini['fieldsIni']['status']['name'] )

    #         for iniepic in ini['epics']:
    #             print( '     epic:',iniepic['key']," - ", iniepic['fields']['summary'], '-->', iniepic['fields']['status']['name'])

    #     print('---------------------------------------')

    return data_dict



