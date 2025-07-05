import hashlib
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class AuditLogger:
    def __init__(self, private_key_path: str):
        with open(private_key_path, 'rb') as key_file:
            self.private_key = load_pem_private_key(
                key_file.read(),
                password=None
            )
        self.log = []
    
    def log_decision(self, prompt: str, response: str, context: dict) -> str:
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'prompt': prompt,
            'response': response,
            'context': context
        }
        entry_str = json.dumps(entry, sort_keys=True)
        entry_id = hashlib.sha256(entry_str.encode()).hexdigest()
        
        signature = self.private_key.sign(
            entry_str.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        self.log.append({
            'id': entry_id,
            'entry': entry,
            'signature': signature.hex()
        })
        return entry_id
