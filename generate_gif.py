# -*- coding: utf-8 -*-
r"""
generate_gif.py
Genera una versión GIF animada de la tarjeta de perfil con interfaz de Windows Command Prompt (CMD),
con la versión mejorada del rostro ASCII en Consolas Regular 15pt (20px) idéntica a Bloc de Notas,
paleta limpia y minimalista, y las estadísticas y educación en inglés para @BlueberryMauro.
Compatible con Windows y Linux (GitHub Actions).
"""
import os
from PIL import Image, ImageDraw, ImageFont

raw_ascii_frames = {
    "center": [
        """    ."``````'.        """,
        """   /          \\       """,
        """  /   ________/       """,
        """  | .' ==  ==|        """,
        """  \\(\\=(_o)^(o)        """,
        """   |\\      | |        """,
        """   | \\     _)|        """,
        """   |\\ \\  ━_━/         """,
        """.'`| '.`__.'          """,
        """   \\     |_           """,
        """    '-__ / `-         """
    ],
    "left": [
        """    ."``````'.        """,
        """   /          \\       """,
        """  /   ________/       """,
        """  | .' ==  ==|        """,
        """  \\(\\=(o_)(o_)        """,
        """   |\\      | |        """,
        """   | \\     _)|        """,
        """   |\\ \\  ━_━/         """,
        """.'`| '.`__.'          """,
        """   \\     |_           """,
        """    '-__ / `-         """
    ],
    "blink": [
        """    ."``````'.        """,
        """   /          \\       """,
        """  /   ________/       """,
        """  | .' ==  ==|        """,
        """  \\(\\=(__)^(_)        """,
        """   |\\      | |        """,
        """   | \\     _)|        """,
        """   |\\ \\  ━_━/         """,
        """.'`| '.`__.'          """,
        """   \\     |_           """,
        """    '-__ / `-         """
    ]
}

right_lines = [
    ("prompt", "C:\\Users\\Mauro> ", "whoami"),
    ("sep", "----------------------------------------------------", ""),
    ("prop", "Degree", "     : B.S. in Intelligent Computing Engineering"),
    ("prop", "University", " : Autonomous University of Aguascalientes"),
    ("prop", "Stack", "      : Python, Rust, TypeScript, PHP, MySQL"),
    ("prop", "CoreSkills", " : Backend, Systems, Fullstack & DB"),
    ("sep", "----------------------------------------------------", ""),
    ("prop", "Repos", "      : 5"),
    ("prop", "Commits", "    : 149"),
    ("prop", "Stars", "      : 6"),
    ("prop", "TotalLOC", "   : 1,457,475")
]

width = 800
height = 330

def get_font(size, is_ui=False, is_ascii=False):
    if is_ui:
        candidates = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
        ]
        for p in candidates:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass

    if is_ascii:
        candidates = [
            "C:/Windows/Fonts/consola.ttf",
            "C:/Windows/Fonts/lucon.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "consola.ttf"
        ]
        for p in candidates:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass

    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cascadiacode.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "consola.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default()
    except Exception:
        return None

# Consolas 15pt en pantalla = 20px
font_ascii = get_font(20, is_ascii=True)
font_right = get_font(14)
font_ui = get_font(12, is_ui=True)

def create_frame_img(face_lines):
    img = Image.new("RGB", (width, height), color="#0c0c0c")
    draw = ImageDraw.Draw(img)

    # Ventana Command Prompt
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=8, outline="#2d2d2d", width=2)

    # Barra de Título Windows CMD
    draw.rectangle((0, 0, width - 1, 32), fill="#181818")
    draw.line((0, 32, width - 1, 32), fill="#2d2d2d", width=1)

    # Título de Ventana (sin icono, alineado a la izquierda)
    draw.text((16, 8), "Command Prompt", font=font_ui, fill="#cccccc")

    # Botones Windows (Minimizar, Maximizar, Cerrar) en la esquina superior derecha
    btn_col = "#999999"
    draw.line((710, 16, 720, 16), fill=btn_col, width=1)
    draw.rectangle((736, 11, 746, 21), outline=btn_col, width=1)
    draw.line((764, 11, 774, 21), fill=btn_col, width=1)
    draw.line((774, 11, 764, 21), fill=btn_col, width=1)

    # ASCII portrait (lado izquierdo - 11 líneas proporcionales a Bloc de Notas)
    start_y = 50
    line_step = 23
    for i, line in enumerate(face_lines):
        draw.text((28, start_y + i * line_step), line, font=font_ascii, fill="#cccccc")

    # CMD Output (lado derecho - 11 líneas simétricas)
    rx = 270
    start_y_right = 53
    for i, item in enumerate(right_lines):
        y = start_y_right + i * line_step
        kind = item[0]
        if kind == "prompt":
            draw.text((rx, y), item[1], font=font_right, fill="#cccccc")
            bbox = font_right.getbbox(item[1])
            kw = bbox[2] - bbox[0]
            draw.text((rx + kw, y), item[2], font=font_right, fill="#ffffff")
        elif kind == "sep":
            draw.text((rx, y), item[1], font=font_right, fill="#444444")
        elif kind == "prop":
            prop_name = item[1]
            val = item[2]
            draw.text((rx, y), prop_name, font=font_right, fill="#4fa6d8")
            bbox = font_right.getbbox(prop_name)
            kw = bbox[2] - bbox[0]
            draw.text((rx + kw, y), val, font=font_right, fill="#cccccc")

    return img

def main():
    timeline = [
        ("center", 2800),
        ("left", 1500),
        ("center", 2000),
        ("blink", 200),
        ("center", 300),
        ("blink", 180),
        ("center", 1400),
    ]

    imgs = []
    durations = []
    for state, dur in timeline:
        imgs.append(create_frame_img(raw_ascii_frames[state]))
        durations.append(dur)

    target_dir = r"c:\Users\Lomeli\Downloads\pagit"
    out_gif = os.path.join(target_dir, "profile_animated.gif")
    imgs[0].save(
        out_gif,
        save_all=True,
        append_images=imgs[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print("Guardado GIF animado con Consolas 15pt y nuevo ASCII en:", out_gif)

if __name__ == "__main__":
    main()
