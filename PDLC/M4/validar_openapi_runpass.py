"""Reproducible OpenAPI validation. Requires openapi-spec-validator 0.7.2."""
import hashlib
import json
import re
from importlib.metadata import version
from pathlib import Path
from openapi_spec_validator import OpenAPIV30SpecValidator
from openapi_schema_validator import OAS30Validator
from jsonschema import RefResolver

path=Path('API-RunPass-v1.openapi.json'); raw=path.read_bytes(); d=json.loads(raw)
errors=list(OpenAPIV30SpecValidator(d).iter_errors())
assert not errors, '\n'.join(str(e) for e in errors)
refs=[]; operations=[]
def walk(value):
 if isinstance(value,dict):
  if '$ref' in value:refs.append(value['$ref'])
  for child in value.values():walk(child)
 elif isinstance(value,list):
  for child in value:walk(child)
walk(d)
for pointer in refs:
 node=d
 for key in pointer.removeprefix('#/').split('/'):node=node[key]
for route,methods in d['paths'].items():
 for method,op in methods.items():
  if method not in ['get','post','put','patch','delete']:continue
  operations.append(op['operationId'])
  assert set(re.findall(r'{([^}]+)}',route))=={p['name'] for p in op.get('parameters',[]) if p.get('in')=='path'}
  if '204' in op['responses']:assert 'content' not in op['responses']['204']
  if route.startswith('/admin/'):assert op.get('x-required-role') and op.get('x-requires-mfa')
assert len(operations)==len(set(operations))
resolver=RefResolver.from_schema(d)
notes={k:4 for k in d['components']['schemas']['ReviewRatings']['required']}
cases=[
 ('CreateParticipation',{'editionId':'e1','distanceId':'d1'},True),
 ('CreateParticipation',{'editionRequestId':'r1','distanceKm':10},True),
 ('CreateParticipation',{'editionId':'e1'},False),
 ('PatchParticipation',{'expectedVersion':1,'timeSeconds':None},True),
 ('PatchParticipation',{'expectedVersion':1,'ratings':notes},False),
 ('ReplaceReview',{'expectedVersion':1,'ratings':notes},True),
 ('ReplaceReview',{'expectedVersion':1,'ratings':dict(list(notes.items())[:-1])},False),
 ('PublicProfile',{'id':'u1','displayName':'Runner','username':'runner','version':1,'email':'private@example.com'},False),
 ('BetaAdmissionInput',{'birthDate':'1990-01-01','declaresAdult':True},True),
 ('BetaAdmissionInput',{'birthDate':'1990-01-01','declaresAdult':False},False),
 ('ReviewAuditRecord',{'eventId':'evt','schemaVersion':1,'eventType':'ReviewCreated','occurredAt':'2026-10-27T12:00:00Z','expiresAt':'2026-12-26T12:00:00Z','reviewId':'r1','aggregateVersion':1,'correlationId':'c1','before':None,'after':{'ratings':notes,'comment':None}},True),
 ('AccountDeletionReceipt',{'operationId':'o1','state':'accepted','accessBlocked':False,'publiclyHidden':True},False),
]
for name,example,expected in cases:
 found=list(OAS30Validator(d['components']['schemas'][name],resolver=resolver).iter_errors(example))
 assert (not found)==expected,(name,[e.message for e in found])
report={'contract':path.name,'version':d['info']['version'],'sha256':hashlib.sha256(raw).hexdigest(),'validator':'openapi-spec-validator','validatorVersion':version('openapi-spec-validator'),'openapiErrors':len(errors),'paths':len(d['paths']),'operations':len(operations),'internalReferences':len(refs),'schemaExamplesPassed':len(cases),'limits':['No API execution, IAM/MFA enforcement or concurrency tested.','No assertion of full PRD coverage or technical approval.','Age/date business validation must be implemented in server code.']}
Path('VALIDACAO-OPENAPI-RunPass.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=True))
