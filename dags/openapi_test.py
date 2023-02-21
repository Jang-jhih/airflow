import requests

url = 'http://localhost:8080/openapi/entities/v1/'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMSIsImV4cCI6MTY1MDY2MDY1NSwianRpIjoiM2E4ZDY3ZTItOTM5Yi00NTY3LWE0MjYtZDdlMDA1ZGU3NjJjIiwic3ViIjoiZGF0YWh1YiIsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.pp_vW2u1tiiTT7U0nDF2EQdcayOMB8jatiOA8Je4JJA'
}

payload = [
    {
        "aspect": {
            "__type": "SchemaMetadata",
            "schemaName": "SampleHdfsSchema",
            "platform": "urn:li:dataPlatform:platform",
            "platformSchema": {
                "__type": "MySqlDDL",
                "tableSchema": "schema"
            },
            "version": 0,
            "created": {
                "time": 1621882982738,
                "actor": "urn:li:corpuser:etl",
                "impersonator": "urn:li:corpuser:jdoe"
            },
            "lastModified": {
                "time": 1621882982738,
                "actor": "urn:li:corpuser:etl",
                "impersonator": "urn:li:corpuser:jdoe"
            },
            "hash": "",
            "fields": [
                {
                    "fieldPath": "county_fips_codefg",
                    "jsonPath": "null",
                    "nullable": True,
                    "description": "null",
                    "type": {
                        "type": {
                            "__type": "StringType"
                        }
                    },
                    "nativeDataType": "String()",
                    "recursive": False
                },
                {
                    "fieldPath": "county_name",
                    "jsonPath": "null",
                    "nullable": True,
                    "description": "null",
                    "type": {
                        "type": {
                            "__type": "StringType"
                        }
                    },
                    "nativeDataType": "String()",
                    "recursive": False
                }
            ]
        },
        "entityType": "dataset",
        "entityUrn": "urn:li:dataset:(urn:li:dataPlatform:platform,testSchemaIngest,PROD)"
    }
]

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.content)
