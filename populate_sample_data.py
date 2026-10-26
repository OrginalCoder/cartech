import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.product.models import Category, CarBrand, CarModel, Product
from apps.accounts.models import CustomUser, Profile

def populate():
    print("Test ma'lumotlarini yuklash boshlandi...")

    # 1. Superuser tekshirish/yaratish
    if not CustomUser.objects.filter(username='admin').exists():
        admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@cartech.uz',
            password='admin',
            first_name='Admin',
            last_name='CarTech',
            phone_number='+998901112233'
        )
        Profile.objects.get_or_create(user=admin_user, city='Toshkent', shipping_address='Amir Temur shoh ko\'chasi, 10')
        print("Superuser yaratildi: admin / admin")

    # 2. Car Brands & Models
    brands_data = {
        'Chevrolet': ['Cobalt', 'Gentra / Lacetti', 'Nexia 3', 'Tracker', 'Malibu 2', 'Onix', 'Damás'],
        'BYD': ['Song Plus', 'Chazor', 'Han', 'Song Pro'],
        'Kia': ['K5', 'Sportage', 'Seltos', 'Carnival'],
        'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
        'Toyota': ['Camry', 'Corolla', 'RAV4', 'Land Cruiser 300'],
        'BMW': ['3 Series (G20)', '5 Series (G30)', 'X5 (G05)'],
    }

    brand_objs = {}
    model_objs = {}
    for brand_name, models_list in brands_data.items():
        brand, _ = CarBrand.objects.get_or_create(name=brand_name)
        brand_objs[brand_name] = brand
        for m_name in models_list:
            model, _ = CarModel.objects.get_or_create(brand=brand, name=m_name)
            model_objs[f"{brand_name} {m_name}"] = model

    print(f"{len(brand_objs)} ta brend va modellar saqlandi.")

    # 3. Categories
    categories_data = [
        {
            'name': 'Moy va filtrlar',
            'icon': 'fa-oil-can',
            'desc': 'Sintetik motor moylari, transmissiya moylari, moy, havo va salon filtrlari.',
            'featured': True,
        },
        {
            'name': 'Tormoz tizimi',
            'icon': 'fa-compact-disc',
            'desc': 'Tormoz kolodkalari, disklar, tormoz suyuqliklari va shlanglari.',
            'featured': True,
        },
        {
            'name': 'Dvigatel qismlari',
            'icon': 'fa-gears',
            'desc': 'Svechalar, remenlar, roliklar, suv nasoslari (pompa) va qistirmalar.',
            'featured': True,
        },
        {
            'name': 'Elektronika & Aksessuarlar',
            'icon': 'fa-plug-circle-bolt',
            'desc': 'Videoregistratorlar, parktroniklar, LED lampalar, audio tizimlar.',
            'featured': True,
        },
        {
            'name': 'Akkumulyatorlar',
            'icon': 'fa-car-battery',
            'desc': 'Original AGM, EFB va standart avtomobil akkumulyatorlari.',
            'featured': True,
        },
        {
            'name': 'Podveska va amortizatorlar',
            'icon': 'fa-car-burst',
            'desc': 'Amortizatorlar, prujinalar, sharovoylar, saylentbloklar.',
            'featured': True,
        },
    ]

    cat_objs = {}
    for c_data in categories_data:
        cat, _ = Category.objects.get_or_create(
            name=c_data['name'],
            defaults={
                'icon': c_data['icon'],
                'description': c_data['desc'],
                'is_featured': c_data['featured'],
            }
        )
        cat_objs[c_data['name']] = cat

    print(f"{len(cat_objs)} ta toifa saqlandi.")

    # 4. Products
    products_data = [
        {
            'name': 'Shell Helix Ultra 5W-30 Motor Moyi (4L)',
            'category': 'Moy va filtrlar',
            'sku': 'SH-5W30-4L',
            'price': 420000,
            'old_price': 480000,
            'stock': 25,
            'manufacturer': 'Shell',
            'country': 'Germaniya',
            'warranty': '100% Original kafolati',
            'is_featured': True,
            'is_new': True,
            'description': 'PurePlus texnologiyasi asosida ishlab chiqarilgan to\'liq sintetik premium motor moyi. Dvigatelni maksimal darajada toza saqlaydi va yoqilg\'i sarfini tejaydi.',
            'models': ['Chevrolet Cobalt', 'Chevrolet Gentra / Lacetti', 'Chevrolet Tracker', 'Hyundai Elantra', 'Kia K5']
        },
        {
            'name': 'Mann-Filter W 67/2 Moy Filtri',
            'category': 'Moy va filtrlar',
            'sku': 'MANN-W672',
            'price': 75000,
            'old_price': 90000,
            'stock': 40,
            'manufacturer': 'Mann-Filter',
            'country': 'Germaniya',
            'warranty': '6 oy',
            'is_featured': True,
            'is_new': False,
            'description': 'Germaniyaning yetakchi brendidan yuqori aniqlikdagi tozalovchi moy filtri. Har qanday zararli zarrachalarni ushlab qoladi.',
            'models': ['Chevrolet Cobalt', 'Chevrolet Nexia 3', 'Chevrolet Onix']
        },
        {
            'name': 'Brembo Old Tormoz Kolodkalari (P 10 004)',
            'category': 'Tormoz tizimi',
            'sku': 'BRM-P10004',
            'price': 380000,
            'old_price': 440000,
            'stock': 15,
            'manufacturer': 'Brembo',
            'country': 'Italiya',
            'warranty': '12 oy',
            'is_featured': True,
            'is_new': True,
            'description': 'Italiya brendining yuqori samarali keramika tormoz kolodkalari. Qizib ketishga chidamli va tormozlanish masofasini qisqartiradi, shovqinsiz ishlaydi.',
            'models': ['Chevrolet Cobalt', 'Chevrolet Gentra / Lacetti']
        },
        {
            'name': 'Bosch S4 005 60Ah Akkumulyator',
            'category': 'Akkumulyatorlar',
            'sku': 'BSH-S4-60',
            'price': 890000,
            'old_price': 990000,
            'stock': 12,
            'manufacturer': 'Bosch',
            'country': 'Chexiya',
            'warranty': '18 oy',
            'is_featured': True,
            'is_new': False,
            'description': 'PowerFrame texnologiyasi bilan uzoq xizmat muddati va sovuq havoda dvigatelni ishonchli o\'t oldirish kafolati.',
            'models': ['Chevrolet Cobalt', 'Chevrolet Gentra / Lacetti', 'Kia Sportage', 'Hyundai Elantra']
        },
        {
            'name': '70mai A800S 4K Ultra Dash Cam Videoregistrator',
            'category': 'Elektronika & Aksessuarlar',
            'sku': '70M-A800S',
            'price': 1450000,
            'old_price': 1650000,
            'stock': 8,
            'manufacturer': '70mai (Xiaomi)',
            'country': 'Xitoy',
            'warranty': '12 oy',
            'is_featured': True,
            'is_new': True,
            'description': '4K UHD piksellar soni, o\'rnatilgan GPS, ADAS xavfsizlik tizimi va 24 soatlik to\'xtash joyi kuzatuv tizimi (Parking surveillance).',
            'models': ['Chevrolet Cobalt', 'Chevrolet Tracker', 'Chevrolet Malibu 2', 'BYD Song Plus', 'Kia K5']
        },
        {
            'name': 'NGK Laser Iridium Svechalari to\'plami (4 dona)',
            'category': 'Dvigatel qismlari',
            'sku': 'NGK-IZFR6K',
            'price': 320000,
            'old_price': 360000,
            'stock': 20,
            'manufacturer': 'NGK',
            'country': 'Yaponiya',
            'warranty': '100,000 km',
            'is_featured': False,
            'is_new': True,
            'description': 'Lazerli iridiy qoplamali elektrod. Kuchli uchqun, barqaror aylanishlar va yoqilg\'i tejamkorligi.',
            'models': ['Chevrolet Cobalt', 'Chevrolet Gentra / Lacetti', 'Chevrolet Nexia 3']
        },
        {
            'name': 'Kayaba (KYB) Old Amortizator (Excel-G)',
            'category': 'Podveska va amortizatorlar',
            'sku': 'KYB-333005',
            'price': 520000,
            'old_price': None,
            'stock': 14,
            'manufacturer': 'KYB (Kayaba)',
            'country': 'Yaponiya',
            'warranty': '12 oy',
            'is_featured': False,
            'is_new': True,
            'description': 'Ikki quvurli gaz-moyli amortizator. Har qanday yo\'l sharoitida yuqori boshqaruv va qulaylik beradi.',
            'models': ['Chevrolet Cobalt', 'Chevrolet Gentra / Lacetti']
        },
        {
            'name': 'Castrol EDGE 5W-40 To\'liq Sintetik Moy (4L)',
            'category': 'Moy va filtrlar',
            'sku': 'CAS-5W40-4L',
            'price': 460000,
            'old_price': 510000,
            'stock': 18,
            'manufacturer': 'Castrol',
            'country': 'Buyuk Britaniya',
            'warranty': '100% Original kafolati',
            'is_featured': True,
            'is_new': True,
            'description': 'Fluid TITANIUM texnologiyasi bilan dvigatel bosim ostida ishlaganda moy pardasini mustahkamlaydi va ishqalanishni 20% ga kamaytiradi.',
            'models': ['Chevrolet Tracker', 'Chevrolet Malibu 2', 'BMW 3 Series (G20)', 'Kia Sportage']
        },
    ]

    for p_info in products_data:
        cat = cat_objs.get(p_info['category'])
        prod, created = Product.objects.get_or_create(
            sku=p_info['sku'],
            defaults={
                'name': p_info['name'],
                'category': cat,
                'price': p_info['price'],
                'old_price': p_info['old_price'],
                'stock': p_info['stock'],
                'manufacturer': p_info['manufacturer'],
                'country': p_info['country'],
                'warranty': p_info['warranty'],
                'is_featured': p_info['is_featured'],
                'is_new': p_info['is_new'],
                'description': p_info['description'],
            }
        )
        # Compatible models qo'shish
        for m_name in p_info.get('models', []):
            if m_name in model_objs:
                prod.compatible_models.add(model_objs[m_name])

    print(f"{len(products_data)} ta mahsulot saqlandi!")
    print("Muvaffaqiyatli yakunlandi!")

if __name__ == '__main__':
    populate()
