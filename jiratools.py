from atlassian import Jira
from dotenv import load_dotenv
from pathlib import os
import urllib3
from users.models import Config
from django.contrib.auth import get_user
from reports import main
from cryptography.fernet import InvalidToken

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Carregar variáveis de ambiente de um arquivo .env
load_dotenv('.env')


class JiraTools(Jira):
    def __init__(self, request):

        user = get_user(request)
        print(user.username)

        # get the token
        try:
            config = Config.objects.get(fk_user=user)
            self.token = main.encrypt_or_decrypt(config.token, False)
        except Config.DoesNotExist as config_error:
            # Tratar exceção Config.DoesNotExist
            self.token = ""
            # Alguma lógica adicional se necessário
        except InvalidToken as invalid_token_error:
            # Tratar exceção InvalidToken
            self.token = ""
            # Alguma lógica adicional se necessário

        self.jira_url = config.jira_url
        self.email = user.email
        self.jira = None

    def connect(self):
        try:  
            # Criar objeto JIRA
            self.jira = Jira(
                url= self.jira_url,
                username=self.email,
                password=self.token,
                verify_ssl=False
            )
            print("Conexão com o Jira estabelecida com sucesso!")

        except Exception as e:
            print(f"Falha na conexão com o Jira: {str(e)}")
        
        return self.jira

    def close(self):
        if self.jira is not None:
            self.jira.close()
            print("Conexão com o Jira encerrada.")

    def create_issue(self, project_key, summary, description):
        pass


    def search_with_pagination(self, jql_query, start_at=0, max_results=100):
        results = []

        while True:
            # Realiza a chamada à API Jira
            response = self.jira.jql(jql=jql_query, start=start_at, limit=max_results)

            # Verifique se há resultados
            if 'issues' in response:
                issues = response['issues']
                results.extend(issues)

                # Atualize start_at para a próxima página
                start_at += max_results

                # Verifique se há mais resultados
                if start_at >= response['total']:
                    break
            else:
                # Se não houver mais resultados ou ocorrer um erro, saia do loop
                break

        return results
        
