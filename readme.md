
# 事前準備
## profile作成

- awscliと awscli-localを入れておく
```
pip install awscli awscli-local
```

- `~/.aws/credentials`
```
[localstack]
aws_access_key_id = dummy
aws_secret_access_key = dummy
```

- `~/.aws/config`
```
[profile localstack]
region = us-east-1
output = json
```

## docker-compose

- 2021/12/14現在 version13で動かせない（13は先月リリース)
- version12の最終バージョンを使う

```
version: '2.1'

services:
  localstack:
    container_name: "${LOCALSTACK_DOCKER_NAME-localstack_main}"
    image: localstack/localstack:0.12.20
    network_mode: bridge
    ports:
      - 127.0.0.1:4566:4566/tcp
    environment:
      - SERVICES=${SERVICES- }
      - DEBUG=${DEBUG- }
      - DATA_DIR=${DATA_DIR- }
      - LAMBDA_EXECUTOR=${LAMBDA_EXECUTOR- }
      - KINESIS_ERROR_PROBABILITY=${KINESIS_ERROR_PROBABILITY- }
      - DOCKER_HOST=unix:///var/run/docker.sock
      - HOST_TMP_FOLDER=${TMPDIR}
    volumes:
      - "${TMPDIR:-/tmp/localstack}:/tmp/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"

```


# 実行
- 
```
export AWS_PROFILE=localstack
docker-compose up
```


# S3

## バケットを作成
```
awslocal s3api create-bucket --bucket test-bucket
```

## ls
```
awslocal s3 ls
```
## cp
```
awslocal s3 cp hello.txt s3://test-bucket/
```

## cat
```
awslocal s3 cp s3://test-bucket/hello.txt -
```

# lambda

## 登録
- lambda.py に 関数lambda_handlerがあるとして

```
zip lambda_package.zip lambda.py
awslocal lambda create-function --function-name test  --runtime python3.8 --handler lambda.lambda_handler --role r1  --zip-file fileb://lambda_package.zip
```

## 更新
```
awslocal lambda update-function-code --function-name test --zip-file fileb://lambda.zip 

```

## 削除
```
awslocal lambda delete-function --function-name test
```

## 実行
```
awslocal lambda invoke --function-name test  result.json
```
もしくは
```
awslocal lambda invoke --function-name test  --invocation-type RequestResponse --payload '{}' result.json; cat result.json | jq .
```


## ローカルでlambdaのみを動かすとき

````
docker run -v "$PWD":/var/task -t lambci/lambda:python3.8 l2.lambda_handler '{}'
```