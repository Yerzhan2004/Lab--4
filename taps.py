import hashlib
import time
import random
from threading import Thread, Lock


class Block:
    def __init__(self, index, previous_hash, transactions, difficulty=4, reward=10):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = None
        self.difficulty = difficulty
        self.reward = reward

    def mine_block(self):
        prefix = '0' * self.difficulty
        while True:
            self.nonce = random.randint(0, int(1e6))
            self.hash = self.calculate_hash()
            if self.hash.startswith(prefix):
                return self.hash

    def calculate_hash(self):
        block_data = f'{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}'
        return hashlib.sha256(block_data.encode()).hexdigest()


class Blockchain:
    def __init__(self, difficulty=4, reward=10):
        self.difficulty = difficulty  # Теперь переменные объявлены перед вызовом create_genesis_block
        self.reward = reward
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.lock = Lock()
        self.stakes = {}

    def create_genesis_block(self):
        genesis_block = Block(0, '0', [], self.difficulty, self.reward)
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        with self.lock:
            if not self.pending_transactions:
                print(f'Нет транзакций для майнинга {miner_address}')
                return

            new_block = Block(len(self.chain), self.chain[-1].hash, self.pending_transactions, self.difficulty,
                              self.reward)
            mined_hash = new_block.mine_block()
            self.chain.append(new_block)
            self.pending_transactions = [f'Reward to {miner_address}: {self.reward}']
            print(f'Miner {miner_address} mined block {new_block.index} with hash {mined_hash}')

    def stake(self, validator, amount):
        if validator in self.stakes:
            self.stakes[validator] += amount
        else:
            self.stakes[validator] = amount

    def select_validator(self):
        total_stake = sum(self.stakes.values())
        if total_stake == 0:
            return None

        rand_point = random.uniform(0, total_stake)
        cumulative = 0
        for validator, stake in self.stakes.items():
            cumulative += stake
            if cumulative >= rand_point:
                return validator
        return None

    def validate_block(self, transactions):
        validator = self.select_validator()
        if validator:
            print(f'Validator {validator} approved transactions: {transactions}')
            return True
        return False


# Создаем блокчейн
blockchain = Blockchain(difficulty=4, reward=10)

# Имитация транзакций
blockchain.add_transaction("Alice -> Bob: 5 BTC")
blockchain.add_transaction("Bob -> Charlie: 2 BTC")

# Два майнера соревнуются за нахождение nonce
miner1 = Thread(target=blockchain.mine_pending_transactions, args=("Miner1",))
miner2 = Thread(target=blockchain.mine_pending_transactions, args=("Miner2",))

miner1.start()
miner2.start()

miner1.join()
miner2.join()

# Стейкинг и выбор валидатора
blockchain.stake("Validator1", 50)
blockchain.stake("Validator2", 30)
blockchain.stake("Validator3", 20)

validator = blockchain.select_validator()
if validator:
    blockchain.validate_block(blockchain.pending_transactions)

# Выводим блокчейн
for block in blockchain.chain:
    print(
        f'Block {block.index}: Hash {block.hash}, Prev Hash {block.previous_hash}, Transactions: {block.transactions}')
