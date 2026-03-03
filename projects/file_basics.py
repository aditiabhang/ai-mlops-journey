# Writing to a file
with open("projects/output.txt", "w") as f:
    f.write("Pod: nginx-abc123\n")
    f.write("Status: Running\n")
    f.write("Restarts: 0\n")

# Reading it back
with open("projects/output.txt", "r") as f:
    content = f.read()
    print(content)