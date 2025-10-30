"""
Blockchain Ledger Implementation for IoT Security
Manages transactions, blocks, and chain validation
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import pickle


class Transaction:
    """Represents a blockchain transaction"""
    
    def __init__(self, tx_type: str, data: Dict[str, Any], did: str):
        self.tx_type = tx_type  # 'access', 'firmware', 'activity', 'alert'
        self.data = data
        self.did = did  # Decentralized Identifier
        self.timestamp = time.time()
        self.tx_hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calculate SHA-256 hash of transaction"""
        tx_string = json.dumps({
            'type': self.tx_type,
            'data': self.data,
            'did': self.did,
            'timestamp': self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary"""
        return {
            'tx_type': self.tx_type,
            'data': self.data,
            'did': self.did,
            'timestamp': self.timestamp,
            'tx_hash': self.tx_hash
        }


class Block:
    """Represents a block in the blockchain"""
    
    def __init__(self, index: int, transactions: List[Transaction], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = time.time()
        self.merkle_root = self._calculate_merkle_root()
        self.hash = self._calculate_hash()
    
    def _calculate_merkle_root(self) -> str:
        """Calculate Merkle root of transactions"""
        if not self.transactions:
            return hashlib.sha256(b'').hexdigest()
        
        tx_hashes = [tx.tx_hash for tx in self.transactions]
        
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 != 0:
                tx_hashes.append(tx_hashes[-1])
            
            new_hashes = []
            for i in range(0, len(tx_hashes), 2):
                combined = tx_hashes[i] + tx_hashes[i + 1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_hashes.append(new_hash)
            
            tx_hashes = new_hashes
        
        return tx_hashes[0]
    
    def _calculate_hash(self) -> str:
        """Calculate SHA-256 hash of block"""
        block_string = json.dumps({
            'index': self.index,
            'merkle_root': self.merkle_root,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'timestamp': self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'hash': self.hash
        }


class BlockchainLedger:
    """Main blockchain ledger for IoT security"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = 2  # Proof of work difficulty
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_tx = Transaction(
            tx_type='genesis',
            data={'message': 'IoT Security Blockchain Initialized'},
            did='DID:System:Genesis'
        )
        genesis_block = Block(0, [genesis_tx], '0')
        self.chain.append(genesis_block)
    
    def add_transaction(self, tx_type: str, data: Dict[str, Any], did: str) -> str:
        """Add a new transaction to pending transactions"""
        transaction = Transaction(tx_type, data, did)
        self.pending_transactions.append(transaction)
        return transaction.tx_hash
    
    def mine_pending_transactions(self, miner_did: str = 'DID:System:Miner') -> Block:
        """Mine pending transactions into a new block"""
        if not self.pending_transactions:
            return None
        
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=previous_block.hash
        )
        
        # Simple proof of work
        while not new_block.hash.startswith('0' * self.difficulty):
            new_block.nonce += 1
            new_block.hash = new_block._calculate_hash()
        
        self.chain.append(new_block)
        self.pending_transactions = []
        
        return new_block
    
    def validate_chain(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is correct
            if current_block.hash != current_block._calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Verify Merkle root
            if current_block.merkle_root != current_block._calculate_merkle_root():
                return False
        
        return True
    
    def get_transactions_by_did(self, did: str) -> List[Dict[str, Any]]:
        """Retrieve all transactions for a specific DID"""
        transactions = []
        for block in self.chain:
            for tx in block.transactions:
                if tx.did == did:
                    transactions.append(tx.to_dict())
        return transactions
    
    def get_transactions_by_type(self, tx_type: str) -> List[Dict[str, Any]]:
        """Retrieve all transactions of a specific type"""
        transactions = []
        for block in self.chain:
            for tx in block.transactions:
                if tx.tx_type == tx_type:
                    transactions.append(tx.to_dict())
        return transactions
    
    def get_latest_transaction(self, did: str, tx_type: str) -> Optional[Dict[str, Any]]:
        """Get the most recent transaction for a DID and type"""
        for block in reversed(self.chain):
            for tx in reversed(block.transactions):
                if tx.did == did and tx.tx_type == tx_type:
                    return tx.to_dict()
        return None
    
    def save_to_file(self, filename: str):
        """Save blockchain to file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_from_file(filename: str) -> 'BlockchainLedger':
        """Load blockchain from file"""
        with open(filename, 'rb') as f:
            return pickle.load(f)
    
    def get_chain_info(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        return {
            'total_blocks': len(self.chain),
            'total_transactions': total_transactions,
            'is_valid': self.validate_chain(),
            'latest_block_hash': self.chain[-1].hash if self.chain else None,
            'pending_transactions': len(self.pending_transactions)
        }


# Singleton instance
_blockchain_instance = None

def get_blockchain() -> BlockchainLedger:
    """Get or create blockchain singleton instance"""
    global _blockchain_instance
    if _blockchain_instance is None:
        _blockchain_instance = BlockchainLedger()
    return _blockchain_instance
