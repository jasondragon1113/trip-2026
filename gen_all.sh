#!/bin/zsh
# Regenerate posters for given ids (or all) with the mascot description in posters.json
# 依 posters.json 重生海報；參數給 id 清單，不給就全部
cd "/Users/lujiajun/ai-projects/年末旅遊"
ids=("$@"); [ ${#ids[@]} -eq 0 ] && ids=($(python3 -c "import json;print(' '.join(json.load(open('posters.json'))['posters']))"))
for id in $ids; do
  prompt=$(python3 -c "import json,sys;j=json.load(open('posters.json'));i=sys.argv[1];print('請用你的圖片生成工具畫一張 1200x675 橫式的手繪旅遊攻略海報，存成本目錄 '+i+'.jpg。'+j['style']+j['chars']+j['posters'][i])" "$id")
  ./gen_image.sh "$id" "$prompt"
done
