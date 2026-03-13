import os
import smtplib
from email.message import EmailMessage
# from email.policy import SMTPUTF8

from app.models.product import Product, ProductTranslation, ProductImage

OWNER_EMAIL = "qsa8647332@gmail.com"

def _position_label(pos):
    if not pos:
        return ""
    return f"第{pos}順位"


def _format_price(value):
    """Return integer string if whole number, else float string."""
    return str(int(value)) if value == int(value) else str(value)


def send_order_confirmation(user, order_out, db):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASSWORD", "")

    if not smtp_user or not smtp_pass:
        print("Email skipped: SMTP_USER / SMTP_PASSWORD not configured")
        return

    # ── Build items data ──────────────────────────────────────────────────────
    items_data = []
    total_price = 0.0
    total_original = 0.0

    for item in order_out.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        translation = db.query(ProductTranslation).filter(
            ProductTranslation.product_id == item.product_id,
            ProductTranslation.locale == "zh-TW",
        ).first()

        image = (
            db.query(ProductImage)
            .filter(ProductImage.product_id == item.product_id)
            .order_by(ProductImage.sort_order)
            .first()
        )

        name = (
            translation.name
            if translation
            else (product.code if product else str(item.product_id))
        )
        img_url = image.url if image else ""
        price = float(item.price)
        original_price = (
            float(product.original_price)
            if product and product.original_price
            else None
        )
        pickup_time = product.pickup_available_time if product else None
        pickup_str = (
            pickup_time.strftime("%Y/%m/%d") if pickup_time else "隨時"
        )

        total_price += price
        total_original += original_price if original_price is not None else price

        items_data.append(
            {
                "name": name,
                "img_url": img_url,
                "price": price,
                "original_price": original_price,
                "pickup_str": pickup_str,
                "waiting_position": item.waiting_position,
            }
        )

    # ── Order number (matches frontend logic) ─────────────────────────────────
    short_id = str(order_out.id)[-6:]
    count = str(len(items_data)).zfill(2)
    order_number = f"{short_id}{_format_price(total_price)}{count}"

    # ── Pickup date ───────────────────────────────────────────────────────────
    pickup_display = (
        order_out.pickup_time.strftime("%Y/%m/%d")
        if order_out.pickup_time
        else ""
    )

    # ── Salutation ────────────────────────────────────────────────────────────
    salutation_map = {"Mr": "先生", "Ms": "小姐", "Mrs": "小姐"}
    salutation = salutation_map.get(user.salutation, user.salutation)

    html = _build_html(
        user=user,
        salutation=salutation,
        pickup_display=pickup_display,
        items_data=items_data,
        order_number=order_number,
        total_price=total_price,
        total_original=total_original,
    )

    subject = f"預訂成功！訂單編號 {order_number} - HomeFinds"
    recipients = list({user.email, OWNER_EMAIL})  # deduplicate

    # 清除任何意外夾帶的不換行空格，避免 ASCII 編碼錯誤
    # html = html.replace('\xa0', ' ')

    # msg = EmailMessage(policy=SMTPUTF8)
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)
    msg.set_content(html, subtype="html", charset="utf-8")

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"Order confirmation email sent to {recipients}")
    except Exception as e:
        print(f"Email sending failed: {e}")


