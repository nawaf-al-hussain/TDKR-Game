WT = '/tmp/my-project/work/ghpages_staged_wt/playable'
H = f'{WT}/integration_lazy.html'
old = """    for (let f = 0; f < 30; f++) {
      mercMixer.update(1 / 60);"""
new = """    for (let f = 0; f < 30; f++) {
      mercMixer.update(1 / 60);
      merc.updateMatrixWorld(true);   // no render here: refresh bone world matrices for the probe"""
src = open(H, encoding='utf-8').read()
assert src.count(old) == 1, src.count(old)
open(H, 'wb').write(src.replace(old, new).encode('utf-8'))
print('patched control matrixWorld')
