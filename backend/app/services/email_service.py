import os
import time
import resend

from app.models.product import Product, ProductTranslation, ProductImage
from app.models.room import RoomTranslation

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

# ── Restore notification translations ─────────────────────────────────────────
RESTORE_EMAIL_TRANSLATIONS = {
    "zh-TW": {
        "html_lang": "zh-TW",
        "subject": "【好消息】您訂單中的商品恢復販售了！- Christy's HomeFinds",
        "header": "商品恢復販售通知",
        "greeting": "Hi {first_name}，好消息！",
        "body": "您訂單中，原本已出售的商品現已恢復販售。本場採用「先付款先得」制，請把握機會完成付款！",
        "col_name": "物品名稱",
        "col_price": "價錢",
        "zelle_title": "💰 Zelle 匯款資訊：",
        "zelle_account": "帳號: (984)373-9392",
        "zelle_name": "戶名: SHU CHING LI",
        "zelle_note": "備註: 請務必註明您的「訂單編號」",
        "orders_link_text": "前往查看我的訂單",
        "footer": "💡 有任何問題？歡迎聯絡 Christy:",
        "anytime": "隨時",
    },
    "zh-CN": {
        "html_lang": "zh-CN",
        "subject": "【好消息】您订单中的商品恢复销售了！- Christy's HomeFinds",
        "header": "商品恢复销售通知",
        "greeting": "Hi {first_name}，好消息！",
        "body": "您订单中，原本已售出的商品现已恢复销售。本场采用「先付款先得」制，请把握机会完成付款！",
        "col_name": "物品名称",
        "col_price": "价格",
        "zelle_title": "💰 Zelle 汇款信息：",
        "zelle_account": "帐号: (984)373-9392",
        "zelle_name": "户名: SHU CHING LI",
        "zelle_note": "备注: 请务必注明您的「订单编号」",
        "orders_link_text": "前往查看我的订单",
        "footer": "💡 有任何问题？欢迎联络 Christy:",
        "anytime": "随时",
    },
    "en": {
        "html_lang": "en",
        "subject": "Great News! An item in your order is back for sale! - Christy's HomeFinds",
        "header": "Items Back on Sale",
        "greeting": "Hi {first_name}, Good news!",
        "body": "An item in your order that was previously sold out is now available again. Please note that we operate on a \"first-pay, first-served\" basis. Don’t miss this chance to complete your purchase!",
        "col_name": "Item Name",
        "col_price": "Price",
        "zelle_title": "💰 Zelle Payment Information:",
        "zelle_account": "Account: (984)373-9392",
        "zelle_name": "Account Name: SHU CHING LI",
        "zelle_note": "Note: Please include your \"Order Number\" in the memo.",
        "orders_link_text": "Go to My Order",
        "footer": "💡 Have questions? Feel free to contact Christy at:",
        "anytime": "Anytime",
    },
}

# ── Payment success email translations ────────────────────────────────────────
PAYMENT_SUCCESS_TRANSLATIONS = {
    "zh-TW": {
        "html_lang": "zh-TW",
        "subject": "✅ 付款成功！訂單 {order_number} - Christy's HomeFinds",
        "header": "付款成功通知",
        "emoji": "✅",
        "greeting": "Hi {first_name}，付款成功！",
        "body": "感謝您的付款！期待於 {pickup_time} 與您見面領取物品。",
        "order_number_label": "訂單編號：",
        "col_name": "物品名稱",
        "col_price": "價錢",
        "orders_link_text": "查看我的訂單",
        "footer": "💡 有任何問題？歡迎聯絡 Christy:",
        "anytime": "隨時",
    },
    "zh-CN": {
        "html_lang": "zh-CN",
        "subject": "✅ 付款成功！订单 {order_number} - Christy's HomeFinds",
        "header": "付款成功通知",
        "emoji": "✅",
        "greeting": "Hi {first_name}，付款成功！",
        "body": "感谢您的付款！期待于 {pickup_time} 与您见面领取物品。",
        "order_number_label": "订单编号：",
        "col_name": "物品名称",
        "col_price": "价格",
        "orders_link_text": "查看我的订单",
        "footer": "💡 有任何问题？欢迎联络 Christy:",
        "anytime": "随时",
    },
    "en": {
        "html_lang": "en",
        "subject": "✅ Payment Confirmed! Order {order_number} - Christy's HomeFinds",
        "header": "Payment Confirmed",
        "emoji": "✅",
        "greeting": "Hi {first_name}, payment confirmed!",
        "body": "Thank you for your payment! We look forward to seeing you on {pickup_time} for pickup.",
        "order_number_label": "Order ID:",
        "col_name": "Item",
        "col_price": "Price",
        "orders_link_text": "View My Orders",
        "footer": "💡 Questions? Feel free to contact Christy:",
        "anytime": "Anytime",
    },
}

