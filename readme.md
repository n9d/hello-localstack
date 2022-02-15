
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

## .env

- `cp .env.example .env` PRO版を使うときには.envにkeyを書く


# 実行

```
export AWS_PROFILE=localstack
docker-compose up
```


# S3

## バケット作成
```
awslocal s3 mb s3://test-bucket
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

## sqsにイベントを貼り付ける
```
awslocal lambda create-event-source-mapping --function-name test --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-1:000000000000:test-queue
```


## ローカルでlambdaのみを動かすとき

```
docker run -v "$PWD":/var/task -t lambci/lambda:python3.8 l2.lambda_handler '{}'
```

# sqs

## 作成
```
awslocal sqs create-queue --queue-name test-queue 
```

## 一覧
```
awslocal sqs list-queues
```

## 属性の確認
下記を確認したいときはこれを使う
- queueのarn(QueueArn)
- メッセージ数(ApproximateNumberOfMessages)
```
awslocal sqs get-queue-attributes --queue-url http://localhost:4566/000000000000/test-queue --attribute-names All
```

## メッセージ送信
```
awslocal sqs send-message --queue-url http://localhost:4566/000000000000/test-queue --message-body "hello sqs"
```

## メッセージ消費
```
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/test-queue 
```

## メッセージ削除
- receive-messageで取得できるReciptHandleで削除する
```
awslocal sqs delete-message --queue-url http://localhost:4566/000000000000/test-queue --receipt-handle "drukdarzwcktvmxfwyixmllekpetzzzpfmeeoncimtizupetgcygvnrsylyvfvfekyldlynnfpluamonghracakmtnczywzzhzssecjuymyodaucglnjrdpxhrkpevgatacrtxraakgyblhvugouluqqilvsckjxudzflkhubuwnphpbovksgrenr"
```

## lambdaにイベントを登録する
- lambdaの節を参照
# cloudwatch

## 一覧

```
awslocal cloudwatch list-metrics
```


# 参考URL

- [localstackに向けてteraform](https://future-architect.github.io/articles/20201113/)



# cdklocal

- [ローカルで行うCDK](https://github.com/localstack/aws-cdk-local)
- nodenv経由でnodeがインストールされているなら `nodenv rehash`

```
npm install -g aws-cdk-local aws-cdk
nodenv rehash
```
