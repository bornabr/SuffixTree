def SimpleFastaParser(handle):
	# Skip any text before the first record (e.g. blank lines, comments)
	for line in handle:
		if line[0] == ">":
			title = line[1:].rstrip()
			break
	else:
		# no break encountered - probably an empty file
		return

	# Main logic
	# Note, remove trailing whitespace, and any internal spaces
	# (and any embedded \r which are possible in mangled files
	# when not opened in universal read lines mode)
	lines = []
	for line in handle:
		if len(line) > 0 and line[0] == ">":
			if len(lines) > 0:
				yield title, "".join(lines).replace(" ", "")
			lines = []
			title = line[1:].rstrip()
			continue
		lines.append(line.rstrip())

	yield title, "".join(lines).replace(" ", "").replace("\r", "")
