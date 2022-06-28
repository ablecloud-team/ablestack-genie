#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib2
import urllib
import hashlib
import hmac
import base64
import argparse

def createArgumentParser():
    '''
    입력된 argument를 파싱하여 dictionary 처럼 사용하게 만들어 주는 parser를 생성하는 함수
    :return: argparse.ArgumentParser
    '''
    # 참조: https://docs.python.org/ko/3/library/argparse.html
    # 프로그램 설명
    parser = argparse.ArgumentParser(description='AWX에서 Automation API를 사용하기 위한 프로그램',
                                        epilog='copyrightⓒ 2022 All rights reserved by ABLECLOUD™',
                                        usage='%(prog)s arguments')

    # 인자 추가: https://docs.python.org/ko/3/library/argparse.html#the-add-argument-method

    #--API Commond
    parser.add_argument('-c', '--commond', metavar='API Commond', choices=['listAutomationDeployedResource', 'addDeployedResourceGroup', 'addDeployedUnitResource', 'deleteDeployedResourceGroup', 'deleteDeployedUnitResource', 'updateDeployedResourceGroup'], type=str, help='input Value to API Commond', required=True)
    
    #--Mold Service API Protocol
    parser.add_argument('-ap', '--api-protocol', metavar='Mold Service API Protocol', choices=['http', 'https'], type=str, help='input Value to Mold Service API Protocol', required=True)
    
    #--Mold Service Network IP address
    parser.add_argument('-ip', '--ip-address', metavar='Mold Service Network IP address', type=str, help='input Value Mold Service Network IP address', required=True)

    #--Mold Service API Port
    parser.add_argument('-p', '--port', metavar='Mold Service API Port', type=str, help='input Value Mold Service API Port', required=True)

    #--Mold Automation Controller User apikey
    parser.add_argument('-ak', '--apikey', metavar='Mold Automation Controller User apikey', type=str, help='input Value Mold Automation Controller User apikey', required=True)
    
    #--Mold Automation Controller User secretkey
    parser.add_argument('-sk', '--secretkey', metavar='Mold Automation Controller User secretkey', type=str, help='input Value Mold Automation Controller User secretkey', required=True)

    #--the name of deployed service
    parser.add_argument('-n', '--name', metavar='the name of deployed service', type=str, help='input Value the name of deployed service')

    #--the description of the running service
    parser.add_argument('-d', '--description', metavar='the description of the running service', type=str, help='input Value the description of the running service')

    #--the ID of the deployed service
    parser.add_argument('-gid', '--deployed-group-id', metavar='the ID of the deployed service', type=str, help='input Value the ID of the deployed service')

    #--the ID of the deployed service zone
    parser.add_argument('-zid', '--zone-id', metavar='the ID of the deployed service zone', type=str, help='input Value the ID of the deployed service zone')

    #--the ID of the instance the service is running on
    parser.add_argument('-vid', '--deployed-vm-id', metavar='the ID of the instance the service is running on', type=str, help='input Value the ID of the instance the service is running on')
    
    #--the ID of the Automation Controller id
    parser.add_argument('-acid', '--automation-controller-id', metavar='the ID of the Automation Controller id', type=str, help='input Value the ID of the Automation Controller')
    
    #--the name of deployed unit service
    parser.add_argument('-un', '--service-unit-name', metavar='the name of deployed unit service', type=str, help='input Value the name of deployed unit service')

    #--state of deployed unit service
    parser.add_argument('-s', '--state', metavar='state of deployed unit service', type=str, help='input Value state of deployed unit service')

    return parser

def stateResultChecker(state):
    if state.lower() == 'active' or state.lower() == 'inactive':
        return state.lower().title()
    else:
        return 'Inactive'

def excuteApi(request, args):
    secretkey=args.secretkey

    baseurl=args.api_protocol+'://'+args.ip_address+':'+args.port+'/client/api?'
    request_str='&'.join(['='.join([k,urllib.quote_plus(request[k])]) for k in request.keys()])

    sig_str='&'.join(['='.join([k.lower(),urllib.quote_plus(request[k]).lower().replace('+','%20')])for k in sorted(request.iterkeys())])
    sig=hmac.new(secretkey,sig_str,hashlib.sha1)
    sig=hmac.new(secretkey,sig_str,hashlib.sha1).digest()
    sig=base64.encodestring(hmac.new(secretkey,sig_str,hashlib.sha1).digest())
    sig=base64.encodestring(hmac.new(secretkey,sig_str,hashlib.sha1).digest()).strip()
    sig=urllib.quote_plus(base64.encodestring(hmac.new(secretkey,sig_str,hashlib.sha1).digest()).strip())

    req=baseurl+request_str+'&signature='+sig
    res=urllib2.urlopen(req)
    return res.read()

def listAutomationDeployedResource(args):
    # reqest 세팅
    request={}
    request['command']=args.commond
    request['name']=args.name
    request['response']='json'
    request['apikey']=args.apikey
    
    # API 호출
    result = excuteApi(request, args)
    print(result)

