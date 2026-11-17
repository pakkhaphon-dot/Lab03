# ENG29 2121 · Lab 03 — BJT DC Bias Web App

เว็บ Flask ที่เลือกได้ 3 วงจรไบอัส: Voltage Divider (ผลเดิมจาก Lab 2),
Fixed Bias และ Emitter Bias แบบแหล่งจ่ายเดียว

## วิธีรัน

```powershell
python -m pip install -r requirements.txt
python -m flask --app app run
```

แล้วเปิด http://127.0.0.1:5000/

ถ้า Flask แสดงพอร์ตอื่น (เช่น 5001) ให้ใช้ URL นั้นแทน

## หน่วยบนฟอร์ม

| ช่อง | หน่วย |
|---|---|
| VCC, VBE | V |
| RC, R1, R2, RE | kΩ |
| RB | MΩ |
| β | ไม่มีหน่วย |

ผลลัพธ์: IC เป็น mA, VB/VE/VC/VCE เป็น V

## ตรวจผ่าน Browser ด้วย Playwright MCP

ต้องมี Node.js 18 ขึ้นไปและ Google Chrome ไฟล์ `opencode.json` ตั้งค่า Playwright MCP
ไว้แล้ว (OpenCode V2 ใช้ `mcp.servers`) OpenCode โหลด config อัตโนมัติ ใช้ `/reload`
หากจำเป็น แล้วตรวจว่า `playwright` แสดงสถานะเชื่อมต่อ (`/mcps` ใน V2 หรือ `opencode mcp list`)

Flask ต้องรันค้างไว้ก่อน แล้วให้เอเจนต์เปิด `http://127.0.0.1:5000/` ผ่าน MCP
อ่าน snapshot กรอกฟอร์มและกดคำนวณจริง ใช้ตาราง A1–A5 ในใบงานเป็นค่าคาดหมาย
ไม่ต้องลง Playwright ใน `requirements.txt`

## โครงไฟล์

- `app.py` — Flask route, ตรวจอินพุตและเลือกฟังก์ชันตามโหมด
- `dc_bias.py` — สมการทั้ง 3 วงจร ส่งผลเป็น dict
- `templates/index.html` — ฟอร์มและผลลัพธ์
- `opencode.json` — ตั้งค่า Playwright MCP
- `docs/validation.md` — ตารางผล A1–A5

## ส่งงาน

- GitHub: https://github.com/pakkhaphon-dot/Lab03
- Commit SHA: `e09adcc7f25998f3491268a878192fcba23927d7`

## ส่วนที่ AI ช่วย

AI เขียน `app.py`, `dc_bias.py`, `templates/index.html`, `opencode.json` และแม่แบบ
`docs/validation.md` ตามสมการในใบงาน นักศึกษาตรวจสมการ หน่วย ชื่อคีย์ `dict`
การเลือกฟังก์ชัน อินพุตผิด และผล A1–A5 จากหน้าเว็บจริง รวมถึงคำนวณค่าอ้างอิงอิสระเอง