# ── Item snatched (order still active) email translations ─────────────────────
ITEM_SNATCHED_PENDING_TRANSLATIONS = {
    "zh-TW": {
        "html_lang": "zh-TW",
        "subject": "⚠️ 訂單中有商品已被搶購 - Christy's HomeFinds",
        "header": "商品已被搶先付款",
        "emoji": "⚠️",
        "greeting": "Hi {first_name}，",
        "body": "訂單中，有商品被人搶先付款了！提醒為了能確保其他商品，請盡速付款。",
        "col_name": "物品名稱",
        "col_price": "價錢",
        "zelle_title": "💰 Zelle 匯款資訊：",
        "zelle_account": "帳號: (984)373-9392",
        "zelle_name": "戶名: SHU CHING LI",
        "zelle_note": "備註: 請務必註明您的「訂單編號」",
        "orders_link_text": "立即前往付款",
        "footer": "💡 有任何問題？歡迎聯絡 Christy:",
        "anytime": "隨時",
    },
    "zh-CN": {
        "html_lang": "zh-CN",
        "subject": "⚠️ 订单中有商品已被抢购 - Christy's HomeFinds",
        "header": "商品已被抢先付款",
        "emoji": "⚠️",
        "greeting": "Hi {first_name}，",
        "body": "订单中，有商品被人抢先付款了！提醒为了能确保其他商品，请尽速付款。",
        "col_name": "物品名称",
        "col_price": "价格",
        "zelle_title": "💰 Zelle 汇款信息：",
        "zelle_account": "帐号: (984)373-9392",
        "zelle_name": "户名: SHU CHING LI",
        "zelle_note": "备注: 请务必注明您的「订单编号」",
        "orders_link_text": "立即前往付款",
        "footer": "💡 有任何问题？欢迎联络 Christy:",
        "anytime": "随时",
    },
    "en": {
        "html_lang": "en",
        "subject": "⚠️ An item in your order was just purchased - Christy's HomeFinds",
        "header": "Item Purchased by Someone Else",
        "emoji": "⚠️",
        "greeting": "Hi {first_name},",
        "body": "Someone beat you to the payment for an item in your order! To secure your remaining items, please complete your payment as soon as possible.",
        "col_name": "Item",
        "col_price": "Price",
        "zelle_title": "💰 Zelle Payment Details:",
        "zelle_account": "Account: (984)373-9392",
        "zelle_name": "Name: SHU CHING LI",
        "zelle_note": "Note: Please include your \"Order ID\" in the memo.",
        "orders_link_text": "Pay Now",
        "footer": "💡 Questions? Feel free to contact Christy:",
        "anytime": "Anytime",
    },
}

# ── Order auto-cancelled email translations ────────────────────────────────────
ORDER_AUTO_CANCELLED_TRANSLATIONS = {
    "zh-TW": {
        "html_lang": "zh-TW",
        "subject": "❌ 您的訂單已被取消 - Christy's HomeFinds",
        "header": "訂單已自動取消",
        "emoji": "❌",
        "greeting": "Hi {first_name}，",
        "body": "您的訂單中，有商品被人搶先付款了！因此您的訂單已被自動取消。",
        "order_number_label": "訂單編號：",
        "col_name": "物品名稱",
        "col_price": "價錢",
        "orders_link_text": "查看我的訂單",
        "footer": "💡 有任何問題？歡迎聯絡 Christy:",
        "anytime": "隨時",
    },
    "zh-CN": {
        "html_lang": "zh-CN",
        "subject": "❌ 您的订单已被取消 - Christy's HomeFinds",
        "header": "订单已自动取消",
        "emoji": "❌",
        "greeting": "Hi {first_name}，",
        "body": "您的订单中，有商品被人抢先付款了！因此您的订单已被自动取消。",
        "order_number_label": "订单编号：",
        "col_name": "物品名称",
        "col_price": "价格",
        "orders_link_text": "查看我的订单",
        "footer": "💡 有任何问题？欢迎联络 Christy:",
        "anytime": "随时",
    },
    "en": {
        "html_lang": "en",
        "subject": "❌ Your order has been cancelled - Christy's HomeFinds",
        "header": "Order Automatically Cancelled",
        "emoji": "❌",
        "greeting": "Hi {first_name},",
        "body": "All items in your order have been purchased by someone else. As a result, your order has been automatically cancelled.",
        "order_number_label": "Order ID:",
        "col_name": "Item",
        "col_price": "Price",
        "orders_link_text": "View My Orders",
        "footer": "💡 Questions? Feel free to contact Christy:",
        "anytime": "Anytime",
    },
}

