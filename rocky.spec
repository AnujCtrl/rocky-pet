block_cipher = None

a = Analysis(
    ['src/rocky_pet/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'rocky_pet', 'rocky_pet.app', 'rocky_pet.audio',
        'rocky_pet.bubble_widget', 'rocky_pet.content',
        'rocky_pet.engine', 'rocky_pet.panel_widget',
        'rocky_pet.rocky_widget', 'rocky_pet.settings',
        'rocky_pet.sprites', 'rocky_pet.tray',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='RockyPet',
    debug=False,
    strip=False,
    upx=True,
    console=False,
)