def _build_html(user, salutation, pickup_display, items_data, order_number,
                total_price, total_original):
    # ── Items rows ────────────────────────────────────────────────────────────
    item_rows = ""
    for i, item in enumerate(items_data, 1):
        original_td = (
            f'<span style="text-decoration:line-through;color:#aaa;margin-right:4px;">'
            f'${_format_price(item["original_price"])}</span>'
            if item["original_price"] is not None else ""
        )
        pos = item["waiting_position"]
        pos_color = "#2e7d32" if pos == 1 else "#c0392b"
        pos_label = _position_label(pos)

        thumb_cell = (
            f'<img src="{item["img_url"]}" width="40" height="40" '
            f'style="border-radius:4px;object-fit:cover;display:block;" />'
            if item["img_url"]
            else '<div style="width:40px;height:40px;background:#eee;border-radius:4px;"></div>'
        )

        item_rows += f"""
        <tr>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;color:#999;font-size:13px;text-align:center;">{i}</td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;">{thumb_cell}</td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;font-size:13px;">{item["name"]}</td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;font-size:13px;color:#666;">{item["pickup_str"]}</td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;font-size:13px;font-weight:600;text-align:right;white-space:nowrap;">
            {original_td}${_format_price(item["price"])}
          </td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;font-size:13px;font-weight:700;color:{pos_color};text-align:center;white-space:nowrap;">
            {pos_label}
          </td>
        </tr>"""

    # ── Total row ─────────────────────────────────────────────────────────────
    total_original_html = (
        f'<span style="text-decoration:line-through;color:#aaa;margin-right:6px;">'
        f'${_format_price(total_original)}</span>'
        if total_original > total_price else ""
    )

    # ── Pickup info line ──────────────────────────────────────────────────────
    pickup_line = (
        f'<p style="color:#666;font-size:13px;margin:4px 0 8px;">期待於 {pickup_display} 與您見面領取物品。'
        f'<em>（領取時間可至「<a href="https://schristy2020.github.io/homefinds/#/orders" style="color:#c9a96e;text-decoration:underline;">我的訂單</a>」進行變更）</em></p>'
        if pickup_display
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>預訂成功！</title>
</head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Noto Sans TC',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:32px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08);max-width:600px;">

          <!-- Header -->
          <tr>
            <td align="center" style="padding:32px 24px 16px;border-bottom:1px solid #f0ebe3;">
              <div style="font-size:36px;margin-bottom:8px;">🎁</div>
              <h1 style="margin:0;font-size:22px;font-weight:700;color:#1a1a1a;"><a href="https://schristy2020.github.io/homefinds/" style="color:#c9a96e;text-decoration:underline;">Christy's HomeFinds</a> 預訂成功!</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:24px 28px;">

              <!-- Greeting -->
              <p style="font-size:15px;font-weight:700;margin:0 0 4px;">
                Hi {user.last_name} {salutation}, 感謝您的預訂！
              </p>
              {pickup_line}
              <ul style="margin:0 0 16px;padding-left:20px;font-size:13px;list-style:disc;">
                <li style="margin-bottom:3px;">Email: <strong>{user.email}</strong></li>
                <li style="margin-bottom:3px;">Phone: <strong>{user.phone}</strong></li>
              </ul>

              <!-- Payment Notice -->
              <div style="background:#fffbf0;border:1.5px solid #f0d080;border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:13px;">
                <p style="font-weight:700;margin:0 0 8px;font-size:13px;">
                  ⚠️ 付款重要須知：本場採用「先付款先得」制！
                </p>
                <ul style="margin:0;padding-left:18px;">
                  <li style="margin-bottom:5px;line-height:1.5;">即時認購：不論目前排序，<strong>先完成匯款者直接獲得該物品</strong>。</li>
                  <li style="margin-bottom:5px;line-height:1.5;">成交確認：Christy 確認款項後會發通知，商品也<strong>將立即轉為「已售出」</strong>！</li>
                  <li style="line-height:1.5;">退款保證：若確認後發現商品已由他人搶先買走，Christy 將主動聯繫並透過 Zelle 退款。</li>
                </ul>
              </div>

              <!-- Zelle Info -->
              <div style="margin-bottom:16px;font-size:13px;">
                <p style="font-weight:700;margin:0 0 6px;">💰 Zelle 匯款資訊：</p>
                <ul style="margin:0;padding-left:20px;list-style:disc;">
                  <li style="margin-bottom:3px;">帳號: (984)373-9392</li>
                  <li style="margin-bottom:3px;">戶名: SHU CHING LI</li>
                  <li>備註: 請務必註明您的「訂單編號」</li>
                </ul>
              </div>

              <!-- Order Number -->
              <p style="font-size:14px;font-weight:700;margin:0 0 16px;">
                訂單編號：
                <span style="font-family:monospace;background:#f4f4f4;border-radius:4px;padding:3px 10px;letter-spacing:0.05em;margin-left:4px;">
                  {order_number}
                </span>
              </p>

              <!-- Items Table -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="border-collapse:collapse;margin-bottom:12px;font-size:13px;">
                <thead>
                  <tr style="border-bottom:1.5px solid #e0e0e0;">
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:center;width:24px;"></th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;width:50px;">縮圖</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;">物品名稱</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;">可取貨時間</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:right;">價錢</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:center;">目前順位</th>
                  </tr>
                </thead>
                <tbody>{item_rows}
                </tbody>
              </table>

              <!-- Total -->
              <div style="display:flex;justify-content:space-between;padding:8px 0 4px;font-size:15px;font-weight:600;border-top:1px solid #eee;">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="font-size:14px;font-weight:600;">共 {len(items_data)} 樣物品，總計：</td>
                    <td style="text-align:right;font-size:15px;font-weight:700;">
                      {total_original_html}${_format_price(total_price)}
                    </td>
                  </tr>
                </table>
              </div>

              <!-- Divider -->
              <hr style="border:none;border-top:1px solid #e8e8e8;margin:20px 0;" />

              <!-- Guide Section -->
              <h3 style="font-size:14px;font-weight:700;color:#1a1a1a;margin:0 0 14px;">🛍️ 購物與取貨流程說明</h3>

              <!-- Step 1 -->
              <div style="margin-bottom:14px;font-size:13px;">
                <p style="font-size:13px;font-weight:700;color:#c9a96e;margin:0 0 6px;">Step 1. 預定（保留順位）</p>
                <ol style="margin:0;padding-left:18px;">
                  <li style="font-size:12px;color:#444;line-height:1.5;">預定成功：完成後系統會將您排入「預定排序名單」，名單皆以匿名呈現。</li>
                  <li style="font-size:12px;color:#444;line-height:1.5;">狀態確認：可至商品頁面或「我的訂單」查看預定紀錄，系統也會自動寄信給您。</li>
                  <li style="font-size:12px;color:#c0392b;font-weight:600;list-style:none;margin-left:-18px;">⚠️ 重要提醒：「預定成功」不代表「購買成功」！</li>
                </ol>
              </div>

              <!-- Step 2 -->
              <div style="margin-bottom:14px;font-size:13px;">
                <p style="font-size:13px;font-weight:700;color:#c9a96e;margin:0 0 6px;">Step 2. 付款（確認獲得）</p>
                <p style="font-size:12px;color:#555;margin:0 0 6px;">為了確保交易效率，採取以下原則：</p>
                <ol style="margin:0;padding-left:18px;">
                  <li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">優先獲得權：物品由「先行完成付款者」獲得。</li>
                  <li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">遞補規則：若無人先行付款，則由「預定排序名單」之第一順位獲得。</li>
                  <li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">
                    付款方式：請依訂單總金額透過 Zelle 匯款：
                    <div style="margin-top:4px;padding:6px 10px;font-weight:600;color:#1a1a1a;">
                      <div>a. 帳號: (984)373-9392</div>
                      <div>b. 戶名: SHU CHING LI</div>
                      <div>c. 備註: 訂單編號</div>
                    </div>
                  </li>
                  <li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">確認交易：Christy 確認收到款項後會寄信通知，並將商品改為「已售出」。</li>
                  <li style="font-size:12px;color:#444;line-height:1.5;">例外：第一順位者亦可選擇於「取貨時付款」。</li>
                </ol>
              </div>

              <!-- Step 3 -->
              <div style="margin-bottom:14px;font-size:13px;">
                <p style="font-size:13px;font-weight:700;color:#c9a96e;margin:0 0 6px;">Step 3. 取貨</p>
                <ul style="margin:0;padding-left:18px;">
                  <li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">取貨時間：請依「預計取貨時間」準時到現場。</li>
                  <li style="font-size:12px;color:#444;line-height:1.5;">修改資料：後續若需更改取貨時間，可至「我的訂單」進行編輯。</li>
                </ul>
              </div>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:16px 28px 28px;border-top:1px solid #f0f0f0;font-size:12px;color:#888;text-align:center;">
              💡 有任何問題？歡迎聯絡 Christy:
              <a href="mailto:qsa8647332@gmail.com" style="color:#c9a96e;text-decoration:none;">qsa8647332@gmail.com</a>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
