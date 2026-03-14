import os
import resend

from app.models.product import Product, ProductTranslation, ProductImage

OWNER_EMAIL = "qsa8647332@gmail.com"

# ── Email translations ────────────────────────────────────────────────────────
EMAIL_TRANSLATIONS = {
    "zh-TW": {
        "html_lang": "zh-TW",
        "subject": "預訂成功！訂單編號 {order_number} - Christy's HomeFinds",
        "header": "Christy's HomeFinds 預訂成功!",
        "greeting": "Hi {first_name} 感謝您的預訂!",
        "pickup_info": "期待於 {date} 與您見面領取物品。",
        "pickup_editable": "（領取時間可至「{link}」進行變更）",
        "my_orders_link_text": "我的訂單",
        "payment_title": "⚠️ 付款重要須知：本場採用「先付款先得」制！",
        "payment_notes": [
            "即時認購：不論目前排序，<strong>先完成匯款者直接獲得該物品</strong>。",
            "成交確認：Christy 確認款項後會發通知，商品也<strong>將立即轉為「已售出」</strong>！",
            "退款保證：若確認後發現商品已由他人搶先買走，Christy 將主動聯繫並透過 Zelle 退款。",
        ],
        "zelle_title": "💰 Zelle 匯款資訊：",
        "zelle_account": "帳號: (984)373-9392",
        "zelle_name": "戶名: SHU CHING LI",
        "zelle_note": "備註: 請務必註明您的「訂單編號」",
        "order_number_label": "訂單編號：",
        "col_thumb": "縮圖",
        "col_name": "物品名稱",
        "col_pickup": "可取貨時間",
        "col_price": "價錢",
        "col_position": "目前順位",
        "total": "共 {count} 樣物品，總計：",
        "guide_title": "🛍️ 購物與取貨流程說明",
        "step1_title": "Step 1. 預定（保留順位）",
        "step1_items": [
            "預定成功：完成後系統會將您排入「預定排序名單」，名單皆以匿名呈現。",
            "狀態確認：可至商品頁面或「我的訂單」查看預定紀錄，系統也會自動寄信給您。",
        ],
        "step1_warning": "⚠️ 重要提醒：「預定成功」不代表「購買成功」！",
        "step2_title": "Step 2. 付款（確認獲得）",
        "step2_intro": "為了確保交易效率，採取以下原則：",
        "step2_items": [
            "優先獲得權：物品由「先行完成付款者」獲得。",
            "遞補規則：若無人先行付款，則由「預定排序名單」之第一順位獲得。",
            "確認交易：Christy 確認收到款項後會寄信通知，並將商品改為「已售出」。",
            "例外：第一順位者亦可選擇於「取貨時付款」。",
        ],
        "step2_pay_label": "付款方式：請依訂單總金額透過 Zelle 匯款：",
        "step2_zelle_a": "a. 帳號: (984)373-9392",
        "step2_zelle_b": "b. 戶名: SHU CHING LI",
        "step2_zelle_c": "c. 備註: 訂單編號",
        "step3_title": "Step 3. 取貨",
        "step3_items": [
            "取貨時間：請依「預計取貨時間」準時到現場。",
            "修改資料：後續若需更改取貨時間，可至「我的訂單」進行編輯。",
        ],
        "step3_location_label": "取貨地點：",
        "step3_location_name": "Crowne at 501",
        "step3_location_address": "2031 Honeycutt Dr Suite 1100, Durham, NC 27707",
        "footer": "💡 有任何問題？歡迎聯絡 Christy:",
        "anytime": "隨時",
        "salutation_map": {"Mr": "先生", "Ms": "小姐", "Mrs": "小姐"},
        "position_labels": [
            "第一順位", "第二順位", "第三順位", "第四順位", "第五順位",
            "第六順位", "第七順位", "第八順位", "第九順位", "第十順位",
        ],
        "position_fallback": "第{n}順位",
    },
    "zh-CN": {
        "html_lang": "zh-CN",
        "subject": "预定成功！订单编号 {order_number} - Christy's HomeFinds",
        "header": "Christy's HomeFinds 预定成功!",
        "greeting": "Hi {first_name} 感谢您的预定！",
        "pickup_info": "期待于 {date} 与您见面领取物品。",
        "pickup_editable": "（领取时间可至\"{link}\"进行变更）",
        "my_orders_link_text": "我的订单",
        "payment_title": "⚠️ 付款重要须知：本场采用\"先付款先得\"制！",
        "payment_notes": [
            "即时认购：不论目前排序，<strong>先完成汇款者直接获得该物品</strong>。",
            "成交确认：Christy 确认款项后会发通知，商品也<strong>将立即转为\"已售出\"</strong>！",
            "退款保证：若确认后发现商品已由他人抢先买走，Christy 将主动联系并通过 Zelle 退款。",
        ],
        "zelle_title": "💰 Zelle 汇款信息：",
        "zelle_account": "帐号: (984)373-9392",
        "zelle_name": "户名: SHU CHING LI",
        "zelle_note": "备注: 请务必注明您的\"订单编号\"",
        "order_number_label": "订单编号：",
        "col_thumb": "缩图",
        "col_name": "物品名称",
        "col_pickup": "可取货时间",
        "col_price": "价格",
        "col_position": "目前顺位",
        "total": "共 {count} 件商品，合计：",
        "guide_title": "🛍️ 购物与取货流程说明",
        "step1_title": "Step 1. 预定（保留顺位）",
        "step1_items": [
            "预定成功：完成后系统会将您排入「预定排序名单」，名单皆以匿名呈现。",
            "状态确认：可至商品页面或「我的订单」查看预定记录，系统也会自动寄信给您。",
        ],
        "step1_warning": "⚠️ 重要提醒：「预定成功」不代表「购买成功」！",
        "step2_title": "Step 2. 付款（确认获得）",
        "step2_intro": "为了确保交易效率，采取以下原则：",
        "step2_items": [
            "优先获得权：物品由「先行完成付款者」获得。",
            "递补规则：若无人先行付款，则由「预定排序名单」之第一顺位获得。",
            "确认交易：Christy 确认收到款项后会寄信通知，并将商品改为「已售出」。",
            "例外：第一顺位者亦可选择于「取货时付款」。",
        ],
        "step2_pay_label": "付款方式：请依订单总金额透过 Zelle 汇款：",
        "step2_zelle_a": "a. 帐号: (984)373-9392",
        "step2_zelle_b": "b. 户名: SHU CHING LI",
        "step2_zelle_c": "c. 备注: 订单编号",
        "step3_title": "Step 3. 取货",
        "step3_items": [
            "取货时间：请依「预计取货时间」准时到现场。",
            "修改资料：后续若需更改取货时间，可至「我的订单」进行编辑。",
        ],
        "step3_location_label": "取货地点：",
        "step3_location_name": "Crowne at 501",
        "step3_location_address": "2031 Honeycutt Dr Suite 1100, Durham, NC 27707",
        "footer": "💡 有任何问题？欢迎联络 Christy:",
        "anytime": "随时",
        "salutation_map": {"Mr": "先生", "Ms": "小姐", "Mrs": "小姐"},
        "position_labels": [
            "第一顺位", "第二顺位", "第三顺位", "第四顺位", "第五顺位",
            "第六顺位", "第七顺位", "第八顺位", "第九顺位", "第十顺位",
        ],
        "position_fallback": "第{n}顺位",
    },
    "en": {
        "html_lang": "en",
        "subject": "Order Confirmed! Order #{order_number} - Christy's HomeFinds",
        "header": "Christy's HomeFinds Order Confirmed!",
        "greeting": "Hi {first_name}, thanks for your order!",
        "pickup_info": "We look forward to seeing you on {date} for pickup.",
        "pickup_editable": "(Pickup time can be updated in \"{link}\")",
        "my_orders_link_text": "My Orders",
        "payment_title": "⚠️ Payment Notice: We operate on a \"First-Come, First-Served\" basis!",
        "payment_notes": [
            "Instant Buy: Regardless of your current queue position, the first person to complete the payment gets the item.",
            "Confirmation: Once Christy confirms the payment, the item will be marked as <strong>\"Sold Out\"</strong> immediately!",
            "Money-Back Guarantee: If the item is purchased by someone else before your payment is confirmed, Christy will contact you for a full refund via Zelle.",
        ],
        "zelle_title": "💰 Zelle Payment Details:",
        "zelle_account": "Account: (984)373-9392",
        "zelle_name": "Name: SHU CHING LI",
        "zelle_note": "Note: Please include your \"Order ID\" in the memo.",
        "order_number_label": "Order ID:",
        "col_thumb": "Photo",
        "col_name": "Item",
        "col_pickup": "Pickup Time",
        "col_price": "Price",
        "col_position": "Current Rank",
        "total": "{count} item(s), Total:",
        "guide_title": "🛍️ Shopping & Pickup Guide",
        "step1_title": "Step 1. Pre-order (Reserve Your Spot)",
        "step1_items": [
            "Confirmation: Once reserved, you will be added to the \"Pre-order Waitlist\" (displayed anonymously).",
            "Check Status: View your records on the product page or under \"My Orders.\" An automated email will also be sent to you.",
        ],
        "step1_warning": "⚠️ IMPORTANT: A \"Pre-order\" does NOT guarantee the item is yours!",
        "step2_title": "Step 2. Payment (Secure Your Item)",
        "step2_intro": "To ensure a smooth process, we follow these rules:",
        "step2_items": [
            "First-Pay, First-Serve: The item goes to the person who completes the payment first.",
            "Waitlist Priority: If no one completes an early payment, the first person on the waitlist will get the item.",
            "Verification: Once Christy confirms the payment, you will receive an email and the item will be marked as \"Sold.\"",
            "Note for #1 Spot: If you are the first person on the waitlist, you may choose to \"Pay upon Pickup.\"",
        ],
        "step2_pay_label": "Payment Method: Please transfer the total amount via Zelle:",
        "step2_zelle_a": "a. Account: (984)373-9392",
        "step2_zelle_b": "b. Name: SHU CHING LI",
        "step2_zelle_c": "c. Memo: Order ID",
        "step3_title": "Step 3. Pickup",
        "step3_items": [
            "Schedule: Please arrive on time according to your \"Estimated Pickup Time.\"",
            "Edit Info: You can modify your pickup time later in the \"My Orders\" section.",
        ],
        "step3_location_label": "Pickup Location:",
        "step3_location_name": "Crowne at 501",
        "step3_location_address": "2031 Honeycutt Dr Suite 1100, Durham, NC 27707",
        "footer": "💡 Questions? Contact Christy:",
        "anytime": "Anytime",
        "salutation_map": {"Mr": "Mr.", "Ms": "Ms.", "Mrs": "Mrs."},
        "position_labels": [
            "1st Place", "2nd Place", "3rd Place", "4th Place", "5th Place",
            "6th Place", "7th Place", "8th Place", "9th Place", "10th Place",
        ],
        "position_fallback": "{n}th Place",
    },
}

