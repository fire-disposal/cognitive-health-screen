from typing import List, Dict, Any
from app.service.mock.mock_config import MOCK_CONFIG

class VirtualPatient:
    def __init__(self, patient_info: Dict[str, Any]):
        self.id = patient_info.get("id")
        self.name = patient_info.get("name")
        self.age = patient_info.get("age")
        self.gender = patient_info.get("gender")
        self.devices = patient_info.get("devices", [])

class PatientManager:
    def __init__(self, config: Dict[str, Any]):
        self.patients: List[VirtualPatient] = [
            VirtualPatient(p) for p in config.get("patients", [])
        ]

    def get_patients(self) -> List[VirtualPatient]:
        return self.patients

    def get_devices(self, patient_id: str) -> List[Dict[str, Any]]:
        for patient in self.patients:
            if patient.id == patient_id:
                return patient.devices
        return []

    def all_devices(self) -> List[Dict[str, Any]]:
        devices = []
        for patient in self.patients:
            devices.extend(patient.devices)
        return devices