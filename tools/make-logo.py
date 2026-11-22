"""Cacofone lyre turned about the vertical axis: exact pinhole perspective in 3D.

World: the lyre's centre line lies in its own plane; the plane is turned THETA about the
vertical axis through the centre (32,32) and viewed by a pinhole camera at distance D
(image plane at the same distance, so the centre keeps its size).
  - Rods (arms, crossbar, strings): silhouette = the two lines on the tube where view rays
    are tangent, i.e. centre +/- r * normalize(tangent x view_ray), each projected.
  - Balls (finials, pegs, rod ends): exact sphere silhouette (the tangent circle of the
    view cone), projected. Off-axis spheres therefore become very slightly oval, as in a photo.
  - Base band: a flat plate in the lyre's plane, every point projected.
This is the main Cacofone logo. The shapes come from the upright design kept in
assets/logo-upright.svg (finials, pegs and strings tuned for this view).

Usage: python3 tools/make-logo.py assets/logo.svg"""
import math, sys

THETA = math.radians(45)
D = 56
CX = CY = 32
OPTICAL_CENTRE_FRAMING = False   # True: keep the camera's optical centre at the image centre

def world(x, y):
    X, Y = x - CX, y - CY
    return (X * math.cos(THETA), Y, X * math.sin(THETA))      # +z = away from camera
CAM = (0.0, 0.0, -D)
def P(p):  # project a world point
    s = D / (p[2] + D)
    return (p[0] * s, p[1] * s)

sub = lambda a, b: (a[0]-b[0], a[1]-b[1], a[2]-b[2])
add = lambda a, b: (a[0]+b[0], a[1]+b[1], a[2]+b[2])
mul = lambda a, k: (a[0]*k, a[1]*k, a[2]*k)
dot = lambda a, b: a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
cross = lambda a, b: (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def unit(a):
    L = math.sqrt(dot(a, a)) or 1
    return mul(a, 1 / L)

def cubic(p0, p1, p2, p3, n=64):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return out
def line(a, b, n=32):
    return [(a[0] + (b[0]-a[0])*i/n, a[1] + (b[1]-a[1])*i/n) for i in range(n + 1)]
def arc(cx, cy, r, a0, a1, n=24):
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*i/n)),
             cy + r*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n + 1)]

def area(ring):
    return sum(ring[i][0]*ring[(i+1) % len(ring)][1] - ring[(i+1) % len(ring)][0]*ring[i][1]
               for i in range(len(ring))) / 2
def orient(ring):
    return ring if area(ring) > 0 else ring[::-1]

def sphere(c, r, n=64):
    """Exact silhouette of a sphere (centre c in world space, radius r)."""
    v = sub(CAM, c); L2 = dot(v, v); w = unit(v)
    centre = add(c, mul(v, r*r / L2)); rad = r * math.sqrt(1 - r*r / L2)
    a = unit(cross(w, (0, 1, 0))); b = cross(w, a)
    return orient([P(add(centre, add(mul(a, rad*math.cos(2*math.pi*k/n)), mul(b, rad*math.sin(2*math.pi*k/n))))) for k in range(n)])

def ball(x, y, r):
    return [sphere(world(x, y), r)]

def rod(src, diameter):
    """Exact tube silhouette along a centre line, with spherical (round) ends."""
    r = diameter / 2
    W = [world(x, y) for x, y in src]
    left, right = [], []
    for i, p in enumerate(W):
        t = unit(sub(W[min(i+1, len(W)-1)], W[max(i-1, 0)]))
        n = unit(cross(t, sub(p, CAM)))
        left.append(P(add(p, mul(n, r)))); right.append(P(sub(p, mul(n, r))))
    return [orient(left + right[::-1]), sphere(W[0], r), sphere(W[-1], r)]

def plate_rim(src, width):
    n = len(src); h = width / 2; outer, inner = [], []
    for i, (x, y) in enumerate(src):
        a, b = src[i-1], src[(i+1) % n]
        dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy)
        nx, ny = -dy/L, dx/L
        outer.append((x + nx*h, y + ny*h)); inner.append((x - nx*h, y - ny*h))
    if abs(area(outer)) < abs(area(inner)):   # offset direction depends on winding: name them by size
        outer, inner = inner, outer
    pr = lambda ring: [P(world(x, y)) for x, y in ring]
    return [pr(outer), pr(inner)], pr(inner)

elements = []   # (rings, attrs)
for s in (1, -1):
    m = (lambda x: x) if s == 1 else (lambda x: 64 - x)
    end = 22.6 if s == 1 else 41.4
    pts = line((m(20), 15.5), (m(20), 18), 6)[:-1] \
        + cubic((m(20), 18), (m(20.3), 23), (m(21), 28.5), (m(18), 32)) \
        + cubic((m(18), 32), (m(12), 40), (m(15), 47), (end, 48.9))[1:]
    elements.append((rod(pts, 3.4), ''))
elements.append((rod(line((20.2, 22.5), (43.8, 22.5), 48), 2.6), ''))
for x in (26, 30, 34, 38):
    elements.append((ball(x, 19.95, 1.25), ''))
for x in (20, 44):
    elements.append((ball(x, 15.6, 2.6), ''))
for x in (26, 30, 34, 38):
    elements.append((rod(line((x, 22.5), (x, 45.4), 24), 1.1), ''))
band = arc(37, 49, 3, -90, 90, 32)[:-1] + arc(27, 49, 3, 90, 270, 32)[:-1]
rim, inside = plate_rim(band, 2.6)
elements.append(([inside], ' fill-opacity="0.2"'))
elements.append((rim, ' fill-rule="evenodd"'))

xs = [x for rings, _ in elements for r in rings for x, _ in r]
ys = [y for rings, _ in elements for r in rings for _, y in r]
if OPTICAL_CENTRE_FRAMING:
    ox, oy = CX, CY
else:
    ox = CX - (min(xs) + max(xs)) / 2; oy = CY - (min(ys) + max(ys)) / 2
def d(rings):
    return " ".join("M" + " L".join(f"{x+ox:.2f} {y+oy:.2f}" for x, y in r) + " Z" for r in rings)

out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Cacofone lyre logo">',
       f'  <!-- Lyre turned {math.degrees(THETA):.0f} degrees about the vertical axis, exact pinhole perspective (camera distance {D}). Generated by tools/make-logo.py; do not hand-edit. -->',
       '  <g id="lyre" fill="currentColor">']
out += [f'    <path{attrs} d="{d(rings)}"/>' for rings, attrs in elements]
out += ['  </g>', '</svg>', '']
open(sys.argv[1], "w").write("\n".join(out))
print(f"bbox w={max(xs)-min(xs):.2f} h={max(ys)-min(ys):.2f}")