# ── Order status reverted (paid → pending/cancelled) email translations ─────────
ORDER_STATUS_REVERTED_TRANSLATIONS = {
    "zh-TW": {
        "html_lang": "zh-TW",
        "subject": "⚠️ 訂單狀態已變更 - Christy's HomeFinds",
        "header": "訂單狀態已變更",
        "emoji": "⚠️",
        "greeting": "Hi {first_name}，",
        "body_pending": "您的訂單狀態已由「已付款」更改為「待付款」，請確認訂單詳情，若有任何疑問請聯絡 Christy。",
        "body_cancelled": "您的訂單狀態已由「已付款」更改為「已取消」，若有任何疑問請聯絡 Christy。",
        "order_number_label": "訂單編號：",
        "col_name": "物品名稱",
        "col_price": "價錢",
        "orders_link_text": "查看我的訂單",
        "footer": "💡 有任何問題？歡迎聯絡 Christy:",
        "anytime": "隨時",
    },
    "zh-CN": {
        "html_lang": "zh-CN",
        "subject": "⚠️ 订单状态已变更 - Christy's HomeFinds",
        "header": "订单状态已变更",
        "emoji": "⚠️",
        "greeting": "Hi {first_name}，",
        "body_pending": "您的订单状态已由「已付款」更改为「待付款」，请确认订单详情，如有疑问请联络 Christy。",
        "body_cancelled": "您的订单状态已由「已付款」更改为「已取消」，如有疑问请联络 Christy。",
        "order_number_label": "订单编号：",
        "col_name": "物品名称",
        "col_price": "价格",
        "orders_link_text": "查看我的订单",
        "footer": "💡 有任何问题？欢迎联络 Christy:",
        "anytime": "随时",
    },
    "en": {
        "html_lang": "en",
        "subject": "⚠️ Order Status Updated - Christy's HomeFinds",
        "header": "Order Status Updated",
        "emoji": "⚠️",
        "greeting": "Hi {first_name},",
        "body_pending": "Your order status has been changed from 'Paid' to 'Pending Payment'. Please review your order details. Contact Christy if you have any questions.",
        "body_cancelled": "Your order status has been changed from 'Paid' to 'Cancelled'. Please contact Christy if you have any questions.",
        "order_number_label": "Order ID:",
        "col_name": "Item",
        "col_price": "Price",
        "orders_link_text": "View My Orders",
        "footer": "💡 Questions? Feel free to contact Christy:",
        "anytime": "Anytime",
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


def send_product_restored_notification(user, restored_product_ids, db):
    """通知買家：訂單中原本已出售的商品恢復販售了。"""
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM", "")
    if not resend_api_key or not from_email:
        print("Email skipped: RESEND_API_KEY / RESEND_FROM not configured")
        return

    locale = getattr(user, "locale", "zh-TW") or "zh-TW"
    tr = RESTORE_EMAIL_TRANSLATIONS.get(locale, RESTORE_EMAIL_TRANSLATIONS["zh-TW"])
    db_locale = _LOCALE_TO_DB.get(locale, "zh-TW")

    products_data = []
    for pid in restored_product_ids:
        product = db.query(Product).filter(Product.id == pid).first()
        if not product:
            continue
        translation = db.query(ProductTranslation).filter(
            ProductTranslation.product_id == pid,
            ProductTranslation.locale == db_locale,
        ).first()
        if not translation and db_locale != "zh-TW":
            translation = db.query(ProductTranslation).filter(
                ProductTranslation.product_id == pid,
                ProductTranslation.locale == "zh-TW",
            ).first()
        image = (
            db.query(ProductImage)
            .filter(ProductImage.product_id == pid)
            .order_by(ProductImage.sort_order)
            .first()
        )
        name = translation.name if translation else (product.code if product else str(pid))
        img_url = image.url if image else ""
        price = float(product.price)
        original_price = float(product.original_price) if product.original_price else None
        products_data.append({
            "name": name,
            "img_url": img_url,
            "price": price,
            "original_price": original_price,
        })

    if not products_data:
        return

    greeting = tr["greeting"].replace("{first_name}", user.first_name)

    # Build product rows
    item_rows = ""
    for item in products_data:
        original_td = (
            f'<span style="text-decoration:line-through;color:#aaa;margin-right:4px;">'
            f'${_format_price(item["original_price"])}</span>'
            if item["original_price"] is not None else ""
        )
        thumb_cell = (
            f'<img src="{item["img_url"]}" width="40" height="40" '
            f'style="border-radius:4px;object-fit:cover;display:block;" />'
            if item["img_url"]
            else '<div style="width:40px;height:40px;background:#eee;border-radius:4px;"></div>'
        )
        item_rows += f"""
        <tr>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;">{thumb_cell}</td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;font-size:13px;">{item["name"]}</td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;font-size:13px;font-weight:600;text-align:right;white-space:nowrap;">
            {original_td}${_format_price(item["price"])}
          </td>
        </tr>"""

    orders_link = (
        f'<a href="https://schristy2020.github.io/homefinds/#/orders" '
        f'style="color:#c9a96e;text-decoration:underline;">{tr["orders_link_text"]}</a>'
    )

    html = f"""<!DOCTYPE html>
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
              <div style="font-size:36px;margin-bottom:8px;">🎉</div>
              <h1 style="margin:0;font-size:22px;font-weight:700;color:#1a1a1a;">
                <a href="https://schristy2020.github.io/homefinds/" style="color:#c9a96e;text-decoration:underline;">Christy's HomeFinds</a>
                — {tr["header"]}
              </h1>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:24px 28px;">
              <p style="font-size:15px;font-weight:700;margin:0 0 8px;">{greeting}</p>
              <p style="font-size:13px;color:#444;margin:0 0 16px;">{tr["body"]}</p>

              <!-- Product table -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="border-collapse:collapse;margin-bottom:16px;font-size:13px;">
                <thead>
                  <tr style="border-bottom:1.5px solid #e0e0e0;">
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;width:50px;"></th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;">{tr["col_name"]}</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:right;">{tr["col_price"]}</th>
                  </tr>
                </thead>
                <tbody>{item_rows}
                </tbody>
              </table>

              <!-- Zelle info -->
              <div style="margin-bottom:16px;font-size:13px;">
                <p style="font-weight:700;margin:0 0 6px;">{tr["zelle_title"]}</p>
                <ul style="margin:0;padding-left:20px;list-style:disc;">
                  <li style="margin-bottom:3px;">{tr["zelle_account"]}</li>
                  <li style="margin-bottom:3px;">{tr["zelle_name"]}</li>
                  <li>{tr["zelle_note"]}</li>
                </ul>
              </div>

              <p style="font-size:13px;color:#444;margin:0;">{orders_link}</p>
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

    subject = tr["subject"]
    resend_domain_verified = os.getenv("RESEND_DOMAIN_VERIFIED", "false").lower() == "true"
    to = [user.email] if resend_domain_verified else [OWNER_EMAIL]
    cc = [OWNER_EMAIL] if resend_domain_verified else []
    params = {"from": from_email, "to": to, "subject": subject, "html": html}
    if cc:
        params["cc"] = cc

    try:
        time.sleep(1)
        resend.api_key = resend_api_key
        resend.Emails.send(params)
        print(f"Restore notification sent to={to} cc={cc}")
    except Exception as e:
        print(f"Email sending failed: {e}")


def _build_simple_product_rows(product_ids, db, db_locale):
    """Shared helper: build (products_data, item_rows_html) for a list of product IDs."""
    products_data = []
    for pid in product_ids:
        product = db.query(Product).filter(Product.id == pid).first()
        if not product:
            continue
        translation = db.query(ProductTranslation).filter(
            ProductTranslation.product_id == pid,
            ProductTranslation.locale == db_locale,
        ).first()
        if not translation and db_locale != "zh-TW":
            translation = db.query(ProductTranslation).filter(
                ProductTranslation.product_id == pid,
                ProductTranslation.locale == "zh-TW",
            ).first()
        image = (
            db.query(ProductImage)
            .filter(ProductImage.product_id == pid)
            .order_by(ProductImage.sort_order)
            .first()
        )
        name = translation.name if translation else (product.code if product else str(pid))
        img_url = image.url if image else ""
        price = float(product.price)
        original_price = float(product.original_price) if product.original_price else None
        products_data.append({"name": name, "img_url": img_url, "price": price, "original_price": original_price})

    item_rows = ""
    for item in products_data:
        original_td = (
            f'<span style="text-decoration:line-through;color:#aaa;margin-right:4px;">'
            f'${_format_price(item["original_price"])}</span>'
            if item["original_price"] is not None else ""
        )
        thumb_cell = (
            f'<img src="{item["img_url"]}" width="40" height="40" '
            f'style="border-radius:4px;object-fit:cover;display:block;" />'
            if item["img_url"]
            else '<div style="width:40px;height:40px;background:#eee;border-radius:4px;"></div>'
        )
        item_rows += f"""
        <tr>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;">{thumb_cell}</td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;font-size:13px;">{item["name"]}</td>
          <td style="padding:8px 6px;border-bottom:1px solid #e8e8e8;font-size:13px;font-weight:600;text-align:right;white-space:nowrap;">
            {original_td}${_format_price(item["price"])}
          </td>
        </tr>"""
    return products_data, item_rows


def _build_simple_email_html(tr, greeting, body_text, product_ids, db, db_locale,
                              order_number=None, extra_section_html=""):
    """Build a simple email HTML with optional product table."""
    _, item_rows = _build_simple_product_rows(product_ids, db, db_locale)

    orders_link = (
        f'<a href="https://schristy2020.github.io/homefinds/#/orders" '
        f'style="color:#c9a96e;text-decoration:underline;">{tr["orders_link_text"]}</a>'
    )

    order_number_html = ""
    if order_number:
        order_number_html = f"""
              <p style="font-size:14px;font-weight:700;margin:0 0 16px;">
                {tr["order_number_label"]}
                <span style="font-family:monospace;background:#f4f4f4;border-radius:4px;padding:3px 10px;letter-spacing:0.05em;margin-left:4px;">
                  {order_number}
                </span>
              </p>"""

    product_table_html = ""
    if item_rows:
        product_table_html = f"""
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="border-collapse:collapse;margin-bottom:16px;font-size:13px;">
                <thead>
                  <tr style="border-bottom:1.5px solid #e0e0e0;">
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;width:50px;"></th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:left;">{tr["col_name"]}</th>
                    <th style="padding:6px;color:#888;font-weight:500;font-size:12px;text-align:right;">{tr["col_price"]}</th>
                  </tr>
                </thead>
                <tbody>{item_rows}
                </tbody>
              </table>"""

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
              <div style="font-size:36px;margin-bottom:8px;">{tr["emoji"]}</div>
              <h1 style="margin:0;font-size:22px;font-weight:700;color:#1a1a1a;">
                <a href="https://schristy2020.github.io/homefinds/" style="color:#c9a96e;text-decoration:underline;">Christy's HomeFinds</a>
                — {tr["header"]}
              </h1>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:24px 28px;">
              <p style="font-size:15px;font-weight:700;margin:0 0 8px;">{greeting}</p>
              <p style="font-size:13px;color:#444;margin:0 0 16px;">{body_text}</p>
              {order_number_html}
              {product_table_html}
              {extra_section_html}
              <p style="font-size:13px;color:#444;margin:0;">{orders_link}</p>
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


def _send_simple_email(user, subject, html, resend_api_key, from_email):
    resend_domain_verified = os.getenv("RESEND_DOMAIN_VERIFIED", "false").lower() == "true"
    to = [user.email] if resend_domain_verified else [OWNER_EMAIL]
    cc = [OWNER_EMAIL] if resend_domain_verified else []
    params = {"from": from_email, "to": to, "subject": subject, "html": html}
    if cc:
        params["cc"] = cc
    try:
        time.sleep(1)
        resend.api_key = resend_api_key
        resend.Emails.send(params)
        print(f"Email sent to={to} cc={cc}: {subject[:50]}")
    except Exception as e:
        print(f"Email sending failed: {e}")


def send_payment_success_notification(user, order_number, pickup_time, paid_product_ids, db):
    """付款成功通知 — 寄給付款訂單的 user。"""
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM", "")
    if not resend_api_key or not from_email:
        print("Email skipped: RESEND_API_KEY / RESEND_FROM not configured")
        return

    locale = getattr(user, "locale", "zh-TW") or "zh-TW"
    tr = PAYMENT_SUCCESS_TRANSLATIONS.get(locale, PAYMENT_SUCCESS_TRANSLATIONS["zh-TW"])
    db_locale = _LOCALE_TO_DB.get(locale, "zh-TW")

    pickup_str = _format_datetime_12h(pickup_time) if pickup_time else tr["anytime"]
    greeting = tr["greeting"].replace("{first_name}", user.first_name)
    body_text = tr["body"].replace("{pickup_time}", f"<strong>{pickup_str}</strong>")

    html = _build_simple_email_html(
        tr=tr,
        greeting=greeting,
        body_text=body_text,
        product_ids=paid_product_ids,
        db=db,
        db_locale=db_locale,
        order_number=order_number,
    )
    subject = tr["subject"].replace("{order_number}", order_number)
    _send_simple_email(user, subject, html, resend_api_key, from_email)


def send_item_snatched_pending_notification(user, snatched_product_ids, db):
    """有商品被搶先付款，但訂單中還有未售出商品 — 提醒盡速付款。"""
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM", "")
    if not resend_api_key or not from_email:
        print("Email skipped: RESEND_API_KEY / RESEND_FROM not configured")
        return

    locale = getattr(user, "locale", "zh-TW") or "zh-TW"
    tr = ITEM_SNATCHED_PENDING_TRANSLATIONS.get(locale, ITEM_SNATCHED_PENDING_TRANSLATIONS["zh-TW"])
    db_locale = _LOCALE_TO_DB.get(locale, "zh-TW")

    greeting = tr["greeting"].replace("{first_name}", user.first_name)

    zelle_section = f"""
              <div style="margin-bottom:16px;font-size:13px;">
                <p style="font-weight:700;margin:0 0 6px;">{tr["zelle_title"]}</p>
                <ul style="margin:0;padding-left:20px;list-style:disc;">
                  <li style="margin-bottom:3px;">{tr["zelle_account"]}</li>
                  <li style="margin-bottom:3px;">{tr["zelle_name"]}</li>
                  <li>{tr["zelle_note"]}</li>
                </ul>
              </div>"""

    html = _build_simple_email_html(
        tr=tr,
        greeting=greeting,
        body_text=tr["body"],
        product_ids=snatched_product_ids,
        db=db,
        db_locale=db_locale,
        extra_section_html=zelle_section,
    )
    _send_simple_email(user, tr["subject"], html, resend_api_key, from_email)


def send_order_auto_cancelled_notification(user, order_number, snatched_product_ids, db):
    """訂單中所有商品皆被搶購，訂單已自動取消 — 通知 user。"""
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM", "")
    if not resend_api_key or not from_email:
        print("Email skipped: RESEND_API_KEY / RESEND_FROM not configured")
        return

    locale = getattr(user, "locale", "zh-TW") or "zh-TW"
    tr = ORDER_AUTO_CANCELLED_TRANSLATIONS.get(locale, ORDER_AUTO_CANCELLED_TRANSLATIONS["zh-TW"])
    db_locale = _LOCALE_TO_DB.get(locale, "zh-TW")

    greeting = tr["greeting"].replace("{first_name}", user.first_name)

    html = _build_simple_email_html(
        tr=tr,
        greeting=greeting,
        body_text=tr["body"],
        product_ids=snatched_product_ids,
        db=db,
        db_locale=db_locale,
        order_number=order_number,
    )
    subject = tr["subject"]
    _send_simple_email(user, subject, html, resend_api_key, from_email)


def send_order_status_reverted_notification(user, order_number, target_status, product_ids, db):
    """訂單從「已付款」改為「待付款」或「取消」 — 通知 user。"""
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM", "")
    if not resend_api_key or not from_email:
        print("Email skipped: RESEND_API_KEY / RESEND_FROM not configured")
        return

    locale = getattr(user, "locale", "zh-TW") or "zh-TW"
    tr = ORDER_STATUS_REVERTED_TRANSLATIONS.get(locale, ORDER_STATUS_REVERTED_TRANSLATIONS["zh-TW"])
    db_locale = _LOCALE_TO_DB.get(locale, "zh-TW")

    greeting = tr["greeting"].replace("{first_name}", user.first_name)
    body_text = tr["body_pending"] if target_status == "pending_payment" else tr["body_cancelled"]

    html = _build_simple_email_html(
        tr=tr,
        greeting=greeting,
        body_text=body_text,
        product_ids=product_ids,
        db=db,
        db_locale=db_locale,
        order_number=order_number,
    )
    subject = tr["subject"]
    _send_simple_email(user, subject, html, resend_api_key, from_email)


def send_order_confirmation(user, order_out, db):
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM", "")

    if not resend_api_key or not from_email:
        print("Email skipped: RESEND_API_KEY / RESEND_FROM not configured")
        return

    locale = getattr(user, "locale", "zh-TW") or "zh-TW"
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
    to = [user.email] if resend_domain_verified else [OWNER_EMAIL]
    cc = [OWNER_EMAIL] if resend_domain_verified else []
    params = {"from": from_email, "to": to, "subject": subject, "html": html}
    if cc:
        params["cc"] = cc

    try:
        time.sleep(1)
        resend.api_key = resend_api_key
        resend.Emails.send(params)
        print(f"Order confirmation email sent to={to} cc={cc}")
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


# ── Rent reservation confirmation translations ─────────────────────────────────
RENT_CONFIRMATION_TRANSLATIONS = {
    "zh-TW": {
        "html_lang": "zh-TW",
        "subject": "房源預留訂金支付提醒！訂單編號 {order_number} - Christy's HomeFinds",
        "header": "請盡快支付訂金以預留房源!",
        "greeting": "Hi {first_name}，您的預訂快完成了！",
        "deposit_warning": "日期將優先保留給「先完成付款」的房客。",
        "deposit_pay_note": "支付金額：請依訂單之訂金金額付款（總額之30%）。",
        "zelle_title": "🔥 Zelle 匯款資訊：",
        "zelle_account": "帳號: (984)373-9392",
        "zelle_name": "戶名: SHU CHING LI",
        "zelle_memo": "備註: 請務必註明您的「<strong>訂單編號</strong>」",
        "auto_cancel_note": "*若未在1小時內付款，該訂單將自動取消",
        "stay_info": "您的行程",
        "order_no_label": "訂單編號",
        "check_in_label": "入住時間",
        "check_out_label": "退房時間",
        "nights_label": "共{nights}晚",
        "original_label": "原價",
        "special_label": "特價",
        "early_bird_label": "早鳥優惠",
        "early_bird_note": "*3月預定優惠再9折",
        "deposit_amount_label": "訂金金額",
        "deposit_amount_note": "*請依此金額進行匯款",
        "basic_info": "基本資料",
        "label_first_name": "名字",
        "label_last_name": "姓氏",
        "label_salutation": "稱呼",
        "label_email": "Email",
        "label_phone": "電話",
        "label_birth_year": "出生年份",
        "label_occupation": "職業",
        "label_has_guests_pets": "是否有其他人或寵物入住?",
        "label_guests_pets_desc": "請簡單描述總入住人數、同住成員身分或寵物",
        "label_special_requests": "需求備註",
        "yes": "是",
        "no": "否",
        "booking_guide_title": "🏠 房間預訂流程說明",
        "booking_guide_deposit_title": "【下單與支付訂金】",
        "booking_guide_warning": "⚠️ 溫馨提醒：「下單成功」不代表「預定成功」！日期將優先保留給「先完成付款」的房客。",
        "booking_guide_pay_amount": "支付金額：請依訂單之訂金金額付款（總額之30%）。",
        "booking_guide_zelle_title": "付款方式（Zelle）：",
        "booking_guide_zelle_a": "a. 帳號: (984)373-9392",
        "booking_guide_zelle_b": "b. 戶名: SHU CHING LI",
        "booking_guide_zelle_c": "c. 備注: 訂單編號",
        "footer": "💡 有任何問題？歡迎聯絡 Christy:",
    },
    "zh-CN": {
        "html_lang": "zh-CN",
        "subject": "房源预留订金支付提醒！订单编号 {order_number} - Christy's HomeFinds",
        "header": "请尽快支付订金以预留房源!",
        "greeting": "Hi {first_name}，您的预订快完成了！",
        "deposit_warning": "日期将优先保留给「先完成付款」的房客。",
        "deposit_pay_note": "支付金额：请依订单之订金金额付款（总额之30%）。",
        "zelle_title": "🔥 Zelle 汇款资讯：",
        "zelle_account": "帐号: (984)373-9392",
        "zelle_name": "户名: SHU CHING LI",
        "zelle_memo": "备注: 请务必注明您的「<strong>订单编号</strong>」",
        "auto_cancel_note": "*若未在1小时内付款，该订单将自动取消",
        "stay_info": "您的行程",
        "order_no_label": "订单编号",
        "check_in_label": "入住时间",
        "check_out_label": "退房时间",
        "nights_label": "共{nights}晚",
        "original_label": "原价",
        "special_label": "特价",
        "early_bird_label": "早鸟优惠",
        "early_bird_note": "*3月预定优惠再9折",
        "deposit_amount_label": "订金金额",
        "deposit_amount_note": "*请依此金额进行汇款",
        "basic_info": "基本资料",
        "label_first_name": "名字",
        "label_last_name": "姓氏",
        "label_salutation": "称呼",
        "label_email": "Email",
        "label_phone": "电话",
        "label_birth_year": "出生年份",
        "label_occupation": "职业",
        "label_has_guests_pets": "是否有其他人或宠物入住?",
        "label_guests_pets_desc": "请简单描述总入住人数、同住成员身分或宠物",
        "label_special_requests": "需求备注",
        "yes": "是",
        "no": "否",
        "booking_guide_title": "🏠 房间预订流程说明",
        "booking_guide_deposit_title": "【下单与支付订金】",
        "booking_guide_warning": "⚠️ 温馨提醒：「下单成功」不代表「预定成功」！日期将优先保留给「先完成付款」的房客。",
        "booking_guide_pay_amount": "支付金额：请依订单之订金金额付款（总额之30%）。",
        "booking_guide_zelle_title": "付款方式（Zelle）：",
        "booking_guide_zelle_a": "a. 帐号: (984)373-9392",
        "booking_guide_zelle_b": "b. 户名: SHU CHING LI",
        "booking_guide_zelle_c": "c. 备注: 订单编号",
        "footer": "💡 有任何问题？欢迎联络 Christy:",
    },
    "en": {
        "html_lang": "en",
        "subject": "Secure your stay! Order No. {order_number} - Christy's HomeFinds",
        "header": "Complete your payment to secure your stay!",
        "greeting": "Hi {first_name}, your reservation is almost complete!",
        "deposit_warning": "Booking priority is given to guests who complete their deposit payment.",
        "deposit_pay_note": "Security Deposit: A 30% down payment is required to finalize your reservation.",
        "zelle_title": "🔥 Zelle Transfer Info:",
        "zelle_account": "Account: (984)373-9392",
        "zelle_name": "Recipient Name: SHU CHING LI",
        "zelle_memo": "Memo: Please include your <strong>Order No.</strong> in the memo.",
        "auto_cancel_note": "*Please note: This pending reservation will expire if the deposit is not received within 1 hour.",
        "stay_info": "Your Trip",
        "order_no_label": "Order No.",
        "check_in_label": "Check-in",
        "check_out_label": "Check-out",
        "nights_label": "{nights} nights",
        "original_label": "Original",
        "special_label": "Special",
        "early_bird_label": "Early Bird",
        "early_bird_note": "*Book in March for an extra 10% OFF!",
        "deposit_amount_label": "Deposit",
        "deposit_amount_note": "*Please transfer this exact amount to secure your booking.",
        "basic_info": "Basic Information",
        "label_first_name": "First Name",
        "label_last_name": "Last Name",
        "label_salutation": "Salutation",
        "label_email": "Email",
        "label_phone": "Phone",
        "label_birth_year": "Birth Year",
        "label_occupation": "Occupation",
        "label_has_guests_pets": "Will there be additional occupants or pets?",
        "label_guests_pets_desc": "Please provide details on occupants, relationships, and pets.",
        "label_special_requests": "Special Requests",
        "yes": "Yes",
        "no": "No",
        "booking_guide_title": "🏠 Booking Process",
        "booking_guide_deposit_title": "[Order & Pay Deposit]",
        "booking_guide_warning": "⚠️ Note: Placing an order does NOT guarantee your reservation. Dates will be held for guests who complete payment first.",
        "booking_guide_pay_amount": "Deposit: A 30% down payment is required to secure your booking.",
        "booking_guide_zelle_title": "Payment Method (Zelle):",
        "booking_guide_zelle_a": "a. Account: (984)373-9392",
        "booking_guide_zelle_b": "b. Recipient Name: SHU CHING LI",
        "booking_guide_zelle_c": "c. Memo: Order No.",
        "footer": "💡 Any questions? Feel free to contact Christy:",
    },
}


def send_reservation_confirmation(user, reservation, db):
    """寄送房源預留訂金支付提醒給房客，並 CC 給房東。"""
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM", "")
    if not resend_api_key or not from_email:
        print("Email skipped: RESEND_API_KEY / RESEND_FROM not configured")
        return

    locale = getattr(user, "locale", "zh-TW") or "zh-TW"
    tr = RENT_CONFIRMATION_TRANSLATIONS.get(locale, RENT_CONFIRMATION_TRANSLATIONS["zh-TW"])

    # Fetch admin-configured booking description for this locale
    room_translation = db.query(RoomTranslation).filter(
        RoomTranslation.locale == locale
    ).first()
    booking_description = (room_translation.booking_description or "") if room_translation else ""

    greeting = tr["greeting"].replace("{first_name}", user.first_name)
    order_number = reservation.order_number or ""
    subject = tr["subject"].replace("{order_number}", order_number)

    # Format dates MM/DD/YYYY
    def fmt_date(d):
        return f"{d.month:02d}/{d.day:02d}/{d.year}"

    check_in_str  = fmt_date(reservation.check_in)
    check_out_str = fmt_date(reservation.check_out)
    nights        = reservation.nights
    nights_str    = tr["nights_label"].replace("{nights}", str(nights))

    deposit_amount = _format_price(float(reservation.deposit_amount))

    # Price breakdown rows
    original_price   = float(reservation.original_price)   if reservation.original_price   else None
    special_price    = float(reservation.special_price)     if reservation.special_price     else None
    early_bird_price = float(reservation.early_bird_price)  if reservation.early_bird_price  else None
    is_early_bird    = bool(reservation.is_early_bird)

    original_price_html = ""
    if original_price is not None:
        original_price_html = f"""
              <tr>
                <td style="padding:4px 0;font-size:13px;color:#888;width:120px;">{tr["original_label"]}</td>
                <td style="padding:4px 0;font-size:13px;color:#aaa;text-decoration:line-through;">USD {_format_price(original_price)}</td>
              </tr>"""

    special_price_html = ""
    if special_price is not None:
        sp_style = "text-decoration:line-through;color:#aaa;" if is_early_bird else "font-size:1.1em;font-weight:700;color:#1a1a1a;"
        special_price_html = f"""
              <tr>
                <td style="padding:4px 0;font-size:13px;color:#888;">{tr["special_label"]}</td>
                <td style="padding:4px 0;font-size:13px;{sp_style}">USD {_format_price(special_price)}</td>
              </tr>"""

    early_bird_html = ""
    if is_early_bird and early_bird_price is not None:
        early_bird_html = f"""
              <tr>
                <td style="padding:4px 0;font-size:13px;color:#c0392b;font-weight:600;">{tr["early_bird_label"]}</td>
                <td style="padding:4px 0;font-size:1.1em;font-weight:800;color:#c0392b;">
                  USD {_format_price(early_bird_price)}
                  <span style="display: block;font-weight:500;margin-left:4px;">{tr["early_bird_note"]}</span>
                </td>
              </tr>"""

    # Basic info rows
    has_guests = bool(reservation.has_guests_or_pets)
    guests_desc = reservation.guests_pets_description or ""
    special_requests = reservation.special_requests or ""

    guests_pets_row = f"""
              <tr>
                <td style="padding:4px 0;font-size:13px;color:#888;width:160px;">{tr["label_has_guests_pets"]}</td>
                <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{tr["yes"] if has_guests else tr["no"]}</td>
              </tr>"""

    guests_desc_row = ""
    if has_guests and guests_desc:
        guests_desc_row = f"""
              <tr>
                <td style="padding:4px 0;font-size:13px;color:#888;">{tr["label_guests_pets_desc"]}</td>
                <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{guests_desc}</td>
              </tr>"""

    special_requests_row = ""
    if special_requests:
        special_requests_row = f"""
              <tr>
                <td style="padding:4px 0;font-size:13px;color:#888;">{tr["label_special_requests"]}</td>
                <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{special_requests}</td>
              </tr>"""

    birth_year = str(reservation.birth_year) if reservation.birth_year else ""
    occupation = reservation.occupation or ""

    html = f"""<!DOCTYPE html>
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
              <div style="font-size:36px;margin-bottom:8px;">🏠</div>
              <h1 style="margin:0;font-size:22px;font-weight:700;color:#1a1a1a;">
                <a href="https://schristy2020.github.io/homefinds/" style="color:#c9a96e;text-decoration:underline;">Christy's HomeFinds</a>
              </h1>
              <p style="margin:8px 0 0;font-size:17px;font-weight:700;color:#1a1a1a;">{tr["header"]}</p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:24px 28px;">

              <!-- Greeting -->
              <p style="font-size:15px;font-weight:700;margin:0 0 12px;">{greeting}</p>

              <!-- Deposit warning -->
              <p style="font-size:13px;margin:0 0 4px;">
                <span style="color:#e67e22;margin-right:4px;">⚠️</span>
                <strong>{tr["deposit_warning"]}</strong>
              </p>
              <p style="font-size:13px;color:#444;margin:0 0 16px;">&nbsp;&nbsp;· {tr["deposit_pay_note"]}</p>

              <!-- Zelle info -->
              <div style="margin-bottom:12px;font-size:13px;">
                <p style="font-weight:700;margin:0 0 6px;">{tr["zelle_title"]}</p>
                <ul style="margin:0;padding-left:20px;list-style:disc;">
                  <li style="margin-bottom:3px;">{tr["zelle_account"]}</li>
                  <li style="margin-bottom:3px;">{tr["zelle_name"]}</li>
                  <li>{tr["zelle_memo"]}</li>
                </ul>
              </div>

              <!-- Auto-cancel note -->
              <p style="font-size:14px;color:#c0392b;font-weight:600;margin:0 0 20px;">{tr["auto_cancel_note"]}</p>

              <hr style="border:none;border-top:1px solid #f0ebe3;margin:0 0 20px;" />

              <!-- Itinerary section -->
              <p style="font-size:14px;font-weight:700;color:#1a1a1a;margin:0 0 12px;">{tr["stay_info"]}</p>

              <!-- Order number -->
              <p style="font-size:13px;margin:0 0 10px;">
                <span style="color:#888;">{tr["order_no_label"]}</span>
                <span style="font-family:monospace;background:#f4f4f4;border-radius:4px;padding:2px 8px;letter-spacing:0.05em;font-weight:700;font-size: 20px;">{order_number}</span>
              </p>

              <!-- Dates -->
              <table cellpadding="0" cellspacing="0" style="margin-bottom:14px;">
                <tr>
                  <td style="font-size:12px;color:#888;">{tr["check_in_label"]}</td>
                  <td style="padding:0 12px;font-size:13px;color:#888;">→</td>
                  <td style="font-size:12px;color:#888;">{tr["check_out_label"]}</td>
                  <td style="padding-left:20px;font-size:13px;font-weight:600;color:#1a1a1a;white-space:nowrap;">{nights_str}</td>
                </tr>
                <tr>
                  <td style="font-size:15px;font-weight:700;color:#1a1a1a;">{check_in_str}</td>
                  <td></td>
                  <td style="font-size:15px;font-weight:700;color:#1a1a1a;">{check_out_str}</td>
                  <td></td>
                </tr>
              </table>

              <!-- Price breakdown -->
              <table cellpadding="0" cellspacing="0" style="margin-bottom:12px;width:100%;">
                <tbody>
                  {original_price_html}
                  {special_price_html}
                  {early_bird_html}
                  <tr>
                    <td style="padding:6px 0 4px;font-size:13px;color:#888;">{tr["deposit_amount_label"]}</td>
                    <td style="padding:6px 0 4px;">
                      <span style="font-size:1.2em;font-weight:800;color:#c0392b;">USD {deposit_amount}</span>
                      <span style="font-size:14px;font-weight: 700;color:#c0392b;margin-left:6px;display:block;">{tr["deposit_amount_note"]}</span>
                    </td>
                  </tr>
                </tbody>
              </table>

              <hr style="border:none;border-top:1px solid #f0ebe3;margin:0 0 20px;" />

              <!-- Basic info section -->
              <p style="font-size:14px;font-weight:700;color:#1a1a1a;margin:0 0 12px;">{tr["basic_info"]}</p>
              <table cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;">
                <tbody>
                  <tr>
                    <td style="padding:4px 0;font-size:13px;color:#888;width:160px;">{tr["label_first_name"]}</td>
                    <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{user.first_name}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 0;font-size:13px;color:#888;">{tr["label_last_name"]}</td>
                    <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{user.last_name}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 0;font-size:13px;color:#888;">{tr["label_salutation"]}</td>
                    <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{user.salutation}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 0;font-size:13px;color:#888;">{tr["label_email"]}</td>
                    <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{user.email}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 0;font-size:13px;color:#888;">{tr["label_phone"]}</td>
                    <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{user.phone}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 0;font-size:13px;color:#888;">{tr["label_birth_year"]}</td>
                    <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{birth_year}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 0;font-size:13px;color:#888;">{tr["label_occupation"]}</td>
                    <td style="padding:4px 0;font-size:13px;color:#1a1a1a;">{occupation}</td>
                  </tr>
                  {guests_pets_row}
                  {guests_desc_row}
                  {special_requests_row}
                </tbody>
              </table>

              <hr style="border:none;border-top:1px solid #f0ebe3;margin:20px 0;" />

              <!-- Booking guide (from admin settings) -->
              <div style="font-size:13px;color:#444;">{booking_description}</div>

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

    resend_domain_verified = os.getenv("RESEND_DOMAIN_VERIFIED", "false").lower() == "true"
    to = [user.email] if resend_domain_verified else [OWNER_EMAIL]
    cc = [OWNER_EMAIL] if resend_domain_verified else []
    params = {"from": from_email, "to": to, "subject": subject, "html": html}
    if cc:
        params["cc"] = cc

    try:
        time.sleep(1)
        resend.api_key = resend_api_key
        resend.Emails.send(params)
        print(f"Reservation confirmation sent to={to} cc={cc}: {subject[:60]}")
    except Exception as e:
        print(f"Reservation email sending failed: {e}")
