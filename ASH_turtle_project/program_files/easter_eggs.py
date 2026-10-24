"""Secret logo drawings for the ASH Turtle app.

These are classroom-friendly approximations, not official brand artwork.
Each function returns drawing commands compatible with teacher_sequence.py.
"""
import math


def _path(points, color="black", fill=None, width=3):
    """Draw a connected path; close it and fill when requested."""
    if not points:
        return []
    commands = [("color", color), ("width", width), ("up", *points[0]), ("down",)]
    if fill is not None:
        commands += [("fillcolor", fill), ("begin_fill",)]
    for a, b in zip(points, points[1:] + ([points[0]] if fill is not None else [])):
        dx, dy = b[0]-a[0], b[1]-a[1]
        if math.hypot(dx, dy) > 1e-7:
            commands += [("heading", math.degrees(math.atan2(dy, dx))),
                         ("forward", math.hypot(dx, dy))]
    if fill is not None:
        commands.append(("end_fill",))
    commands.append(("up",))
    return commands


def _ellipse(cx, cy, rx, ry, color, fill=None, width=3, n=60, tilt=0):
    a = math.radians(tilt)
    pts=[]
    for i in range(n+1):
        t=2*math.pi*i/n
        x,y=rx*math.cos(t),ry*math.sin(t)
        pts.append((cx+x*math.cos(a)-y*math.sin(a), cy+x*math.sin(a)+y*math.cos(a)))
    return _path(pts, color, fill, width)


def _bezier(a,b,c,d,n=28):
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],
             (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1])
            for t in (i/n for i in range(n+1))]


def nike_logo():
    """Black swoosh inspired by the familiar sports logo."""
    outer=_bezier((-4.5,-0.7),(-4.0,-3.4),(-1.9,-2.4),(0.2,-1.5))
    outer+=_bezier((0.2,-1.5),(2.0,-0.7),(3.5,0.0),(4.7,1.3))[1:]
    inner=_bezier((4.7,1.3),(1.3,0.4),(-1.1,-0.8),(-2.7,-1.0))[1:]
    inner+=_bezier((-2.7,-1.0),(-3.7,-1.1),(-4.0,-0.5),(-3.7,0.4))[1:]
    return _path(outer+inner, "black", "black", 1)


def billabong_logo():
    """Two stylised surfing waves (Billabong-inspired)."""
    c=[]
    for offset, scale in [(-1.35,1.0),(1.35,0.85)]:
        top=_bezier((offset-1.35*scale,-0.6),(offset-0.6*scale,1.4),
                    (offset+0.3*scale,1.5),(offset+1.5*scale,-0.2))
        bottom=_bezier((offset+1.5*scale,-0.2),(offset+0.25*scale,0.4),
                       (offset-0.1*scale,-1.1),(offset-1.35*scale,-0.6))
        c+=_path(top+bottom,"black","black",1)
    return c


def toyota_logo():
    """Three overlapping red ovals."""
    c=_ellipse(0,0,3.6,2.25,"red",width=8)
    c+=_ellipse(0,0,1.25,2.15,"red",width=7)
    c+=_ellipse(0,0.6,2.4,1.1,"red",width=7)
    return c


def nasa_logo():
    """NASA-inspired blue badge with white stars and red orbital swoosh."""
    c=_ellipse(0,0,2.65,2.65,"#124b9a","#124b9a",width=1)
    for x,y in [(-1.7,1.4),(-1.2,-0.7),(0.7,1.75),(1.8,-0.6),(-0.1,-1.8)]:
        c+=_ellipse(x,y,0.09,0.09,"white","white",width=1,n=12)
    # Orbital stroke: short red segments across the blue badge.
    orbit=_bezier((-2.35,-1.4),(-0.7,0.7),(1.2,1.9),(2.45,2.8),n=30)
    c+=_path(orbit,"#e53935",width=9)
    # White lettering, constructed with strokes, to avoid unsupported text commands.
    letters={
      "N":[[(-1.75,-0.25),(-1.75,0.55),(-1.15,-0.25),(-1.15,0.55)]],
      "A":[[(-0.9,-0.25),(-0.6,0.55),(-0.3,-0.25)],[(-0.78,0.05),(-0.42,0.05)]],
      "S":[[(0.4,0.52),(0.0,0.52),(-0.02,0.18),(0.38,0.05),(0.36,-0.25),(-0.06,-0.25)]],
      "A2":[[(0.65,-0.25),(0.95,0.55),(1.25,-0.25)],[(0.77,0.05),(1.13,0.05)]]}
    for strokes in letters.values():
        for stroke in strokes: c+=_path(stroke,"white",width=5)
    return c


def dominoes_logo():
    """Domino's-inspired red/blue domino tiles and white pips."""
    c=[]
    for x,y,colour in [(-1.5,0.0,"#e72e37"),(1.0,0.0,"#1478bc")]:
        c+=_path([(x-1.2,y-1.25),(x+1.2,y-1.25),
                  (x+1.2,y+1.25),(x-1.2,y+1.25)],colour,colour,1)
    for x,y in [(-1.5,0.0),(0.45,0.65),(1.55,-0.65)]:
        c+=_ellipse(x,y,0.29,0.29,"white","white",1,24)
    return c
