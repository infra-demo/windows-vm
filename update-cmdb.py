#!/usr/bin/python3.6
from time import sleep
import requests
import json
from collections import namedtuple
from datetime import datetime

def getToken(username,passoword,url):
    headers = {
    'content-type': 'application/x-www-form-urlencoded'
    }
    params = {
    'username': username,
    'password': passoword
    }
    resp = requests.post(url, data=params, headers=headers)
    return resp.content

def getCMDBJson():
    data = json.load(open('vm-output.json'))
    # data = json.dumps(data)
    # try:
    #     x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys(),rename=False)(*d.values()))
    #     print(x.Business_Owner.value)
    # except ValueError as err:
    #     print(err)
    res = {"values":{ "Name": "",

        "Asset ID+": "",

        "Short Description": "",

        "Company": "AGL",

        "Primary Capability": "Server",

        "AssetLifecycleStatus": "Deployed",

        "Environment Specification": "Staging",

        "DNS Host Name": "",

        "Data Set Id" : "BMC.ASSET",

		"Building" : "Australia South East",

        "Serial Number" : ""}}

    res['values']['Name']=data['VM_Name']['value']
    res['values']['Asset ID+']=data['VM_Name']['value']
    res['values']['Short Description']=data['VM_Name']['value']
    res['values']['DNS Host Name']=data['VM_Name']['value']

    res = json.dumps(res)
    return res



def updateCMDB(data,token,url):
    headers = {
        'Content-Type':'application/json',
        'Authorization':'AR-JWT '+token
    }
    resp = requests.post(url,data=data,headers=headers)
    return resp

def getDateTime():
    timeOffset = datetime.now()
    now = timeOffset.strftime("%H:%M:%S")
    nowDay = timeOffset.strftime("%Y-%m-%d")
    res = nowDay+'T'+now
    return res

def getInfraChangeID():
    id=''
    file = open("cr.txt", "r")
    for line in file:
        id=line
    file.close()
    # print(cr)
    return id


def getCrNo(InfraChangeID,token,url):
    headers = {
        'Content-Type':'application/json',
        'Authorization':'AR-JWT '+token
    }
    url=url+"?q='Infrastructure Change ID' = \""+InfraChangeID+"\"&fields=values(Request ID)"
    #url=url+"?q=%27Infrastructure%20Change%20ID%27%20%3D%20%22"+InfraChangeID+"%22"
    #print(url)
    resp=requests.get(url,headers=headers)
    resp=resp.content.decode('utf-8')
    resp=json.loads(resp)
    # print(resp['entries'][0]['values']['Request ID'])
    return resp['entries'][0]['values']['Request ID']



def getCrJson():
    res = {
        "values" : {
		"z1D_Action" : "MODIFY",
        "Outage?": "No",
        "Change Request Status": "Closed",
        "Status Reason": "Successful",
        "Scheduled Start Date": "2018-04-01T10:00:00",
        "Scheduled End Date" : "2018-04-02T15:00:00",
        "Actual Start Date" : "2018-04-01T10:00:00",
        "Actual End Date" : "2018-04-02T15:00:00"
        }
        }
    res['values']['Scheduled Start Date']=getDateTime()
    res['values']['Actual Start Date']=getDateTime()
    sleep(10)
    res['values']['Scheduled End Date']=getDateTime()
    res['values']['Actual End Date']=getDateTime()
    res=json.dumps(res)
    return res

def closeCR(crNo,url,token,data):
    headers = {
        'Content-Type':'application/json',
        'Authorization':'AR-JWT '+token
    }
    url=url+crNo
    print(url)
    resp = requests.put(url,data=data,headers=headers)
    return resp

def getReconID(token,url):
    data = json.load(open('vm-output.json'))
    headers={
        'Content-Type':'application/json',
        'Authorization':'AR-JWT '+token
    }
    url=url+"?q='Name' = \""+data['VM_Name']['value']+"\"&fields=values(Reconciliation Identity)"
    print('recon-url',url)
    resp=requests.get(url,headers=headers)
    resp=resp.text
    resp=json.loads(resp)
    return resp['entries'][0]['values']['Reconciliation Identity']


def getCMDB_BOJson(recon_Id):

    data = json.load(open('vm-output.json'))
    res = { "values" : {

        "Asset ID+": "",

        "AssetInstanceId": "",

        "AssetClassId": "BMC_COMPUTERSYSTEM",

        "PeopleGroupInstanceID": "AGGAA5V0GMSWGAO3X03BAP050JF0FG",

        "Full Name" : "Matthew Wilton",

        "PeopleGroup Form Entry ID" : "PPL000000021715",

        "Login Name" : "a136842",

        "Form Type" : "People",

        "PersonRole" : "Used by",

        "Contact Company" : "AGL",
            }
}

    res['values']['Asset ID+']=data['VM_Name']['value']
    res['values']['AssetInstanceId']=recon_Id

    res = json.dumps(res)
    return res



###############main####################

url = "http://glawi1283.agl.int:8008/api/jwt/login"
password = "remedyapi"
username = "remedyapi"

cmdbUrl = "http://glawi1283.agl.int:8008/api/arsys/v1/entry/AST:ComputerSystem"

crURL= "http://glawi1283.agl.int:8008/api/arsys/v1/entry/CHG:ChangeInterface/"

boUrl="http://glawi1283.agl.int:8008/api/arsys/v1/entry/AST:AssetPeople"

token = getToken(username,password,url).decode('utf-8')
print('Token Generated...\n')


data=getCMDBJson()

CMDBresp=updateCMDB(data,token,cmdbUrl)
status=CMDBresp.status_code


try:


    if status==204:
        reconID=getReconID(token,cmdbUrl)
        data=getCMDB_BOJson(reconID)
        CMDBresp=updateCMDB(data,token,boUrl)
        if CMDBresp.status_code==200 or CMDBresp.status_code==204:
            print("CMDB Updated Successfully....\n")
            print('Attempting to get Infrastructure Change ID...')
            id=getInfraChangeID()
            id=id.replace('\n','')
            print('Infrastructure Change ID='+id+'\n')
            print('Attempting to get CR Number...')
            cr=getCrNo(id,token,crURL)
            print('CR Number='+cr+'\n')
            crData=getCrJson()
            print(crData)
            print('Attempting to close '+cr+'...\n')
            resp=closeCR(cr,crURL,token,crData)
            # print(resp.status_code,resp.content,resp.reason,resp.json())
            if resp.status_code==204:
                print(cr+' closed successfully.')
            else:
                print('CR could not be closed...')
                print('Error:'+str(resp.status_code)+' - '+resp.json()[0]['messageAppendedText'])
        else:
             print('CMDB BO Update Error:',status,'-',CMDBresp.json()[0]['messageAppendedText'])

    else:
        print('CMDB Update Error:',status,'-',CMDBresp.json()[0]['messageAppendedText'])

except Exception as e:
    print(e)


