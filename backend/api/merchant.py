from flask import Blueprint, jsonify
# سنحتاج إلى استيراد نموذج 'Merchant' الذي من المفترض أن يكون موجودًا
# from ..models import Merchant # (سنقوم بإنشاء هذا النموذج لاحقًا إذا لم يكن موجودًا)

# ننشئ Blueprint جديدًا خاصًا بالتجار
merchant_bp = Blueprint('merchant_bp', __name__)

# --- المسار الأول: جلب جميع التجار ---
# هذا هو الـ API Endpoint الذي ستستدعيه واجهة الأدمن
@merchant_bp.route('/merchants', methods=['GET'])
def get_merchants():
    """
    API endpoint to get a list of all merchants.
    """
    # في الوقت الحالي، سنعيد قائمة وهمية (dummy data) لأننا لم نربط قاعدة البيانات بعد
    dummy_merchants = [
        {"id": 1, "name": "تاجر وهمي 1", "email": "merchant1@example.com"},
        {"id": 2, "name": "تاجر وهمي 2", "email": "merchant2@example.com"},
    ]
    
    # jsonify تقوم بتحويل قائمة بايثون إلى استجابة JSON صالحة
    return jsonify(dummy_merchants), 200

# يمكنك إضافة مسارات أخرى هنا لاحقًا (لإضافة تاجر، حذفه، إلخ)

