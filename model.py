def load_obj(file):
    vertex, faces = [], []
    with open(file) as f:
        for line in f:
            if line.startswith('v '):
                vertex.append([float(i) for i in line.split()[1:]] + [1])
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                faces.append([int(faces_[face_].split('/')[0]) - 1 for face_ in range(3)])
    return [vertex, faces]