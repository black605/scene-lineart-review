# annotate.py  用法：python annotate.py spec.json
# spec 示例：
# {"base":"03_1280.png","out":"03-审核标注.png","title":"03 主广场 · r1","verdict":"返工",
#  "fixed":[[0,0,1280,72,"顶栏 72px"],[320,696,960,776,"Dock"]],
#  "labels":[[330,52,490,84,"图书馆"]], "hot":[[160,100,550,320]],
#  "cards":[[210,460,410,650,"任务卡1"]], "ip":[[90,470,196,640,"向导角色"]],
#  "issues":[["fix",[150,36,850,104],"图书馆、工坊屋顶太高，标签撞顶栏 → 两栋下移到最高点 y≥124"],
#            ["note",[1030,300,1120,345],"剧场标签贴邻楼 → UI 阶段右移 30px"]]}
import json, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

def cjk_font(size):
    # 优先简体中文字体；macOS 常见 PingFang / Hiragino，Linux 常见 Noto CJK
    files = subprocess.run(['fc-list', ':lang=zh', 'file'], capture_output=True, text=True).stdout.split()
    files = [x.rstrip(':') for x in files] + ['/System/Library/Fonts/PingFang.ttc', '/System/Library/Fonts/Hiragino Sans GB.ttc']
    files.sort(key=lambda x: (('SC' not in x and 'PingFang' not in x), 'Bold' not in x))
    for path in files:
        try: return ImageFont.truetype(path, size)
        except Exception: continue
    return ImageFont.load_default()

S = json.load(open(sys.argv[1]))
base = Image.open(S['base']).convert('RGBA'); W, H = base.size
ov = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); f = cjk_font(15)
def box(b, fill, line, txt=None, r=12, w=2):
    d.rounded_rectangle(b[:4], r, fill=fill, outline=line, width=w)
    if txt: d.text((b[0] + 8, (b[1] + b[3]) / 2 - 10), txt, font=f, fill=(30, 30, 30, 255))
for b in S.get('fixed', []):  box(b, (40, 110, 220, 70), (40, 110, 220, 255), b[4] if len(b) > 4 else None)
for b in S.get('labels', []): box(b, (245, 150, 40, 110), (220, 120, 20, 255), b[4] if len(b) > 4 else None)
for b in S.get('cards', []):  box(b, (40, 170, 90, 70), (30, 140, 70, 255), b[4] if len(b) > 4 else None)
for b in S.get('ip', []):     box(b, (150, 80, 210, 80), (130, 60, 190, 255), b[4] if len(b) > 4 else None)
for b in S.get('hot', []):    d.rectangle(b[:4], outline=(245, 150, 40, 200), width=2)
for i, (sev, b, _) in enumerate(S.get('issues', [])):
    col = (225, 40, 40, 255) if sev == 'fix' else (235, 160, 0, 255)
    for k in range(3): d.rectangle((b[0] + k, b[1] + k, b[2] - k, b[3] - k), outline=col)
    d.ellipse((b[0] + 6, b[1] + 6, b[0] + 34, b[1] + 34), fill=col)
    d.text((b[0] + 14, b[1] + 8), str(i + 1), font=cjk_font(17), fill=(255, 255, 255, 255))
img = Image.alpha_composite(base, ov).convert('RGB')
lines = S.get('issues', [])
cap = Image.new('RGB', (W, 64 + 30 * len(lines)), (250, 247, 242)); dc = ImageDraw.Draw(cap)
dc.text((20, 12), f"{S.get('title', '')}  【{S.get('verdict', '')}】", font=cjk_font(24), fill=(30, 26, 22))
for i, (sev, _, t) in enumerate(lines):
    dc.text((20, 56 + 30 * i), f"{i + 1}. {'【需返工】' if sev == 'fix' else '【后续处理】'}{t}", font=cjk_font(17),
            fill=(200, 40, 40) if sev == 'fix' else (150, 100, 0))
out = Image.new('RGB', (W, H + cap.height), 'white'); out.paste(img, (0, 0)); out.paste(cap, (0, H)); out.save(S['out'])
print('saved', S['out'])
