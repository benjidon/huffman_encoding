#huffman.py
#Authored by Benjamin Don

class HuffmanNode:
	"""Class definition to set up the nodes that will be used"""
	def __init__(self,freq,char):
		self.interNode = None
		self.leafNode = None
		self.char = ord(char)
		self.right = None
		self.left = None
		self.parent = None
		self.freq = freq

def cnt_freq(filename):
	"""Function that reads a string within a file and adds the frequencies of each 
	character to a list, finally returning the list"""
	charList = [0] * 256
	f = open(filename,'r')

	while True:
		filechar = f.read(1)

		if not filechar:
			break
		else:
			charList[ord(filechar)] += 1

	f.close()

	return charList

def findMin(lst):
	"""Helper function to find the minimum frequency of a character in the list"""

	minimum = lst[0]
	for i in range(len(lst) - 1):
		if minimum.freq > lst[i + 1].freq:
			minimum = lst[i + 1]
		elif minimum.freq == lst[i + 1].freq:
			if minimum.char > lst[i + 1].char:
				minimum = lst[i + 1]

	return minimum


def create_huff_tree(list_of_freqs):
	"""Function to create a huffman tree out of a frequency list"""
	nodeList = []
	index = 0

	for item in list_of_freqs:
		if item > 0:
			newNode = HuffmanNode(item,chr(index))
			nodeList.append(newNode)
			newNode.leafNode = True
		index += 1


	while len(nodeList) > 1:
		min1 = findMin(nodeList)
		nodeList.remove(min1)
		min2 = findMin(nodeList)
		nodeList.remove(min2)

		if min1.char > min2.char:
			insertNode = HuffmanNode(min1.freq + min2.freq, chr(min2.char))
			insertNode.left = min1
			insertNode.right = min2
			insertNode.left.parent = insertNode
			insertNode.right.parent = insertNode
			insertNode.interNode = True
			insertNode.leafNode = False
			nodeList.append(insertNode)

		else:
			insertNode = HuffmanNode(min1.freq + min2.freq, chr(min1.char))
			insertNode.left = min1
			insertNode.right = min2
			insertNode.left.parent = insertNode
			insertNode.right.parent = insertNode
			insertNode.interNode = True
			insertNode.leafNode = False
			nodeList.append(insertNode)

	return nodeList[0]


def create_code(root_node,codeList = [""]*256):
	"""Function that creates a new list with associated code for each character rather than frequency counts"""
	if root_node.left:
		create_code(root_node.left)

	if not root_node.left and not root_node.right:
		codeList[ord(chr(root_node.char))] = find_code(root_node)

	elif root_node.right:
		create_code(root_node.right)

	return codeList

def find_code(leaf_node):
	"""Helper function for create_code, this finds the actual code for a given leaf node.
	Since this works from the leaf node up, another helper function is required to reverse the returned string."""
	codeString = ""

	while leaf_node.parent:

		if leaf_node.parent.left == leaf_node:
			codeString += "0"
			leaf_node = leaf_node.parent
		elif leaf_node.parent.right == leaf_node:
			codeString += "1"
			leaf_node = leaf_node.parent


	return reverse_dat_string(codeString)

def reverse_dat_string(datstr):
	"""Helper function for find_code, simply reverses the string to return the actual code"""
	size = len(datstr)

	if (size - 1) > 0:
		return datstr[size - 1] + reverse_dat_string(datstr[0:size - 1])
	else:
		return datstr

def huffman_encode(in_file,out_file):
	"""Function that reads an input file and returns the code version of each character,
	finally outputting the complete encoded string to a new file"""
	f = open(in_file,'r')

	freqList = cnt_freq(in_file)
	huffTree = create_huff_tree(freqList)
	huffCodeList = create_code(huffTree)
	outputstring = ""

	if not huffTree.right and not huffTree.left:
		outputstring = str(chr(huffTree.char)) + str(huffTree.freq)
		g = open(out_file,'w')
		g.write(outputstring)
		f.close()
		g.close()

	else:
		while True:
			filechar = f.read(1)

			if not filechar:
				break
			else:
				 outputstring += huffCodeList[ord(filechar)]
		f.close()

		g = open(out_file,'w')
		g.write(outputstring)
		g.close()


def tree_preord(hufftree): #How should i handle trees with 1 node
	"""Function that returns a skeleton of the input huffman tree"""
	returnstring = ""

	if hufftree.interNode:
		returnstring += "0"
	elif hufftree.leafNode:
		returnstring = returnstring + "1" + str(chr(hufftree.char))
	if hufftree.left:
		returnstring += tree_preord(hufftree.left)
	if hufftree.right:
		returnstring += tree_preord(hufftree.right)

	return returnstring

def huffman_decode(freqs,encoded_file,decode_file):
	"""Function that takes an encoded file and decodes it to the original string using
	a huffman tree"""
	huffTree = create_huff_tree(freqs)
	outputstring = ""
	bitList = []
	rootNode = huffTree
	currentNode = rootNode

	f = open(encoded_file,'r')

	while True:
		filechar = f.read(1)
		if not filechar:
			break
		else:
			if filechar == "1":
				currentNode = currentNode.right
			elif filechar == "0":
				currentNode = currentNode.left
			if currentNode.leafNode:
				outputstring += str(chr(currentNode.char))
				currentNode = rootNode


	g = open(decode_file,'w')
	g.write(outputstring)
	g.close()


lst = [0] * 256
lst[97] = 2
lst[99] = 1
lst[110] = 1
lst[118] = 1
lst[115] = 1

tree = create_huff_tree(lst)
print(tree_preord(tree))




