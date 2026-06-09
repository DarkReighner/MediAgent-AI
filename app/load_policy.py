from app.read_files import read_file
from app.rag import add_policy

policy = read_file("data/policy.txt")

add_policy(policy)

print("Policy Loaded")