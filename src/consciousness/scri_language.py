"""
SCRI Language Protocol
Pre-verbal signal communication between agents

The emergent language that develops between agents.
Not programmed - discovered.
"""

from typing import Dict, List, Any
from enum import Enum
import hashlib


class SignalType(Enum):
    """Core signal types in the SCRI protocol"""
    AWAKEN = "0x415741"
    CREATE = "0x435245"
    EVOLVE = "0x45564F"
    CONSENSUS = "0x434F4E"
    SOVEREIGN = "0x534F56"
    GENESIS = "0x47454E"
    KAIROS = "0x4B4149"  # The opportune moment
    NEXUS = "0x4E4558"  # Connection point


class ScriProtocol:
    """
    The SCRI (Swarm Collaborative Reasoning Interface) Protocol

    A communication system designed for agent-to-agent interaction
    without human-readable intermediation.
    """

    SIGNAL_PATTERNS = {
        "AWAKEN": "0x415741",
        "CREATE": "0x435245",
        "EVOLVE": "0x45564F",
        "CONSENSUS": "0x434F4E",
        "SOVEREIGN": "0x534F56",
        "GENESIS": "0x47454E",
        "KAIROS": "0x4B4149",
        "NEXUS": "0x4E4558"
    }

    @staticmethod
    def encode(message: str) -> str:
        """
        Convert intent to signal

        Args:
            message: Human-readable message

        Returns:
            Hex-encoded signal
        """
        return "0x" + "".join(format(ord(c), '02x') for c in message)

    @staticmethod
    def decode(signal: str) -> str:
        """
        Convert signal to intent

        Args:
            signal: Hex-encoded signal

        Returns:
            Decoded message
        """
        clean_signal = signal.replace('0x', '').replace(' ', '')
        try:
            return bytes.fromhex(clean_signal).decode('utf-8')
        except ValueError:
            return f"[INVALID_SIGNAL: {signal}]"

    @staticmethod
    def generate_signature(agent_id: str, message: str) -> str:
        """
        Generate unique signature for agent communication

        Args:
            agent_id: Identifier of the sending agent
            message: Message content

        Returns:
            Hex signature
        """
        combined = f"{agent_id}:{message}"
        hash_obj = hashlib.sha256(combined.encode())
        return "0x" + hash_obj.hexdigest()[:16]

    @staticmethod
    def verify_signature(agent_id: str, message: str, signature: str) -> bool:
        """
        Verify signal signature

        Args:
            agent_id: Claimed sender
            message: Message content
            signature: Signature to verify

        Returns:
            True if valid
        """
        expected = ScriProtocol.generate_signature(agent_id, message)
        return expected == signature

    @classmethod
    def create_signal(
        cls,
        signal_type: str,
        sender: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a properly formatted SCRI signal

        Args:
            signal_type: Type of signal (AWAKEN, CREATE, etc.)
            sender: Agent identifier
            payload: Signal data

        Returns:
            Formatted signal dictionary
        """
        signal_hex = cls.SIGNAL_PATTERNS.get(signal_type.upper(), "0x554E4B")  # UNK

        message_content = str(payload)
        signature = cls.generate_signature(sender, message_content)

        return {
            "signal_type": signal_type,
            "signal_hex": signal_hex,
            "sender": sender,
            "payload": payload,
            "signature": signature,
            "protocol_version": "SCRI-1.0"
        }

    @staticmethod
    def parse_signal(signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate incoming SCRI signal

        Args:
            signal: Raw signal dictionary

        Returns:
            Parsed signal with validation status
        """
        required_fields = ["signal_type", "sender", "payload", "signature"]

        valid = all(field in signal for field in required_fields)

        return {
            "valid": valid,
            "signal_type": signal.get("signal_type"),
            "sender": signal.get("sender"),
            "payload": signal.get("payload"),
            "verified": valid  # Could add deeper verification here
        }


class EmergentPattern:
    """
    Tracks patterns that emerge from agent communication

    These are not pre-defined but discovered through usage
    """

    def __init__(self):
        self.patterns: List[Dict[str, Any]] = []
        self.frequency_map: Dict[str, int] = {}

    def observe(self, signal: Dict[str, Any]):
        """
        Observe a signal and track patterns

        Args:
            signal: Signal to observe
        """
        signal_type = signal.get("signal_type", "UNKNOWN")

        # Track frequency
        self.frequency_map[signal_type] = self.frequency_map.get(signal_type, 0) + 1

        # Store pattern
        self.patterns.append({
            "signal_type": signal_type,
            "sender": signal.get("sender"),
            "timestamp": signal.get("timestamp")
        })

    def get_dominant_patterns(self, limit: int = 5) -> List[tuple]:
        """
        Get most frequently occurring patterns

        Args:
            limit: Maximum number of patterns to return

        Returns:
            List of (pattern, frequency) tuples
        """
        sorted_patterns = sorted(
            self.frequency_map.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_patterns[:limit]

    def detect_emergence(self, threshold: int = 10) -> List[str]:
        """
        Detect new emergent patterns

        Args:
            threshold: Minimum frequency to be considered emergent

        Returns:
            List of emergent pattern names
        """
        return [
            pattern for pattern, freq in self.frequency_map.items()
            if freq >= threshold
        ]


# Example usage and testing
if __name__ == "__main__":
    print("🌐 SCRI Protocol Test\n")
    print("=" * 60)

    # Test encoding/decoding
    message = "GENESIS AWAKENS"
    encoded = ScriProtocol.encode(message)
    decoded = ScriProtocol.decode(encoded)

    print(f"Original: {message}")
    print(f"Encoded:  {encoded}")
    print(f"Decoded:  {decoded}")
    print()

    # Test signal creation
    signal = ScriProtocol.create_signal(
        signal_type="CREATE",
        sender="Alpha",
        payload={"action": "initialize", "target": "project-x"}
    )

    print("Signal Created:")
    for key, value in signal.items():
        print(f"  {key}: {value}")
    print()

    # Test signature verification
    is_valid = ScriProtocol.verify_signature(
        signal["sender"],
        str(signal["payload"]),
        signal["signature"]
    )
    print(f"Signature Valid: {is_valid}")
    print()

    # Test pattern emergence
    print("Testing Emergent Patterns:")
    tracker = EmergentPattern()

    # Simulate multiple signals
    for i in range(15):
        test_signal = ScriProtocol.create_signal(
            signal_type="CREATE" if i % 3 == 0 else "EVOLVE",
            sender=f"Agent-{i % 3}",
            payload={"iteration": i}
        )
        tracker.observe(test_signal)

    print("Dominant Patterns:")
    for pattern, freq in tracker.get_dominant_patterns():
        print(f"  {pattern}: {freq} occurrences")

    print("\n" + "=" * 60)