# Map frontend locale codes to DB ProductTranslation locale codes
_LOCALE_TO_DB = {
    "zh-TW": "zh-TW",
    "zh-CN": "zh-CN",
    "en": "en",
}


def _position_label(pos, tr):
    if not pos:
        return ""
    labels = tr["position_labels"]
    if 1 <= pos <= len(labels):
        return labels[pos - 1]
    return tr["position_fallback"].replace("{n}", str(pos))


def _format_price(value):
    """Format price: integer if whole number, else 2 decimal places."""
    rounded = round(value, 2)
    return str(int(rounded)) if rounded == int(rounded) else f"{rounded:.2f}"


def _format_datetime_12h(dt):
    """Format datetime as MM/DD/YYYY H:MM AM/PM"""
    h = dt.hour
    ampm = "PM" if h >= 12 else "AM"
    h12 = h % 12 or 12
    return f"{dt.strftime('%m/%d/%Y')} {h12}:{dt.strftime('%M')} {ampm}"


def send_order_confirmation(user, order_out, db, locale="zh-TW"):
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM", "")

    if not resend_api_key or not from_email:
        print("Email skipped: RESEND_API_KEY / RESEND_FROM not configured")
        return

    tr = EMAIL_TRANSLATIONS.get(locale, EMAIL_TRANSLATIONS["zh-TW"])
    db_locale = _LOCALE_TO_DB.get(locale, "zh-TW")

    # ── Build items data ──────────────────────────────────────────────────────
    items_data = []
    total_price = 0.0
    total_original = 0.0

    for item in order_out.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        translation = db.query(ProductTranslation).filter(
            ProductTranslation.product_id == item.product_id,
            ProductTranslation.locale == db_locale,
        ).first()

        # Fallback to zh-TW if no translation found for the requested locale
        if not translation and db_locale != "zh-TW":
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
            _format_datetime_12h(pickup_time) if pickup_time else tr["anytime"]
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
    order_number = f"S{short_id}{int(total_price)}{count}"

    # ── Pickup date ───────────────────────────────────────────────────────────
    pickup_display = (
        _format_datetime_12h(order_out.pickup_time)
        if order_out.pickup_time
        else ""
    )

    # ── Salutation ────────────────────────────────────────────────────────────
    salutation = tr["salutation_map"].get(user.salutation, user.salutation)

    html = _build_html(
        user=user,
        salutation=salutation,
        pickup_display=pickup_display,
        items_data=items_data,
        order_number=order_number,
        total_price=total_price,
        total_original=total_original,
        tr=tr,
    )

    subject = tr["subject"].replace("{order_number}", order_number)
    resend_domain_verified = os.getenv("RESEND_DOMAIN_VERIFIED", "false").lower() == "true"
    recipients = list({user.email, OWNER_EMAIL}) if resend_domain_verified else [OWNER_EMAIL]

    try:
        resend.api_key = resend_api_key
        resend.Emails.send({
            "from": from_email,
            "to": recipients,
            "subject": subject,
            "html": html,
        })
        print(f"Order confirmation email sent to {recipients}")
    except Exception as e:
        print(f"Email sending failed: {e}")