def addDeployedResourceGroup(args):
    # reqest 세팅
    request={}
    request['command']=args.commond
    request['name']=args.name
    request['description']=args.description
    request['zoneid']=args.zone_id
    request['controllerid']=args.automation_controller_id
    request['response']='json'
    request['apikey']=args.apikey
    
    # API 호출
    result = excuteApi(request, args)
    print(result)

def addDeployedUnitResource(args):
    # reqest 세팅
    request={}
    request['command']=args.commond
    request['deployedgroupid']=args.deployed_group_id
    request['virtualmachineid']=args.deployed_vm_id
    request['serviceunitname']=args.service_unit_name
    request['state']=stateResultChecker(args.state)
    request['response']='json'
    request['apikey']=args.apikey

    # API 호출
    result = excuteApi(request, args)
    print(result)

def deleteDeployedResourceGroup(args):
    # reqest 세팅
    request={}
    request['command']=args.commond
    request['name']=args.name
    request['zoneid']=args.zone_id
    request['response']='json'
    request['apikey']=args.apikey

    # API 호출
    result = excuteApi(request, args)
    print(result)

def deleteDeployedUnitResource(args):
    # reqest 세팅
    request={}
    request['command']=args.commond
    request['deployedgroupid']=args.deployed_group_id
    request['response']='json'
    request['apikey']=args.apikey

    # API 호출
    result = excuteApi(request, args)
    print(result)

def updateDeployedResourceGroup(args):
    # reqest 세팅
    request={}
    request['command']=args.commond
    request['id']=args.deployed_group_id
    request['state']=stateResultChecker(args.state)
    request['response']='json'
    request['apikey']=args.apikey
    
    # API 호출
    result = excuteApi(request, args)
    print(result)

if __name__ == '__main__':
    
    # parser 생성
    parser = createArgumentParser()
    # input 파싱
    args = parser.parse_args()

    if args.commond == 'listAutomationDeployedResource':
        #필수값 체크
        if args.name is None:
            print ('name is null')
        else:
            listAutomationDeployedResource(args)
        
    elif args.commond == 'addDeployedResourceGroup':
        #필수값 체크
        if args.name is None:
            print ('name is null')
        elif args.description is None:
            print ('description is null')
        elif args.zone_id is None:
            print ('zone_id is null')
        elif args.automation_controller_id is None:
            print ('automation_controller_id is null')
        else:
            addDeployedResourceGroup(args)

    elif args.commond == 'addDeployedUnitResource':
        #필수값 체크
        if args.deployed_group_id is None:
            print ('deployed group id is null')
        elif args.deployed_vm_id is None:
            print ('deployed vm id is null')
        elif args.service_unit_name is None:
            print ('service unit name is null')
        elif args.state is None:
            print ('state is null')
        else:
            addDeployedUnitResource(args)

    elif args.commond == 'deleteDeployedResourceGroup':
        #필수값 체크
        if args.name is None:
            print ('name is null')
        elif args.zone_id is None:
            print ('zone_id is null')
        else:
            deleteDeployedResourceGroup(args)

    elif args.commond == 'deleteDeployedUnitResource':
        #필수값 체크
        if args.deployed_group_id is None:
            print ('deployed group id is null')
        else:
            deleteDeployedUnitResource(args)

    elif args.commond == 'updateDeployedResourceGroup':
        #필수값 체크
        if args.deployed_group_id is None:
            print ('deployed group id is null')
        elif args.state is None:
            print ('state is null')
        else:
            updateDeployedResourceGroup(args)

    else:
        print ('No matching command found.')

'''
사용 예제

서비스 네임을 이용하여 리스트 정보 조회 기능
python mold_genie_api.py \
	-c listAutomationDeployedResource \
	-ap http -ip 10.10.1.10 -p 8080 \
	-ak api_key_value \
	-sk secret_key_value \
	-n ServiceName

서비스 그룹 등록
python mold_genie_api.py \
	-c addDeployedResourceGroup \
	-ap http -ip 10.10.1.10 -p 8080 \
	-ak api_key_value \
	-sk secret_key_value \
	-zid zone_uuid \
    -acid automation_contriller_uuid \
	-n ServiceName \
	-d 'Service description'

서비스 단위별 상태 등록
python mold_genie_api.py \
	-c addDeployedUnitResource \
	-ap http -ip 10.10.1.10 -p 8080 \
	-ak api_key_value \
	-sk secret_key_value \
	-gid group_id_or_uuid \
	-vid vm_uuid \
	-un mysqld \
	-s Running

서비스 그룹 상태정보 삭제 기능
python mold_genie_api.py \
	-c deleteDeployedResourceGroup \
	-ap http -ip 10.10.1.10 -p 8080 \
	-ak api_key_value \
	-sk secret_key_value \
	-zid zone_uuid \
	-n ServiceName

서비스 단위별 상태정보 삭제 기능
python mold_genie_api.py \
	-c deleteDeployedUnitResource \
	-ap http -ip 10.10.1.10 -p 8080 \
	-ak api_key_value \
	-sk secret_key_value \
	-gid group_uuid

서비스 그룹 상태정보 업데이트 기능
python mold_genie_api.py \
	-c updateDeployedResourceGroup \
	-ap http -ip 10.10.1.10 -p 8080 \
	-ak api_key_value \
	-sk secret_key_value \
	-gid group_uuid \
	-s Active

'''