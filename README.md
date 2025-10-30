# 🚀 Desafio DIO: Processamento de Notas Fiscais com AWS CLI

## 📌 Proposta do Desafio

Este projeto foi desenvolvido como parte do desafio da [Digital Innovation One (DIO)](https://www.dio.me/), que propunha a criação de um ambiente de processamento de notas fiscais utilizando:

- **LocalStack** para simular serviços da AWS localmente
- **AWS CLI** para criar e gerenciar os recursos
- **Lambda + S3 + DynamoDB** como arquitetura principal

O objetivo era demonstrar o uso da AWS CLI para provisionar recursos e automatizar o processamento de arquivos JSON contendo dados de notas fiscais.

---

## ⚠️ Dificuldades encontradas

Durante a execução do desafio, alguns obstáculos técnicos exigiram adaptações:

- Meu notebook principal roda **Windows 8**, que não é compatível com o Docker Desktop (requisito para rodar o LocalStack)
- Como alternativa, utilizei um notebook emprestado com **Windows 11**
- Mesmo assim, não conseguimos ativar a virtualização necessária para o Docker funcionar corretamente

### ✅ Solução adotada

Para garantir a entrega do desafio e manter a proposta original (uso do **AWS CLI**), decidi **executar o projeto diretamente na AWS real**, utilizando a CLI para criar todos os recursos — sem usar o console para provisionamento manual.

---

## 🛠️ Etapas do projeto

### 1. Criar bucket S3

```
aws s3api create-bucket --bucket desafio-caroline-nf --region us-east-1
```

### 2. Criar tabela DynamoDB
```
aws dynamodb create-table \
  --table-name NotasFiscais \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

### 3. Criar role de execução da Lambda
```
aws iam create-role \
  --role-name LambdaS3DynamoRole \
  --assume-role-policy-document file://trust-policy.json
```
trust-policy.json contém a política de confiança para Lambda.

### 4. Anexar permissões à role
```
aws iam attach-role-policy \
  --role-name LambdaS3DynamoRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

aws iam attach-role-policy \
  --role-name LambdaS3DynamoRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

aws iam attach-role-policy \
  --role-name LambdaS3DynamoRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

### 5. Criar função Lambda
```
aws lambda create-function \
  --function-name ProcessaNotaFiscal \
  --runtime python3.9 \
  --role arn:aws:iam::<SEU_ID_DE_CONTA>:role/LambdaS3DynamoRole \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda.zip
```
O arquivo lambda.zip contém o código Python da função.

### 6. Configurar gatilho do S3 para Lambda

Como o AWS CLI não permite configurar o gatilho diretamente, essa etapa foi feita via Console AWS:

- Acesse a função Lambda

- Vá em Configuration → Triggers

- Adicione um gatilho do tipo S3

- Selecione o bucket que irá ser utilizado

- Tipo de evento: PUT
  
- Prefixo e sufixo: deixados em branco para aceitar qualquer arquivo

### 7. Testar o fluxo completo
- Criar arquivo de nota fiscal
  ```
  {
  "id": "NF001",
  "nome_cliente": "João da Silva",
  "data": "2025-10-30",
  "valor": 199.90
  }
  
``` Salvo como nota1.json
```
- Enviar para o S3
  ```
  aws s3 cp nota1.json s3://desafio-caroline-nf/
  ```
### 8. Verificar execução da Lambda
```
  aws logs describe-log-streams --log-group-name /aws/lambda/ProcessaNotaFiscal
  aws logs get-log-events --log-group-name /aws/lambda/ProcessaNotaFiscal --log-stream-name <NOME_DO_LOG_STREAM>
```
Mesmo com erros nos logs, o item foi salvo corretamente no DynamoDB.

### ✅ Resultado final
Apesar dos desafios técnicos com o ambiente local, o projeto foi concluído com sucesso:

- Todos os recursos foram criados via AWS CLI

- O fluxo de envio de JSON → Lambda → DynamoDB está funcionando

- O item foi salvo corretamente na tabela

- O desafio da DIO foi cumprido com fidelidade à proposta original

  ### 📁 Estrutura de arquivos
  .
├── lambda_function.py
├── lambda.zip
├── nota1.json
├── trust-policy.json
└── README.md

### 🙌 Conclusão
Este projeto demonstra como é possível construir uma arquitetura serverless com AWS CLI, mesmo diante de limitações técnicas. A entrega foi adaptada para rodar diretamente na AWS, mantendo a essência do desafio proposto pela DIO.

  





