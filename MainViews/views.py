import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import requests
from MainViews.forms import ContractForm, StateForm, RequestForm
from django.contrib import messages
from MainViews.token import get_token
from MainViews.config import auth_token, storage_conn
import json
from MainViews.models import User
import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta
from azure.storage.blob import ResourceTypes, AccountSasPermissions, generate_account_sas

# Global variables
contract_details = []
email = []
contract_data = {}
contract_id = []
blob_name = []
file_path = []
recent_info = {}
times = []


def recent_activity(request):
    contract_data.clear()
    recent_info.clear()
    token = get_token()
    times.clear()

    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts?workflowId=1&skip=0&top=100"
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = requests.request("GET", url, headers=headers)

    results = response.json()['contracts']

    if sample_view2(request) == 'Individual User':

        # GETTING INDIVIDUAL USER CONTRACTS
        for x in range(len(results)):

            if results[x]['contractActions'][0]['parameters'][1]['value'] == sample_view(request):
                for y in results[x]['contractActions']:
                    times.append(y['timestamp'])

        times.sort()
        times.reverse()

        for u in times:
            for x in range(len(results)):
                for y in results[x]['contractActions']:
                    if u == y['timestamp']:
                        if y['workflowFunctionId'] == 1:
                            recent_info[u] = dict([('Action', 'Create Contract'), (
                                'lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                                   ('id', results[x]['id'])])

                        elif y['workflowFunctionId'] == 2:
                            recent_info[u] = dict([('Action', 'Share Contract'), (
                                'lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                                   ('id', results[x]['id'])])

                        elif y['workflowFunctionId'] == 3:
                            recent_info[u] = dict([('Action', 'Accept Contract'), (
                                'lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                                   ('id', results[x]['id'])])

                        elif y['workflowFunctionId'] == 4:
                            recent_info[u] = dict([('Action', 'Reject Contract'), (
                                'lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                                   ('id', results[x]['id'])])

                        elif y['workflowFunctionId'] == 7:
                            recent_info[u] = dict([('Action', 'Revoke Contract'), (
                                'lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                                   ('id', results[x]['id'])])

                        elif y['workflowFunctionId'] == 8:
                            recent_info[u] = dict([('Action', 'Terminate Contract'), (
                                'lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                                   ('id', results[x]['id'])])

    if sample_view2(request) == 'Organisation':

        # GETTING ORGANISATIONAL USER CONTRACTS
        for x in range(len(results)):
            for y in results[x]['contractActions']:
                for z in y['parameters']:
                    if z['value'] == sample_view(request):
                        times.append(y['timestamp'])

        times.sort()
        times.reverse()

        for u in times:
            for x in range(len(results)):
                for y in results[x]['contractActions']:
                    if u == y['timestamp']:
                        if y['workflowFunctionId'] == 2:
                            recent_info[u] = dict([('Action', 'Share Contract'), (
                                'lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                                   ('id', results[x]['id'])])

    stuff = {
        "recent_info": recent_info
    }
    return render(request, 'identity/recent_activity.html', context=stuff)


# Organisation requesting data
def req_credential():
    token = auth_token
    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts/" + str(contract_id[0]) + "/actions"

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "mscblockchain-h4atns-api.azurewebsites.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    data_credential = {
        "workflowFunctionID": 5,
        "workflowActionParameters": [
            {
                "name": "intendedPurpose",
                "value": str(contract_details[1]),
                "workflowFunctionParameterId": 4
            },
            {
                "name": "appThirdParty",
                "value": str(contract_details[0]),
                "workflowFunctionParameterId": 5
            }
        ]
    }

    payload = json.dumps(data_credential)

    attempt = requests.request("POST", url, data=payload, headers=headers)

    return attempt.text


# Individual sharing a locker
def share_contract():
    token = auth_token
    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts/" + str(contract_id[0]) + "/actions"
    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "mscblockchain-h4atns-api.azurewebsites.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    share_credential = {
        "workflowFunctionID": 2,
        "workflowActionParameters": [
            {
                "name": "thirdPartyRequestor",
                "value": "0xe7afddc56320e2a929333e96afeab366fb65876c",
                "workflowFunctionParameterId": 1
            },
            {
                "name": "intendedPurpose",
                "value": str(contract_details[1]),
                "workflowFunctionParameterId": 2
            },
            {
                "name": "appThirdParty",
                "value": str(contract_details[0]),
                "workflowFunctionParameterId": 3
            }
        ]
    }

    payload = json.dumps(share_credential)
    attempt = requests.request("POST", url, data=payload, headers=headers)

    return attempt.text


# Organisation requesting a locker
def org_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            contract_details.clear()

            third_party = str(sample_view(request))
            intended_purpose = form.cleaned_data.get('intended_purpose')
            contract_details.append(third_party)
            contract_details.append(intended_purpose)

            messages.success(request, f'Locker successfully requested - please await a response.')

            contract_id.clear()
            contract_id.append(request.GET.get('name'))

            # Workbench Function
            req_credential()

            return redirect('contracts')
    else:
        form = StateForm()
    return render(request, 'identity/org_request.html', {'form': RequestForm})


# Retrieve contracts as an Organisation
def org_contracts(request):
    contract_data.clear()
    token = get_token()
    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts?workflowId=1&skip=0&top=5000"
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = requests.request("GET", url, headers=headers)

    query = request.GET.get('q')

    results = response.json()['contracts']

    for x in range(len(results)):
        try:
            if results[x]['contractProperties'][9]['value'] == sample_view(request):

                if query:
                    if query in results[x]['contractActions'][0]['parameters'][0]['value']:
                        if results[x]['contractProperties'][0]['value'] == '1':
                            contract_data[x] = dict(
                                [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                 ('state', 'Sharing Request Pending'), ('id', results[x]['id']),
                                 ('username', results[x]['contractActions'][0]['parameters'][1]['value']),
                                 ('purpose', results[x]['contractProperties'][7]['value'])])

                        if results[x]['contractProperties'][0]['value'] == '2':
                            contract_data[x] = dict(
                                [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                 ('state', 'Available to Access'), ('id', results[x]['id']),
                                 ('username', results[x]['contractActions'][0]['parameters'][1]['value']),
                                 ('purpose', results[x]['contractProperties'][7]['value']),
                                 ])

                else:
                    if results[x]['contractProperties'][0]['value'] == '1':
                        contract_data[x] = dict(
                            [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                             ('state', 'Sharing Request Pending'), ('id', results[x]['id']),
                             ('username', results[x]['contractActions'][0]['parameters'][1]['value']),
                             ('purpose', results[x]['contractProperties'][7]['value'])])

                    if results[x]['contractProperties'][0]['value'] == '2':
                        contract_data[x] = dict(
                            [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                             ('state', 'Available to Access'), ('id', results[x]['id']),
                             ('username', results[x]['contractActions'][0]['parameters'][1]['value']),
                             ('purpose', results[x]['contractProperties'][7]['value']),
                             ])

        except:
            continue

    stuff = {
        "contract_data": contract_data
    }
    return render(request, 'identity/org_contracts.html', context=stuff)


# Django view to operate sharing of a locker
def state_change(request):
    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():

            contract_details.clear()

            third_party = form.cleaned_data.get('third_party_email')
            intended_purpose = form.cleaned_data.get('intended_purpose')
            contract_details.append(third_party)
            contract_details.append(intended_purpose)

            if User.objects.filter(email=contract_details[0]).exists() and \
                    User.objects.get(email=contract_details[0]).profile.user_type == 'Organisation':

                contract_id.clear()
                contract_id.append(request.GET.get('name'))

                # Workbench Function
                share_contract()
                messages.success(request, f'Contract successfully shared')

            else:
                messages.warning(request, f'Email does not exist, please enter a valid third party email.')

    else:
        form = StateForm()

    return render(request, 'identity/state_change.html', {'form': StateForm})


# Returns email of user currently logged in
def sample_view(request):
    current_user = request.user
    return current_user.email


# Returns user type of user currently logged in
def sample_view2(request):
    try:
        current_user = request.user
        return current_user.profile.user_type
    except:
        pass


def home(request):
    # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') --> Use in production

    # Temporary connection string format
    connect_str = storage_conn
    return render(request, 'identity/home.html')


# Workbench function to terminate contract instance
def terminate(request):
    contract_id.clear()
    contract_id.append(request.GET.get('name'))
    token = auth_token

    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts/" + str(contract_id[0]) + "/actions"

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "mscblockchain-h4atns-api.azurewebsites.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    terminate_con = {
        "workflowFunctionID": 8,
        "workflowActionParameters": []
    }

    payload = json.dumps(terminate_con)

    attempt = requests.request("POST", url, data=payload, headers=headers)
    delete_blob()
    messages.warning(request, f'Contract successfully terminated')

    return contracts(request)


# Workbench function to accept locker request
def accept_req(request):
    token = auth_token
    contract_id.clear()
    contract_id.append(request.GET.get('name'))

    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts/" + str(contract_id[0]) + "/actions"

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "mscblockchain-h4atns-api.azurewebsites.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    accepted = {
        "workflowFunctionID": 3,
        "workflowActionParameters": []
    }

    payload = json.dumps(accepted)

    attempt = requests.request("POST", url, data=payload, headers=headers)
    messages.success(request, f'Sharing request accepted')

    return contracts(request)


# Workbench function to reject locker request
def reject_req(request):
    token = auth_token
    contract_id.clear()
    contract_id.append(request.GET.get('name'))

    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts/" + str(contract_id[0]) + "/actions"

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "mscblockchain-h4atns-api.azurewebsites.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    rejected = {
        "workflowFunctionID": 4,
        "workflowActionParameters": []
    }

    payload = json.dumps(rejected)

    attempt = requests.request("POST", url, data=payload, headers=headers)
    messages.warning(request, f'Sharing request rejected')

    return contracts(request)


# Workbench function to release locker
def release(request):
    token = auth_token
    contract_id.clear()
    contract_id.append(request.GET.get('name'))

    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts/" + str(contract_id[0]) + "/actions"

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "mscblockchain-h4atns-api.azurewebsites.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    release_access = {
        "workflowFunctionID": 6,
        "workflowActionParameters": []
    }

    payload = json.dumps(release_access)

    attempt = requests.request("POST", url, data=payload, headers=headers)
    messages.success(request, f'Locker released')

    return contracts(request)


# Workbench function to revoke locker access
def revoke(request):
    token = auth_token
    contract_id.clear()
    contract_id.append(request.GET.get('name'))
    messages.warning(request, f'Locker successfully revoked')

    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts/" + str(contract_id[0]) + "/actions"

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "mscblockchain-h4atns-api.azurewebsites.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    revoke_access = {
        "workflowFunctionID": 7,
        "workflowActionParameters": []
    }

    payload = json.dumps(revoke_access)

    attempt = requests.request("POST", url, data=payload, headers=headers)

    return contracts(request)


# Main contracts view function - retrieves list from Workbench
def contracts(request):
    contract_data.clear()
    token = get_token()

    url = "https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts?workflowId=1&skip=0&top=10000"

    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = requests.request("GET", url, headers=headers)

    results = response.json()['contracts']

    query = request.GET.get('q')

    if sample_view2(request) == 'Organisation':

        # GETTING ORGANISATIONAL USER CONTRACTS
        for x in range(len(results)):
            try:
                # Checking for app email address in each contract - returns if matches signed-in user
                if results[x]['contractProperties'][0]['value'] == '0':
                    if query:
                        if query in results[x]['contractActions'][0]['parameters'][1]['value']:
                            contract_data[x] = dict(
                                [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                 ('state', 'Available To Share'), ('id', results[x]['id']),
                                 ('username', results[x]['contractActions'][0]['parameters'][1]['value'])])
                    else:

                        contract_data[x] = dict(
                            [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                             ('state', 'Available To Share'), ('id', results[x]['id']),
                             ('username', results[x]['contractActions'][0]['parameters'][1]['value'])])

            except:
                continue

    elif sample_view2(request) == 'Individual User':

        # GETTING INDIVIDUAL USER CONTRACTS
        for x in range(len(results)):
            try:
                # Checking for app email address in each contract - returns if matches signed-in user
                if results[x]['contractActions'][0]['parameters'][1]['value'] == sample_view(request):
                    if results[x]['contractProperties'][0]['value'] == '0':
                        if query:
                            if query in results[x]['contractActions'][0]['parameters'][0]['value']:
                                contract_data[x] = dict(
                                    [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                     ('state', 'Available To Share'), ('id', results[x]['id'])])
                        else:
                            contract_data[x] = dict(
                                [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                 ('state', 'Available To Share'), ('id', results[x]['id'])])

                    elif results[x]['contractProperties'][0]['value'] == '2':
                        if query:
                            if query in results[x]['contractActions'][0]['parameters'][0]['value']:
                                contract_data[x] = dict(
                                    [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                     ('state', 'Sharing With Third Party'), ('id', results[x]['id']),
                                     ('requestor', results[x]['contractProperties'][9]['value'])])
                        else:
                            contract_data[x] = dict(
                                [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                 ('state', 'Sharing With Third Party'), ('id', results[x]['id']),
                                 ('requestor', results[x]['contractProperties'][9]['value'])])

                    elif results[x]['contractProperties'][0]['value'] == '1':
                        if query:
                            if query in results[x]['contractActions'][0]['parameters'][0]['value']:
                                contract_data[x] = dict(
                                    [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                     ('state', 'Sharing Request Pending'), ('id', results[x]['id']),
                                     ('purpose', results[x]['contractProperties'][7]['value']),
                                     ('requestor', results[x]['contractProperties'][9]['value'])])
                        else:
                            contract_data[x] = dict(
                                [('lockername', results[x]['contractActions'][0]['parameters'][0]['value']),
                                 ('state', 'Sharing Request Pending'), ('id', results[x]['id']),
                                 ('purpose', results[x]['contractProperties'][7]['value']),
                                 ('requestor', results[x]['contractProperties'][9]['value'])])

            except:
                continue

    stuff = {
        "contract_data": contract_data
    }
    return render(request, 'identity/contracts.html', context=stuff)


# Initiates new contract instance from Django web app
def new_contract(request):
    email.clear()
    email.append(sample_view(request))

    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)

        if form.is_valid():
            locker_name = form.cleaned_data.get('locker_name')
            contract_details.clear()
            contract_details.append(locker_name)

            # Workbench Function
            create_wb_contract()

            # Azure blob function section to upload & code file
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(str(contract_id[0]) + ' ' + myfile.name, myfile)  # saves the file to `media` folder
            upload_it(filename)

            # Removes from local storage
            remove_file()

            contract_details.clear()

            messages.success(request, f'Contract successfully created')

            return redirect('home')
    else:
        form = ContractForm()
    return render(request, 'identity/new_contract.html', {'form': form})


# Upload file to Blob storage
def upload_it(file):
    # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') --> Use in production

    # Temporary connection string format
    connect_str = storage_conn

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)

    container_name = "credentials"

    # Create a file in local data directory to upload and download
    local_path = "./media"
    local_file_name = str(file)
    upload_file_path = os.path.join(local_path, local_file_name)

    file_path.clear()
    file_path.append(upload_file_path)

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)


# Request via Django web app to download data
def view_data(request):
    token = auth_token
    contract_id.clear()
    contract_id.append(request.GET.get('name'))

    return redirect(download_it())


def remove_file():
    os.remove(file_path[0])


# Returns specific file name
def blob_list():
    # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') --> Use in production

    # Temporary connection string format
    connect_str = storage_conn

    blob_name.clear()

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Instantiate a ContainerClient
    container_client = blob_service_client.get_container_client("credentials")

    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        if str(blob.name).split(' ', 1)[0] == str(contract_id[0]):
            blob_name.append(blob.name)

    return blob_name


# Used when contract is terminated to delete file from Blob storage
def delete_blob():
    blob_list()
    # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') --> Use in production

    # Temporary connection string format
    connect_str = storage_conn

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client("credentials")

    # Delete blob
    container_client.delete_blob(blob=blob_name[0])


def download_it():
    blob_list()
    # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') --> Use in production

    # Temporary connection string format
    connect_str = storage_conn

    container_name = 'credentials'
    account_name = 'decentraliseduploads'

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    sas_token = generate_account_sas(
        blob_service_client.account_name,
        account_key=blob_service_client.credential.account_key,
        resource_types=ResourceTypes(object=True),
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    file_conn = 'https://' + account_name + '.blob.core.windows.net/' + container_name + '/' + blob_name[0] \
                + '?' + sas_token

    return file_conn


# Workbench function to create new contract
def create_wb_contract():
    contract_id.clear()
    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + auth_token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "mscblockchain-h4atns-api.azurewebsites.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    raw_contract = {
        "workflowFunctionID": 1,
        "workflowActionParameters": [
            {
                "name": "lockerFriendlyName",
                "value": str(contract_details[0]),
                "workflowFunctionParameterId": 6
            },
            {
                "name": "appUsername",
                "value": str(email[0]),
                "workflowFunctionParameterId": 7
            },
            {
                "name": "bankAgent",
                "value": "0xe7afddc56320e2a929333e96afeab366fb65876c",
                "workflowFunctionParameterId": 8
            }
        ]
    }

    payload = json.dumps(raw_contract)

    attempt = requests.request("POST",
                               'https://mscblockchain-h4atns-api.azurewebsites.net/api/v1/contracts?workflowId=1'
                               '&contractCodeId=1&connectionId=1',
                               data=payload,
                               headers=headers)

    contract_id.append(attempt.text)

    return attempt.text
