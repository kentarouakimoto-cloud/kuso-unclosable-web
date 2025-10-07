# kuso_unclosable_streamlit.py
import streamlit as st
from streamlit.components.v1 import html

# ------------------ カスタマイズ（ここをいじる） ------------------
ACCENT = "#4da6ff"   # ← ここを好きな色コードに変える（例: "#ff6b6b"）
BG_COLOR = "#0f1724"
TEXT_COLOR = "#010110"
TITLE = "🔒 終了できないページ（Web版）"
HEIGHT = 420
# -----------------------------------------------------------------

st.set_page_config(page_title="クソおみくじ系 - 終了できないページ", layout="centered")
st.markdown(f"<h2 style='color:{TEXT_COLOR}; font-family: Helvetica; text-align:center'>{TITLE}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#9aa0b4; text-align:center'>画面内の「終了」ボタンが逃げ回ります。笑って動画を撮ってね。</p>", unsafe_allow_html=True)

# HTML+CSS+JS を埋め込む
embedded = f"""
<div id="stage" style="position:relative; width:100%; height:{HEIGHT}px; background:{BG_COLOR}; border-radius:10px; display:flex; align-items:center; justify-content:center;">
  <div id="arena" style="position:relative; width:560px; height:320px; background: #11121a; border-radius:8px; box-shadow: 0 6px 18px rgba(0,0,0,0.6);">
    <p id="msg" style="color:{TEXT_COLOR}; text-align:center; margin:12px 20px 0 20px; font-family:Helvetica">ボタンを押してみなさい（押せない）</p>
    <button id="escapeBtn" style="
        position:absolute;
        left:50%;
        top:60%;
        transform:translate(-50%,-50%);
        padding:12px 20px;
        font-weight:700;
        border:none;
        border-radius:8px;
        background: {ACCENT};
        color: #fff;
        cursor: pointer;
        transition: transform 0.06s linear;
    ">終了</button>
  </div>
</div>

<script>
const arena = document.getElementById("arena");
const btn = document.getElementById("escapeBtn");
const msg = document.getElementById("msg");

let escapeCount = 0;
let speedIncreaseEvery = 4;

// Utility: get random position within arena (button will be fully visible)
function randomPos() {{
  const bw = btn.offsetWidth;
  const bh = btn.offsetHeight;
  const aw = arena.clientWidth;
  const ah = arena.clientHeight;
  const margin = 8;
  const maxX = Math.max(margin, aw - bw - margin);
  const maxY = Math.max(margin, ah - bh - margin);
  const x = Math.floor(Math.random() * maxX) + margin;
  const y = Math.floor(Math.random() * maxY) + margin;
  return {{x, y}};
}}

// Move with little animation
function moveTo(x, y) {{
  btn.style.left = x + "px";
  btn.style.top = y + "px";
  btn.style.transform = "translate(0,0)";
}}

// Initial small delay to ensure layout
setTimeout(() => {{
  const p = randomPos();
  moveTo(p.x, p.y);
}}, 80);

function updateMessage(clicked=false) {{
  const taunts = [
    "ふっ…まだ早いぞ。",
    "閉じようとする度に逃げるボタン。",
    "押してみな。押してみな？",
    "諦めたらそこで試合終了だよ（無限）",
    "逃げるのが得意なんだ。"
  ];
  let idx = Math.min(taunts.length - 1, Math.floor(escapeCount / 2));
  let text = taunts[idx];
  if (clicked) {{
    const cl = ["へっ、痛くないよ？", "押した？押した？え、押したの？"];
    text = cl[Math.floor(Math.random() * cl.length)];
  }}
  if (escapeCount > 12) text = "いい勝負だ…だが私は逃げる。";
  msg.innerText = text;
}}

// When mouse enters, move away
btn.addEventListener("mouseenter", () => {{
  escapeCount += 1;
  updateMessage();
  const p = randomPos();
  moveTo(p.x, p.y);
}});

// When clicked, also jitter
btn.addEventListener("click", (e) => {{
  e.preventDefault();
  escapeCount += 1;
  updateMessage(true);
  // do two jumps
  for (let i = 0; i < 2; i++) {{
    setTimeout(() => {{
      const p = randomPos();
      moveTo(p.x, p.y);
    }}, 50 + i * 80);
  }}
}});

// Optional: Esc x5 to reveal "escape" overlay
let escCount = 0;
document.addEventListener("keydown", (e) => {{
  if (e.key === "Escape") {{
    escCount += 1;
    msg.innerText = `セーフキー検知…残り ${{5 - escCount}} 回で脱出可能`;
    if (escCount >= 5) {{
      msg.innerText = "セーフキー連打確認。脱出します…。";
      // show an overlay link to close (cannot close browser tab programmatically reliably)
      const overlay = document.createElement("div");
      overlay.style.position = "absolute";
      overlay.style.left = 0;
      overlay.style.top = 0;
      overlay.style.width = "100%";
      overlay.style.height = "100%";
      overlay.style.display = "flex";
      overlay.style.alignItems = "center";
      overlay.style.justifyContent = "center";
      overlay.style.background = "rgba(0,0,0,0.7)";
      overlay.innerHTML = `<div style="text-align:center;color:#fff;font-family:Helvetica;">
                            <h2>脱出成功！</h2>
                            <p>このページは自由に閉じてください。</p>
                           </div>`;
      arena.appendChild(overlay);
    }}
  }}
}});
</script>
"""

html(embedded, height=HEIGHT + 40)
