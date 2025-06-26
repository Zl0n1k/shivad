from aiobotocore.session import get_session
from marshmallow import Schema, INCLUDE, fields
from shiva.common.driver import BaseDriver


def client_context(fnc):
    async def wrapper(*args, **kwargs):
        self = args[0]
        async with self.session.create_client(
            endpoint_url=self.config["endpoint_url"],
            service_name=self.config.get("service_name", "s3"),
            aws_access_key_id=self.config["aws_access_key_id"],
            aws_secret_access_key=self.config["aws_secret_access_key"],
        ) as client:
            bucket = kwargs.get("bucket") or self.bucket
            if not bucket:
                raise Exception("Empty bucket")
            kwargs["bucket"] = bucket
            kwargs["client"] = client
            result = await fnc(*args, **kwargs)
            return result

    return wrapper


class Config(Schema):
    class Meta:
        unknown = INCLUDE

    endpoint_url = fields.String(required=True)
    aws_access_key_id = fields.String(required=True)
    aws_secret_access_key = fields.String(required=True)
    bucket = fields.String(required=True)


class s3Api(BaseDriver):
    name = "s3"

    def validate(self):
        self.config = Config().load(self.config)

    async def prepare(self):
        self.validate()
        self.session = get_session()
        self.bucket = self.config["bucket"]

    @client_context
    async def get_file(self, file_path, bucket, client):
        # res = await client.generate_presigned_url('get_object', Params={'Bucket': 'insurancedev', 'Key': 'bpm/test.pdf'}, ExpiresIn=600)
        # print(res)
        obj = await client.get_object(Bucket=bucket, Key=file_path)
        return await obj["Body"].read()

    @client_context
    async def put_file(self, file_path, body, bucket, client):
        result = await client.put_object(Bucket=bucket, Key=file_path, Body=body)
        return result

    @client_context
    async def publish_file_link(self, filename, expire, bucket, client):
        link = await client.generate_presigned_url(
            "get_object", Params={"Bucket": bucket, "Key": filename}, ExpiresIn=expire
        )
        return link

    @client_context
    async def delete_file(self, file_path, bucket, client):
        result = await client.delete_object(Bucket=bucket, Key=file_path)
        return result

    @client_context
    async def metadata_file(self, file_path, bucket, client):
        result = await client.head_object(Bucket=bucket, Key=file_path)
        return result

    async def stop(self):
        pass
