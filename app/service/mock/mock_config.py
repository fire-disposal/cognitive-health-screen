# 虚拟病人/设备/绑定配置结构示例

MOCK_CONFIG = {
    "patients": [
        {
            "id": "patient_001",
            "name": "张三",
            "age": 68,
            "gender": "male",
            "devices": [
                {
                    "type": "blood_pressure",
                    "sn": "BP10001",
                    "frequency": 60,
                    "bias": {"systolic": [120, 140], "diastolic": [80, 90]},
                    "count": 2
                },
                {
                    "type": "mattress",
                    "sn": "MT20001",
                    "frequency": 300,
                    "bias": {
                        "hb": [60, 90],
                        "br": [12, 20],
                        "st": [1, 1],
                        "we": [65, 80],
                        "wt": [3600, 7200],
                        "od": [0, 1],
                        "fv": [0, 1],
                        "p": [1, 3]
                    },
                    "count": 1
                }
            ]
        },
        {
            "id": "patient_002",
            "name": "李四",
            "age": 75,
            "gender": "female",
            "devices": [
                {
                    "type": "blood_pressure",
                    "sn": "BP20002",
                    "frequency": 120,
                    "bias": {"systolic": [140, 160], "diastolic": [90, 100]},
                    "count": 1
                },
                {
                    "type": "heart_rate",
                    "sn": "HR20002",
                    "frequency": 90,
                    "bias": {"rate": [80, 130]},
                    "count": 3
                },
                {
                    "type": "mattress",
                    "sn": "MT20002",
                    "frequency": 240,
                    "bias": {
                        "hb": [70, 110],
                        "br": [16, 28],
                        "st": [1, 1],
                        "we": [55, 70],
                        "wt": [4000, 8000],
                        "od": [0, 1],
                        "fv": [0, 1],
                        "p": [2, 4]
                    },
                    "count": 2
                }
            ]
        },
        {
            "id": "patient_003",
            "name": "王五",
            "age": 60,
            "gender": "male",
            "devices": [
                {
                    "type": "mattress",
                    "sn": "MT30003",
                    "frequency": 180,
                    "bias": {
                        "hb": [50, 70],
                        "br": [10, 16],
                        "st": [1, 1],
                        "we": [60, 90],
                        "wt": [2000, 6000],
                        "od": [0, 1],
                        "fv": [0, 1],
                        "p": [1, 5]
                    },
                    "count": 2
                }
            ]
        }
    ]
}