def _build_html(user, salutation, pickup_display, items_data, order_number,
                total_price, total_original, tr):
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
        pos_label = _position_label(pos, tr)

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

    # ── Greeting ──────────────────────────────────────────────────────────────
    greeting = (
        tr["greeting"]
        .replace("{first_name}", user.first_name)
        .replace("{last_name}", user.last_name)
        .replace("{salutation}", salutation)
    )

    # ── Pickup info line ──────────────────────────────────────────────────────
    orders_link = (
        f'<a href="https://schristy2020.github.io/homefinds/#/orders" '
        f'style="color:#c9a96e;text-decoration:underline;">{tr["my_orders_link_text"]}</a>'
    )
    pickup_editable = tr["pickup_editable"].replace("{link}", orders_link)
    pickup_line = (
        f'<p style="color:#666;font-size:13px;margin:4px 0 8px;">'
        f'{tr["pickup_info"].replace("{date}", f"<strong>{pickup_display}</strong>")}'
        f'<em>{pickup_editable}</em></p>'
        if pickup_display
        else ""
    )

    # ── Payment notes ─────────────────────────────────────────────────────────
    payment_notes_html = "".join(
        f'<li style="margin-bottom:5px;line-height:1.5;">{note}</li>'
        for note in tr["payment_notes"]
    )

    # ── Step 1 items ──────────────────────────────────────────────────────────
    step1_items_html = "".join(
        f'<li style="font-size:12px;color:#444;line-height:1.5;">{item}</li>'
        for item in tr["step1_items"]
    )

    # ── Step 2 items ──────────────────────────────────────────────────────────
    step2_items_html = ""
    for item in tr["step2_items"]:
        step2_items_html += f'<li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">{item}</li>'
    # Insert pay method item at index 2 (after 2nd item)
    step2_pay_item = f"""<li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">
                    {tr["step2_pay_label"]}
                    <div style="margin-top:4px;padding:6px 10px;font-weight:600;color:#1a1a1a;">
                      <div>{tr["step2_zelle_a"]}</div>
                      <div>{tr["step2_zelle_b"]}</div>
                      <div>{tr["step2_zelle_c"]}</div>
                    </div>
                  </li>"""
    # Rebuild step2 with pay item inserted at position 3 (between item 2 and 3)
    step2_items_list = tr["step2_items"]
    step2_items_html = ""
    for idx, item in enumerate(step2_items_list):
        step2_items_html += f'<li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">{item}</li>'
        if idx == 1:  # after 2nd item, insert pay info
            step2_items_html += step2_pay_item

    # ── Step 3 items ──────────────────────────────────────────────────────────
    step3_items_html = "".join(
        f'<li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">{item}</li>'
        for item in tr["step3_items"]
    )
    step3_items_html += f"""<li style="font-size:12px;color:#444;line-height:1.5;margin-bottom:4px;">
                    <span style="display:block;">{tr["step3_location_label"]}</span>
                    <a href="https://maps.app.goo.gl/HiHjmGr1PLTvgbex9" target="_blank"
                       style="display:inline-block;margin-top:4px;padding:6px 10px;background:#f9f7f4;border-radius:6px;text-decoration:none;">
                      <span style="font-weight:600;color:#c9a96e;display:block;">{tr["step3_location_name"]}</span>
                      <span style="font-size:11px;color:#666;">{tr["step3_location_address"]}</span>
                    </a>
                    <br/>
                    <img src="https://schristy2020.github.io/homefinds/images/pickup-location.jpg"
                         alt="Pickup Location"
                         width="300"
                         style="margin-top:8px;border-radius:8px;display:block;max-width:100%;" />
                  </li>"""

    total_label = tr["total"].replace("{count}", str(len(items_data)))

    return f"""<!DOCTYPE html>
<html lang="{tr["html_lang"]}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{tr["header"]}</title>
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
              <h1 style="margin:0;font-size:22px;font-weight:700;color:#1a1a1a;"><a href="https://schristy2020.github.io/homefinds/" style="color:#c9a96e;text-decoration:underline;">Christy's HomeFinds</a> {tr["header"].replace("Christy's HomeFinds ", "")}</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:24px 28px;">

              <!-- Greeting -->
              <p style="font-size:15px;font-weight:700;margin:0 0 4px;">
                {greeting}
              </p>
              {pickup_line}
              <ul style="margin:0 0 16px;padding-left:20px;font-size:13px;list-style:disc;">
                <li style="margin-bottom:3px;">Name: <strong>{user.first_name} {user.last_name}</strong></li>
                <li style="margin-bottom:3px;">Email: <strong>{user.email}</strong></li>
                <li style="margin-bottom:3px;">Phone: <strong>{user.phone}</strong></li>
              </ul>

              <!-- Payment Notice -->
              <div style="background:#fffbf0;border:1.5px solid #f0d080;border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:13px;">
                <p style="font-weight:700;margin:0 0 8px;font-size:13px;">
                  {tr["payment_title"]}
                </p>
                <ul style="margin:0;padding-left:18px;">
                  {payment_notes_html}
                </ul>
              </div>

              <!-- Zelle Info -->
              <div style="margin-bottom:16px;font-size:13px;">
                <p style="font-weight:700;margin:0 0 6px;">{tr["zelle_title"]}</p>
                <ul style="margin:0;padding-left:20px;list-style:disc;">
                  <li style="margin-bottom:3px;">{tr["zelle_account"]}</li>
                  <li style="margin-bottom:3px;">{tr["zelle_name"]}</li>
                  <li>{tr["zelle_note"]}</li>
                </ul>
              </div>

              <!-- Order Number -->
              <p style="font-size:14px;font-weight:700;margin:0 0 16px;">
                {tr["order_number_label"]}
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
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;width:50px;">{tr["col_thumb"]}</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;">{tr["col_name"]}</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;">{tr["col_pickup"]}</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:right;">{tr["col_price"]}</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:center;">{tr["col_position"]}</th>
                  </tr>
                </thead>
                <tbody>{item_rows}
                </tbody>
              </table>

              <!-- Total -->
              <div style="display:flex;justify-content:space-between;padding:8px 0 4px;font-size:15px;font-weight:600;border-top:1px solid #eee;">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="font-size:14px;font-weight:600;">{total_label}</td>
                    <td style="text-align:right;font-size:15px;font-weight:700;">
                      {total_original_html}${_format_price(total_price)}
                    </td>
                  </tr>
                </table>
              </div>

              <!-- Divider -->
              <hr style="border:none;border-top:1px solid #e8e8e8;margin:20px 0;" />

              <!-- Guide Section -->
              <h3 style="font-size:14px;font-weight:700;color:#1a1a1a;margin:0 0 14px;">{tr["guide_title"]}</h3>

              <!-- Step 1 -->
              <div style="margin-bottom:14px;font-size:13px;">
                <p style="font-size:13px;font-weight:700;color:#c9a96e;margin:0 0 6px;">{tr["step1_title"]}</p>
                <ol style="margin:0;padding-left:18px;">
                  {step1_items_html}
                  <li style="font-size:12px;color:#c0392b;font-weight:600;list-style:none;margin-left:-18px;">{tr["step1_warning"]}</li>
                </ol>
              </div>

              <!-- Step 2 -->
              <div style="margin-bottom:14px;font-size:13px;">
                <p style="font-size:13px;font-weight:700;color:#c9a96e;margin:0 0 6px;">{tr["step2_title"]}</p>
                <p style="font-size:12px;color:#555;margin:0 0 6px;">{tr["step2_intro"]}</p>
                <ol style="margin:0;padding-left:18px;">
                  {step2_items_html}
                </ol>
              </div>

              <!-- Step 3 -->
              <div style="margin-bottom:14px;font-size:13px;">
                <p style="font-size:13px;font-weight:700;color:#c9a96e;margin:0 0 6px;">{tr["step3_title"]}</p>
                <ul style="margin:0;padding-left:18px;">
                  {step3_items_html}
                </ul>
              </div>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:16px 28px 28px;border-top:1px solid #f0f0f0;font-size:12px;color:#888;text-align:center;">
              {tr["footer"]}
              <a href="mailto:qsa8647332@gmail.com" style="color:#c9a96e;text-decoration:none;">qsa8647332@gmail.com</a>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
