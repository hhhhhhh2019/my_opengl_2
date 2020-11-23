def list_to_string(s):
	str1 = ""

	for i in s:

		str1 += i

	return str1


def save_image(arr, file):
	with open(file,"w+b") as f:
		f.write(b'BM')#ID field (42h, 4Dh)
		f.write((154).to_bytes(4,byteorder="little"))
		f.write((0).to_bytes(2,byteorder="little"))
		f.write((0).to_bytes(2,byteorder="little"))
		f.write((122).to_bytes(4,byteorder="little"))
		f.write((108).to_bytes(4,byteorder="little"))
		f.write((arr[0]).to_bytes(4,byteorder="little"))
		f.write((arr[1]).to_bytes(4,byteorder="little"))
		f.write((2).to_bytes(2,byteorder="little"))
		f.write((32).to_bytes(2,byteorder="little"))
		f.write((3).to_bytes(4,byteorder="little"))
		f.write((32).to_bytes(4,byteorder="little"))
		f.write((2835).to_bytes(4,byteorder="little"))
		f.write((2835).to_bytes(4,byteorder="little"))
		f.write((0).to_bytes(4,byteorder="little"))
		f.write((0).to_bytes(4,byteorder="little"))
		f.write(b'\xFF\x00\x00\x00')
		f.write(b'\x00\xFF\x00\x00')
		f.write(b'\x00\x00\xFF\x00')
		f.write(b'\x00\x00\x00\xFF')
		f.write(b' niW')
		f.write((0).to_bytes(36,byteorder="little"))
		f.write((0).to_bytes(4,byteorder="little"))
		f.write((0).to_bytes(4,byteorder="little"))
		f.write((0).to_bytes(4,byteorder="little"))

		for i in arr[2]:
			for col in i:
				#print(col)
				color = b""
				for c in col:
					#print(c)
					cl = list(hex(max(0, c))[2:])
					if len(cl) == 1:
						cl.insert(0, "0")
					color += bytes.fromhex(list_to_string(cl))

				f.write(color)


def new_image(w, h, color=(0, 0, 0, 255)):
	res = [w, h]

	img = []

	for i in range(h):
		row = []

		for j in range(w):
			row.append(color)

		img.append(row)

	res.append(img)

	return res


def point(arr, x, y, color):
	if x > arr[0] or y > arr[1] or x < 0 or y < 0:
		return

	y, x = min(arr[1]-1, int(y)-1), min(arr[0]-1, int(x))

	#print(x, y)

	color = list(color)

	color[0] = int(color[0])
	color[1] = int(color[1])
	color[2] = int(color[2])

	arr[2][y][x] = tuple(list(color) + [255])
