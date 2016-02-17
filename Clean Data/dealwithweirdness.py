with open('weirdness.txt', 'r') as f, open('ACT.csv','a') as f1:
	for line in f:
		print(line)
		print("x")
		f1.write(line)

