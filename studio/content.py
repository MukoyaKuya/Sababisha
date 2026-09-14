SERVICES = [
    {"key": "web", "number": "01", "name": "Web development", "short": "Web", "line": "Built to do more.", "description": "Distinctive websites and web applications. Thoughtful interfaces, solid foundations, and experiences that turn visitors into customers.", "tags": "Websites / E-commerce / Web apps"},
    {"key": "design", "number": "02", "name": "Graphic design", "short": "Design", "line": "Impossible to ignore.", "description": "Visual identities and design systems that give your ideas a voice. From your first logo to your next big campaign.", "tags": "Brand identity / Digital / Print"},
    {"key": "community", "number": "03", "name": "Community platforms", "short": "Platforms", "line": "Bring your people together.", "description": "Purpose-built digital homes for communities. We curate and build spaces where people connect, share knowledge, and belong.", "tags": "Memberships / Directories / Resource hubs"},
    {"key": "tools", "number": "04", "name": "Internal tools", "short": "Tools", "line": "Less friction. More flow.", "description": "Custom tools for the people doing the work. Replace scattered spreadsheets and repetitive tasks with systems built around your department.", "tags": "Dashboards / Workflows / Automation"},
    {"key": "film", "number": "05", "name": "Videography", "short": "Film", "line": "Make them feel something.", "description": "Stories told through movement, sound, and a fresh perspective. Films that capture the people and purpose behind your brand.", "tags": "Brand films / Events / Social content"},
    {"key": "photo", "number": "06", "name": "Photography", "short": "Photo", "line": "A different point of view.", "description": "Honest portraits, striking products, and moments worth remembering. Photography with intention, made to tell your story.", "tags": "Portraits / Products / Events"},
]
SERVICE_CHOICES = [(service["key"], service["name"]) for service in SERVICES]


THEME_PALETTES = {
    "embers": {
        "name": "Embers & Ink",
        "primary": "#ef642d",
        "ink": "#1c1c1c",
        "surface": "#faf3e7",
        "accent": "#ebbf58",
        "arrow": "#ef642d",
    },
    "coastline": {
        "name": "Coastline",
        "primary": "#e66f55",
        "ink": "#142c33",
        "surface": "#f6f0e6",
        "accent": "#6ab6b2",
        "arrow": "#e66f55",
    },
    "acacia": {
        "name": "Acacia & Clay",
        "primary": "#bf5d3c",
        "ink": "#19352b",
        "surface": "#f6f1e6",
        "accent": "#9ab070",
        "arrow": "#bf5d3c",
    },
    "indigo": {
        "name": "Indigo & Brass",
        "primary": "#6d5bd0",
        "ink": "#201d2d",
        "surface": "#f7f4ec",
        "accent": "#d0b461",
        "arrow": "#6d5bd0",
    },
    "noir": {
        "name": "Noir & Gold",
        "primary": "#d89a3d",
        "ink": "#101315",
        "surface": "#f3eee5",
        "accent": "#e2c16d",
        "arrow": "#d89a3d",
    },
    "kenya": {
        "name": "Kenya (Bendera)",
        "primary": "#bb2328",
        "ink": "#111413",
        "surface": "#f7f7f4",
        "accent": "#0a7037",
        "arrow": "#ffffff",
    },
}
THEME_PALETTE_CHOICES = [(key, palette["name"]) for key, palette in THEME_PALETTES.items()]


DECORATIVE_BORDER_CHOICES = [
    ("classic", "Classic curved cutouts"),
    ("square", "Clean square frame"),
    ("rounded", "Soft rounded frame"),
    ("deep-arch", "Deep arch cutouts"),
    ("stepped", "Stepped corner cutouts"),
    ("double", "Double-line frame"),
    ("brackets", "Corner brackets"),
    ("scalloped", "Scalloped cutouts"),
    ("diamond", "Diamond cutouts"),
    ("deco", "Art Deco corners"),
    ("stitched", "Stitched frame"),
    ("triple", "Triple-line frame"),
    ("oval", "Grand oval frame"),
    ("offset", "Offset line frame"),
    ("floral", "Floral corner frame"),
]
