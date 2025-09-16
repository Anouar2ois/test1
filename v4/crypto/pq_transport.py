from typing import Tuple

class PQTransport:
	def handshake(self) -> Tuple[str, str]:
		# Simulate Kyber KEM + Dilithium signatures
		return ("kyber_shared_secret_synth", "dilithium_signature_synth")
