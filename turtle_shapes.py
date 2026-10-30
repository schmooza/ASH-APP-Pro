"""Student-friendly Turtle shape library. Each function RETURNS drawing instructions.
Use these functions inside student_images.py; do not call turtle directly.
Coordinates are grid units (-5 to 5 on the classroom grid).
"""
import math
from teacher_sequence import triangle_shape, square_shape, rectangle_shape, pentagon_shape, hexagon_shape, star_shape

def _begin(x, y, angle, color, width, speed, fill):
    commands = [("color", color), ("width", width),
                ("up", x, y), ("heading", angle), ("down",)]
    if speed is not None:
        commands.insert(0, ("speed", int(speed)))
    if fill:
        commands += [("fillcolor", fill if isinstance(fill, str) else color), ("begin_fill",)]
    return commands

def _finish(commands, fill):
    if fill:
        commands.append(("end_fill",))
    commands.append(("up",))
    return commands

def triangle(x=0, y=0, size=3, angle=0, color="blue", fill=None, speed=None, width=3):
    c=_begin(x,y,angle,color,width,speed,fill)
    c += [("repeat",3),("forward",size),("turn",120),("end_repeat",)]
    return _finish(c,fill)

def square(x=0, y=0, size=2, angle=0, color="green", fill=None, speed=None, width=3):
    return rectangle(x,y,size,size,angle,color,fill,speed,width)

def rectangle(x=0, y=0, width=4, height=2, angle=0, color="blue", fill=None, speed=None, line_width=3):
    c=_begin(x,y,angle,color,line_width,speed,fill)
    c += [("repeat",2),("forward",width),("turn",90),
          ("forward",height),("turn",90),("end_repeat",)]
    return _finish(c,fill)

def _polygon(sides,x,y,size,angle,color,fill,speed,width):
    c=_begin(x,y,angle,color,width,speed,fill)
    c += [("repeat",sides),("forward",size),("turn",360/sides),("end_repeat",)]
    return _finish(c,fill)

def pentagon(x=0,y=0,size=2,angle=0,color="orange",fill=None,speed=None,width=3):
    return _polygon(5,x,y,size,angle,color,fill,speed,width)

def hexagon(x=0,y=0,size=2,angle=0,color="purple",fill=None,speed=None,width=3):
    return _polygon(6,x,y,size,angle,color,fill,speed,width)

def star(x=0,y=0,size=3,angle=0,color="gold",fill=None,speed=None,width=3):
    c=_begin(x,y,angle,color,width,speed,fill)
    c += [("repeat",5),("forward",size),("turn",144),("end_repeat",)]
    return _finish(c,fill)

def circle(x=0,y=0,radius=1,angle=0,color="purple",fill=None,speed=None,width=3):
    c=_begin(x,y,angle,color,width,speed,fill)
    c += [("curve",radius,360)]
    return _finish(c,fill)

def spiral(x=0,y=0,turn=90,steps=14,growth=0.25,angle=0,color="purple",speed=None,width=3):
    c=_begin(x,y,angle,color,width,speed,None)
    for i in range(1,steps+1):
        c += [("forward",round(i*growth,3)),("turn",turn)]
    return _finish(c,None)

def letter_a(x=0,y=0,size=3,color="red",speed=None,width=4):
    c=_begin(x,y,65,color,width,speed,None)
    c += [("forward",size),("heading",295),("forward",size),
          ("up",x+size*0.25,y+size*0.38),("heading",0),("down",),
          ("forward",size*0.35)]
    return _finish(c,None)

def letter_h(x=0,y=0,size=3,color="purple",speed=None,width=4):
    c=_begin(x,y,90,color,width,speed,None)
    c += [("forward",size),("up",x+size*0.6,y),("heading",90),("down",),
          ("forward",size),("up",x,y+size/2),("heading",0),("down",),
          ("forward",size*0.6)]
    return _finish(c,None)

def letter_s(x=0,y=0,radius=1,color="purple",speed=None,width=4):
    # Two opposite arcs, joined tangentially. Start at top of letter.
    c=_begin(x,y,180,color,width,speed,None)
    c += [("curve",radius,180),("curve",radius,-180)]
    return _finish(c,None)

