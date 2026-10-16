#!/bin/zsh
# Generate one hand-drawn poster via agy (Gemini image-generator), copy newest jpg to data/img/<id>.jpg
# 用 agy 請 Gemini 畫一張海報，再從 brain 目錄把最新的 jpg 複製到 data/img/<id>.jpg
set -u
id="$1"; prompt="$2"
root="/Users/lujiajun/ai-projects/年末旅遊"
mkdir -p "$root/data/img"
work="/private/tmp/claude-501/-Users-lujiajun-ai-projects/4d324a30-1bea-46e8-8d6c-4ad5e1dbb684/scratchpad/agyimg-$id"
mkdir -p "$work"; cd "$work"
touch "$work/.start"
agy --new-project --model "Gemini 3.8 Flash (Medium)" --print-timeout 12m -p "$prompt" > "$work/log.txt" 2>&1
# 第一次常在 timeout 前沒做完，續一次等它完成
grep -q "NO_IMAGE_TOOL" "$work/log.txt" && { echo "NO_IMAGE_TOOL $id"; exit 2; }
agy -c --print-timeout 12m -p "圖片生成完成了嗎？完成就回報圖片檔完整路徑；沒完成就等它完成再回報。" >> "$work/log.txt" 2>&1
f=$(find "$HOME/.gemini/antigravity-cli/brain" -type f \( -name '*.jpg' -o -name '*.png' \) -newer "$work/.start" 2>/dev/null | xargs -I{} stat -f '%m %N' {} 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
if [ -n "$f" ]; then cp "$f" "$root/data/img/$id.jpg" && echo "OK $id <- $f"; else echo "NOFILE $id"; tail -5 "$work/log.txt"; exit 1; fi
