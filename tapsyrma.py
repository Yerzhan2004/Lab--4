import hashlib
import json
import time
import random

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount, signature):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'signature': signature
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

class Wallet:
    def __init__(self, owner):
        self.owner = owner
        self.private_key = str(random.randint(1000, 9999))  # Упрощенный "приватный ключ"
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()

    def sign_transaction(self, transaction):
        transaction_data = json.dumps(transaction, sort_keys=True).encode()
        return hashlib.sha256(transaction_data + self.private_key.encode()).hexdigest()

# Создаем блокчейн и кошелек
blockchain = Blockchain()
wallet = Wallet("User1")

while True:
    print("\nВыберите действие:")
    print("1. Добавить транзакцию")
    print("2. Майнить новый блок")
    print("3. Показать блокчейн")
    print("4. Выйти")

    choice = input("Ваш выбор: ")

    if choice == "1":
        sender = wallet.public_key
        recipient = input("Получатель: ")
        amount = float(input("Сумма: "))

        transaction = {"sender": sender, "recipient": recipient, "amount": amount}
        signature = wallet.sign_transaction(transaction)

        index = blockchain.add_transaction(sender, recipient, amount, signature)
        print(f"✅ Транзакция добавлена в блок {index}")

    elif choice == "2":
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block['proof'])
        blockchain.add_transaction(sender="0", recipient=wallet.public_key, amount=1, signature="Reward")
        previous_hash = blockchain.hash(last_block)
        block = blockchain.create_block(proof, previous_hash)
        print(f"✅ Новый блок {block['index']} замайнен!")

    elif choice == "3":
        for block in blockchain.chain:
            print(json.dumps(block, indent=4))

    elif choice == "4":
        break

    else:
        print("Неверный ввод, попробуйте снова.")