def venetian_blind(x=-4,y=-3,width=8,slats=7,slat_height=0.55,gap=0.3,
                   color="steelblue",fill="lightblue",speed=None,line_width=2):
    """Stack horizontal slats. y is the bottom of the first slat."""
    if slats < 1 or int(slats)!=slats:
        raise ValueError("slats must be a positive whole number")
    c=[]
    for i in range(int(slats)):
        c += rectangle(x,y+i*(slat_height+gap),width,slat_height,
                       color=color,fill=fill,speed=speed,line_width=line_width)
    return c

def zigzag(x=-4,y=0,steps=6,segment=1,angle=45,color="orange",speed=None,width=3):
    c=_begin(x,y,angle,color,width,speed,None)
    for i in range(steps):
        c += [("forward",segment),("turn",-2*angle if i%2==0 else 2*angle)]
    return _finish(c,None)

def repeat_shape(shape, count=3, x=0, y=0, dx=1, dy=0, spacing=None,
                 rotate=0, fill=None, random_fill=False, palette=None, **kwargs):
    """Repeat a shape function or a custom command list.

    rotate: degrees added to each new copy (0, 45, 90, ...).
    fill: one fill colour for all copies, e.g. fill="yellow".
    random_fill: True chooses a different random fill for each copy.
    palette: optional list of fill colours for random_fill.
    For custom lists, rotation is around the first ('up', x, y) point.
    """
    import random
    if not isinstance(count, int) or count < 0:
        raise ValueError("count must be a whole number of 0 or more")
    if spacing is not None:
        dx = spacing
    colors = palette if palette is not None else ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
    if random_fill and not colors:
        raise ValueError("palette must contain at least one colour")
    commands = []
    if callable(shape):
        for i in range(count):
            options = dict(kwargs)
            options["angle"] = options.get("angle", 0) + i * rotate
            chosen_fill = random.choice(colors) if random_fill else fill
            if chosen_fill is not None:
                options["fill"] = chosen_fill
            try:
                commands.extend(shape(x=x + i * dx, y=y + i * dy, **options))
            except TypeError as exc:
                if "angle" in str(exc) or "fill" in str(exc):
                    raise TypeError("This shape function does not support angle or fill; use a drawing command list instead") from exc
                raise
    elif isinstance(shape, (list, tuple)):
        if kwargs:
            raise TypeError("Extra shape options only work with shape functions")
        anchor = next(((cmd[1], cmd[2]) for cmd in shape
                       if isinstance(cmd, (list, tuple)) and len(cmd) == 3 and cmd[0] == "up"), (0, 0))
        for i in range(count):
            theta = math.radians(i * rotate)
            cs, sn = math.cos(theta), math.sin(theta)
            offset_x, offset_y = x + i * dx, y + i * dy
            chosen_fill = random.choice(colors) if random_fill else fill
            has_fill = any(cmd[0] == "begin_fill" for cmd in shape if isinstance(cmd, (list, tuple)) and cmd)
            if chosen_fill is not None and not has_fill:
                # Add fill commands around the whole drawing. Multiple disconnected
                # parts may fill as a single region; use a shape function for best results.
                commands.append(("fillcolor", chosen_fill))
                commands.append(("begin_fill",))
            for cmd in shape:
                if not isinstance(cmd, (tuple, list)) or not cmd:
                    raise TypeError("Custom drawings must contain drawing command tuples")
                op = cmd[0]
                if op == "up" and len(cmd) == 3:
                    px, py = cmd[1] - anchor[0], cmd[2] - anchor[1]
                    commands.append(("up", anchor[0] + px * cs - py * sn + offset_x,
                                     anchor[1] + px * sn + py * cs + offset_y))
                elif op == "heading" and len(cmd) == 2:
                    commands.append(("heading", cmd[1] + i * rotate))
                elif op == "fillcolor" and chosen_fill is not None:
                    commands.append(("fillcolor", chosen_fill))
                else:
                    commands.append(tuple(cmd))
            if chosen_fill is not None and not has_fill:
                commands.append(("end_fill",))
    else:
        raise TypeError("Use a shape function or a list of drawing commands")
    return commands

def growing_shapes(shape_function, count=3, x=0, y=0, start_size=1, step=0.5, **kwargs):
    c=[]
    for i in range(count):
        c += shape_function(x=x,y=y,size=start_size+i*step,**kwargs)
    return c

def random_colors(shape_function, count=4, palette=None, x=0,y=0,dx=1,dy=0,**kwargs):
    import random
    palette=palette or ["red","orange","green","blue","purple"]
    c=[]
    for i in range(count):
        c += shape_function(x=x+i*dx,y=y+i*dy,color=random.choice(palette),**kwargs)
    return c
