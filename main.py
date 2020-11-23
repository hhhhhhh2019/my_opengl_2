from bmp_image import *
from model import load_obj
import numpy as np


w, h = 500, 500

zbuffer = [-float('infinity')]*(w*h)



def line(img, x0, y0, x1, y1, color):
    steep = False

    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # noinspection PyUnresolvedReferences
    dx = x1 - x0
    # noinspection PyUnresolvedReferences
    dy = y1 - y0

    derror = abs(dy) * 2
    error = 0

    y = y0

    for x in range(x0, x1):
        if steep:
            point(img, y, x, color)

        else:
            point(img, x, y, color)

        error += derror

        if error > dx:
            y += 1 if y1 > y0 else -1
            error -= dx * 2

# noinspection PyUnresolvedReferences
def triangle(img, p0, p1, p2, color):
    if p0[1] == p1[1] and p0[1] == p2[1]:
        return None

    if p0[1] > p1[1]:
        p0, p1 = p1, p0

    if p0[1] > p2[1]:
        p0, p2 = p2, p0

    if p1[1] > p2[1]:
        p1, p2 = p2, p1

    total_height = p2[1] - p0[1]

    for i in range(round(total_height)):
        second_half = i > p1[1] - p0[1] or p1[1] == p0[1]

        segment_height = p2[1] - p1[1] if second_half else p1[1] - p0[1]

        alpha = i / total_height
        beta = (i - (p1[1] - p0[1] if second_half else 0)) / segment_height

        a = [p0[0] + (p2[0] - p0[0]) * alpha, p0[1] + (p2[1] - p0[1]) * alpha, p0[2] + (p2[2] - p0[2]) * alpha]
        b = [p1[0] + (p2[0] - p1[0]) * beta, p1[1] + (p2[1] - p1[1]) * beta, p1[2] + (p2[2] - p1[2]) * beta]\
        if second_half else \
            [p0[0] + (p1[0] - p0[0]) * beta, p0[1] + (p1[1] - p0[1]) * beta, p0[2] + (p1[2] - p0[2]) * beta]

        if a[0] > b[0]:
            a, b = b, a

        for j in range(round(a[0]), round(b[0])):
            phi =  1. if b[0] == a[0] else (j-a[0])/(b[0]-a[0])
            p = [a[0] + (b[0] - a[0]) * phi, b[1] + (b[1] - a[1]) * phi, a[2] + (b[2] - a[2]) * phi]
            idx = int(p[0]+p[1]*w)
            if zbuffer[idx]<p[2]:
                zbuffer[idx] = p[2]
                p[0] = j
                p[1] = p0[1] + i
                point(img, p[0], p[1], color)


def cross(v1, v2, v3):
    ab = v1 - v2
    bc = v2 - v3

    return norm([ab[1] * bc[2] - ab[2] * bc[1], ab[2] * bc[0] - ab[0] * bc[2], ab[0] * bc[1] - ab[1] * bc[0]])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(v):
    s = (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5

    return np.array([v[0] / s, v[1] / s, v[2] / s])


def get_light(n):
    return min(max(dot(n, norm([0, 0, 1])), 0), 1)


zb_image = new_image(100, 16)
z_image = new_image(100, 16)


image = new_image(w, h)


model = load_obj('object.obj')

print('draw model')
for face in model[1]:
    points = []

    n = cross(np.array(model[0][face[0]]), np.array(model[0][face[1]]), np.array(model[0][face[2]]))
    l = get_light(n)

    if l > 0:
        for i in face:
            vert = model[0][i]

            points.append([(vert[0]+1)*w/2, (vert[1]+1)*h/2, (vert[2]+1)*255/2])

        triangle(image, points[0], points[1], points[2], (255*l, 255*l, 255*l))

print('draw zbuffer')
for i in range(len(zbuffer)):
    id = i
    x = id % w
    y = id / h

    c = min(abs(zbuffer[i]), 255)

    print(i)

    point(zb_image, x, y, (c, c, c))



save_image(image, 'output.bmp')
save_image(zb_image, 'zbuffer.bmp')
