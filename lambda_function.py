import json
import boto3

dynamodb = boto3.resource('dynamodb')
tabela = dynamodb.Table('NotasFiscais')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
       
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=key)
        conteudo = response['Body'].read().decode('utf-8')
        dados = json.loads(conteudo)
       
        tabela.put_item(Item={
            'id': dados['id'],
            'nome_cliente': dados['nome_cliente'],
            'data': dados['data'],
            'valor': str(dados['valor'])
        })
       
    return {'statusCode': 200, 'body': 'Nota fiscal processada'}