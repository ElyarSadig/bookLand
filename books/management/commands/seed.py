from django.core.management.base import BaseCommand
from books.models import Language, Category, Book, Review, UserBook, UserBookmark, Comment, BookCategory
from users.models import Role, User, UserRole
from accounts.models import WalletAction, WalletActionType, Discount, UserDiscount
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Insert data into Languages
        Language.objects.bulk_create([
            Language(name='فارسی'),
            Language(name='انگلیسی'),
            Language(name='فرانسوی'),
            Language(name='آلمانی'),
            Language(name='ترکی استانبولی'),
            Language(name='اسپانیایی'),
            Language(name='ایتالیایی'),
            Language(name='روسی'),
            Language(name='چینی'),
            Language(name='ژاپنی'),
        ])

        # Insert data into Roles
        Role.objects.bulk_create([
            Role(role='Publisher', description='Publishes books on the platform'),
            Role(role='Customer', description='Buys and reviews books on the platform'),
        ])

        # Insert data into Categories
        Category.objects.bulk_create([
            Category(name='کمک درسی'),
            Category(name='داستانی'),
            Category(name='غیر داستانی'),
            Category(name='زندگینامه'),
            Category(name='طنز'),
            Category(name='رمان'),
            Category(name='کتاب آشپزی'),
            Category(name='هیجان انگیز'),
            Category(name='رازآلود'),
            Category(name='شعر'),
            Category(name='فلسفه'),
            Category(name='علمی-تخیلی'),
            Category(name='تاریخ'),
            Category(name='خودیاری'),
            Category(name='فانتزی'),
            Category(name='عاشقانه'),
        ])

        # Insert data into Users
        User.objects.bulk_create([
            User(
                username='Ali',
                email='alitaami2002@gmail.com',
                password=make_password("password"),
                is_active=True,
                is_publisher=False),

            User(username='Elyar',
                 email='ElyarNejati@gmail.com',
                 password=make_password("password"),
                 is_active=True,
                 is_publisher=False),

            User(username='AliTaami',
                 email='alitaami81@gmail.com',
                 password=make_password("password"),
                 is_active=True,
                 is_publisher=False),

            User(username="KheyliSabz",
                 email="kheylisabz@kheylisabz.com",
                 password=make_password("password"),
                 publications_name='انتشارات خیلی سبز',
                 is_confirm=True,
                 is_active=True,
                 is_publisher=True,
                 phone_number="09214491645",
                 identity_image="http://localhost:8080/identities/demo-1.jpg",
                 card_number="6104337457855984",
                 publications_image="http://localhost:8080/publications/demo-1.png"),

            User(username="AmirKabir",
                 email="AmirKabir@amirkabiruni.com",
                 password=make_password("password"),
                 publications_name='انتشارات امیر کبیر',
                 is_confirm=True,
                 is_active=True,
                 is_publisher=True,
                 phone_number="09214491746",
                 identity_image="http://localhost:8080/identities/demo-2.jpg",
                 card_number="6104337427855984",
                 publications_image="http://localhost:8080/publications/demo-2.png"),

            User(username="Sana",
                 email="sanapub@sanapublications.com",
                 password=make_password("password"),
                 publications_name='انتشارات سنا',
                 is_confirm=True,
                 is_active=True,
                 is_publisher=True,
                 phone_number="09214491849",
                 identity_image="http://localhost:8080/identities/demo-3.jpg",
                 card_number="6037997333763952",
                 publications_image="http://localhost:8080/publications/demo-3.png")
        ])

        # Insert data into UserRoles
        UserRole.objects.bulk_create([
            UserRole(user_id=1, role_id=2),
            UserRole(user_id=2, role_id=2),
            UserRole(user_id=3, role_id=2),
            UserRole(user_id=4, role_id=1),
            UserRole(user_id=5, role_id=1),
            UserRole(user_id=6, role_id=1),
        ])

        # Insert data into Books
        Book.objects.bulk_create([
            Book(
                publisher_id=4,
                name='پرسش‌های چهار گزینه‌ای فیزیک جامع - رشته ریاضی',
                author_name='شاهین اقبالی',
                translator_name=None,
                released_date=1400,
                book_cover_image='http://localhost:8080/book-covers/demo-1.jpg',
                price=115000,
                number_of_pages=350,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-1.pdf',
                original_file='http://localhost:8080/books/original-1.pdf',
                description='کتاب پرسش‌های چهار گزینه‌ای فیزیک جامع - رشته ریاضی، شامل تمام نکات و ایده‌های رایج تستی کنکور، درس‌نامه‌های جامع و کنکوری، بیش از 2600 تست سراسری و تألیفی به سبک کنکور جدید و پاسخ‌های تشریحی با روش‌ها و تکنیک‌های کاربردی است.'
            ),
            Book(
                publisher_id=4,
                name='پرسش‌های چهار گزینه‌ای شیمی 2 - پایه یازدهم',
                author_name='شاهین اقبالی',
                translator_name=None,
                released_date=1399,
                book_cover_image='http://localhost:8080/book-covers/demo-2.jpg',
                price=74000,
                number_of_pages=400,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-2.pdf',
                original_file='http://localhost:8080/books/original-2.pdf',
                description='کتاب پرسش‌های چهار گزینه‌ای شیمی 2 - پایه یازدهم نوشته‌ی نیما سپهری و مهدی براتی، دربردارنده‌ی درس‌نامه، تست‌های کنکوری و تألیفی و پاسخ‌های تشریحی و کلیدی است که به دانش‌آموزان کمک می‌کند این درس را بهتر یاد بگیرند و سؤالات و تمرینات درسی‌شان را راحت‌تر حل کنند. این کتاب ویژه‌ی دانش‌آموزان رشته‌های ریاضی و تجربی است.'
            ),
            Book(
                publisher_id=4,
                name='پرسش‌های چهار گزینه‌ای ریاضیات تجربی جامع: جلد دوم',
                author_name='شاهین اقبالی',
                translator_name=None,
                released_date=1402,
                book_cover_image='http://localhost:8080/book-covers/demo-3.jpg',
                price=143000,
                number_of_pages=554,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-3.pdf',
                original_file='http://localhost:8080/books/original-3.pdf',
                description='کتاب پرسش‌های چهار گزینه‌ای ریاضیات تجربی جامع - پاسخ - دهم، یازدهم، دوازدهم: جلد دوم، حاصل همکاری سروش موئینی، رسول محسنی منش و کوروش اسلامی است و پاسخنامه‌ی آزمون‌های جلد اول همین کتاب را در برمی‌گیرد. این پاسخنامه به صورت تشریحی و با راه‌حل‌های متنوع، مفصل و تکنیکی ارائه شده است.'
            ),
            Book(
                publisher_id=4,
                name='پرسش‌های چهار گزینه‌ای فارسی 1 - پایه دهم',
                author_name='ابوالفضل غلامی',
                translator_name=None,
                released_date=1400,
                book_cover_image='http://localhost:8080/book-covers/demo-4.jpg',
                price=52000,
                number_of_pages=300,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-4.pdf',
                original_file='http://localhost:8080/books/original-4.pdf',
                description='کتاب پرسش‌های چهار گزینه‌ای فارسی 1 - پایه دهم، مجموعه‌ای از درس‌نامه و سؤالات تستی، کادر آموزشی آرایه‌های ادبی، کادر آموزشی دستور زبان فارسی و پاسخ‌نامه‌ی تشریحی است.'
            ),
            Book(
                publisher_id=4,
                name='پرسش‌های چهار گزینه‌ای فارسی جامع - سوال - دهم، یازدهم و دوازدهم - جلد اول',
                author_name='ابوالفضل غلامی',
                translator_name=None,
                released_date=2019,
                book_cover_image='http://localhost:8080/book-covers/demo-5.jpg',
                price=120000,
                number_of_pages=500,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-5.pdf',
                original_file='http://localhost:8080/books/original-5.pdf',
                description='کتاب پرسش‌های چهار گزینه‌ای فارسی جامع - سوال - دهم، یازدهم و دوازدهم - جلد اول یک مجموعه‌ سوال کنکوری به‌همراه پاسخنامه‌ی کلیدی است که به تسلط شما بر مباحث درسی و قرار گرفتن در حال‌و‌هوای آزمون سراسری کمک می‌کند.'
            ),
            Book(
                publisher_id=5,
                name='نبرد من',
                author_name='آدولف هیتلر',
                translator_name='مهدی اکبر پور',
                released_date=1395,
                book_cover_image='http://localhost:8080/book-covers/demo-6.jpg',
                price=30000,
                number_of_pages=663,
                demo_file='http://localhost:8080/books/demo-6.pdf',
                original_file='http://localhost:8080/books/original-6.pdf',
                language_id=1,
                description='کتاب نبرد من تنها کتابی است که انتشار آن در آلمان ممنوع است. آدولف هیتلر در این کتاب دیدگاه‌های خود را بیان کرده، اثری که مبنای برپایی حزب ناسیونالیسم (نازی) شد و جهان را درگیر مصیبتی همه‌گیر کرد.'
            ),
            Book(
                publisher_id=5,
                name='با پیشوا تا ابد: خاطرات محافظ شخصی هیتلر',
                author_name='روخوس میش',
                translator_name='فرشته اکبر پور',
                released_date=1400,
                book_cover_image='http://localhost:8080/book-covers/demo-7.jpg',
                price=70000,
                number_of_pages=446,
                demo_file='http://localhost:8080/books/demo-7.pdf',
                original_file='http://localhost:8080/books/original-7.pdf',
                language_id=1,
                description='روخوس میش یکی از محافظین شخصی آدولف هیتلر، رهبر جنجالی حزب نازی، بود. او در کتاب با پیشوا تا ابد: خاطرات محافظ شخصی هیتلر، به روایت دوران کارش در سازمان نظامی اس اس پرداخته و از این طریق، برای نخستین بار ناگفته‌های بسیاری را در باب تشکیلات نازی‌ها بیان نموده است.'
            ),
            Book(
                publisher_id=5,
                name='کتاب A persian in London (یک ایرانی در لندن)',
                author_name='محمد افشاروالا',
                translator_name=None,
                released_date=1398,
                book_cover_image='http://localhost:8080/book-covers/demo-8.jpg',
                price=43000,
                number_of_pages=332,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-8.pdf',
                original_file='http://localhost:8080/books/original-8.pdf',
                description='کتاب A persian in London (یک ایرانی در لندن) به قلم محمد افشاروالا، اصطلاحات و واژگان مهم و کاربردی زبان انگلیسی را مورد بررسی قرار می‌دهد. تمرکز این کتاب بر روی فراگیری اصطلاحات بریتانیایی است.'
            ),
            Book(
                publisher_id=5,
                name='The Orange Girl',
                author_name='Jostein Gaarder',
                translator_name=None,
                released_date=2017,
                book_cover_image='http://localhost:8080/book-covers/demo-9.jpg',
                price=60000,
                number_of_pages=155,
                demo_file='http://localhost:8080/books/demo-9.pdf',
                original_file='http://localhost:8080/books/original-9.pdf',
                language_id=2,
                description='نویسنده‌ی کتاب پرفروش دنیای سوفی با یک کتاب پرخواستار دیگر بازگشته است. یوستین گردر در کتاب دختر پرتقالی داستان پسری پانزده‌ساله به نام «جرج» را روایت می‌کند که در کودکی پدر خود را از دست داده است. ماجرا از زمانی آغاز می‌شود که مجموعه‌ نامه‌هایی از پدر به دست جرج می‌رسند. گویی که این دست‌نوشته‌ها راهی تازه برای ارتباط برقرار کردن او با پدرش باشند... لازم به ذکر است بیش از چهل میلیون نسخه از کتاب حاضر در سرتاسر جهان به فروش رسیده است.'
            ),
            Book(
                publisher_id=6,
                name='The Egyptian',
                author_name='Mika Waltari',
                translator_name=None,
                released_date=1940,
                book_cover_image='http://localhost:8080/book-covers/demo-10.jpg',
                price=140000,
                number_of_pages=512,
                demo_file='http://localhost:8080/books/demo-10.pdf',
                original_file='http://localhost:8080/books/original-10.pdf',
                language_id=2,
                description='کتاب The Egyptian نوشته Mika Waltari در سال های بسیار دور نوشته شده است که بسیاری از وقایع و اتفاقاتی که روایت می گردد بر اساس داستانی واقعی می باشد. بیشتر اتفاقات کتاب به سال های فرمانروایی فراعنه در مصر می پردازد…'
            ),
            Book(
                publisher_id=6,
                name='کمال گرای مضطرب',
                author_name='مایکل پی توهیگ',
                translator_name='شقایق مختاری',
                released_date=1400,
                book_cover_image='http://localhost:8080/book-covers/demo-11.jpg',
                price=25000,
                number_of_pages=312,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-11.pdf',
                original_file='http://localhost:8080/books/original-11.pdf',
                description='عشق و خودشناسی در تقابل با یکدیگر! رافائل ژیوردانو خالق کتاب محبوب «زندگی دومت زمانی آغاز می‌شود که می‌فهمی فقط یک زندگی داری» این‌بار به سراغ موضوع تازه‌ای رفته است. داستان کتاب فرشته عشق بال‌های مقوایی دارد روایتی ماجراجویانه و هیجان‌انگیز درباره عشق و تلاش برای یافتن آن در زندگی و در میان روابط انسانی است.'
            ),
            Book(
                publisher_id=6,
                name='قدرت سکوت: قدرت درونگراها',
                author_name='سوزان کین',
                translator_name=None,
                released_date=1401,
                book_cover_image='http://localhost:8080/book-covers/demo-12.jpg',
                price=19900,
                number_of_pages=274,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-12.pdf',
                original_file='http://localhost:8080/books/original-12.pdf',
                description='کتاب در حسرت فرشته به قلم زهره زندیه، داستانی اجتماعی و جذاب و متعهد به ارزش‌‌‌های انسانی به شمار می‌رود که شما را با خود و احساسات بی‌آلایشتان آشتی می‌دهد. این کتاب روایتگر دردها و مشکلات بسیاری از افراد جامعه است که لحظات غیر قابل وصفی را برای شما رقم می‌زند.'
            ),
            Book(
                publisher_id=6,
                name='مناظره با شیطان',
                author_name='اصغر بهمنی',
                translator_name=None,
                released_date=1392,
                book_cover_image='http://localhost:8080/book-covers/demo-13.jpg',
                price=15900,
                number_of_pages=256,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-13.pdf',
                original_file='http://localhost:8080/books/original-13.pdf',
                description='کتاب مناظره با شیطان نوشته‌ی اصغر بهمنی، دستمایه‌ای است برای شناخت «ابلیس» و یا «رئیس شیاطین عالم» که در این اثر از آن به عنوان «شیطان» یاد می‌شود. در این کتاب، «انسان» عبارت است از یک آدمیزاد پاکدل و دشمن شناس.'
            ),
            Book(
                publisher_id=6,
                name='شیطان پرستی مدرن',
                author_name='اصغر بهمنی',
                translator_name=None,
                released_date=1388,
                book_cover_image='http://localhost:8080/book-covers/demo-14.jpg',
                price=18000,
                number_of_pages=112,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-14.pdf',
                original_file='http://localhost:8080/books/original-14.pdf',
                description='در کتاب شیطان پرستی مدرن، به تالیف حسین بابازاده مقدم، به یکی از جریان‌های فاسد فکری و فرهنگی که ابتدا مرزهای اخلاقیات را در کشورهای اروپایی و آمریکایی در هم شکسته و سپس به سرزمین‌های شرقی رسیده، پرداخته شده است.'
            ),
            Book(
                publisher_id=6,
                name='جهان، صفحه شطرنج سازمان‌های سری',
                author_name='منصور عبدالحکیم',
                translator_name='سید شاهپور حسینی',
                released_date=1398,
                book_cover_image='http://localhost:8080/book-covers/demo-15.jpg',
                price=21000,
                number_of_pages=272,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-15.pdf',
                original_file='http://localhost:8080/books/original-15.pdf',
                description='کتاب جهان، صفحه شطرنج سازمان‌های سری نوشته‌ی منصور عبدالحکیم، مورّخ، پژوهشگر و نویسنده صاحب نام مصری است. او در این اثر به بررسی نحوۀ پیدایش مجامع مخفی و انجمن فراماسونری، نحوۀ عملکرد و معرفی فرقه‌ها و گروه‌های نشئت گرفته از این انجمن و عملکرد این گروه‌ها و تأثیرشان در جهان پرداخته است.'
            ),
            Book(
                publisher_id=6,
                name='در حسرت فرشته',
                author_name='زهره زندیه',
                translator_name=None,
                released_date=1401,
                book_cover_image='http://localhost:8080/book-covers/demo-16.jpg',
                price=19900,
                number_of_pages=274,
                language_id=1,
                demo_file='http://localhost:8080/books/demo-16.pdf',
                original_file='http://localhost:8080/books/original-16.pdf',
                description='کتاب در حسرت فرشته به قلم زهره زندیه، داستانی اجتماعی و جذاب و متعهد به ارزش‌‌‌های انسانی به شمار می‌رود که شما را با خود و احساسات بی‌آلایشتان آشتی می‌دهد. این کتاب روایتگر دردها و مشکلات بسیاری از افراد جامعه است که لحظات غیر قابل وصفی را برای شما رقم می‌زند.'
            ),
        ])

        # Insert data into Reviews
        Review.objects.bulk_create([
            Review(user_id=2, book_id=12, rating=5, created_at='2023-01-10 10:00:00'),
            Review(user_id=2, book_id=11, rating=5, created_at='2023-01-15 14:00:00'),
            Review(user_id=2, book_id=13, rating=1, created_at='2023-01-16 10:00:00'),
            Review(user_id=2, book_id=7, rating=3, created_at='2023-01-16 10:00:00'),
            Review(user_id=1, book_id=7, rating=4, created_at='2023-01-17 11:00:00'),
            Review(user_id=1, book_id=5, rating=3, created_at='2023-01-18 12:00:00'),
        ])

        # Insert data into UserBooks
        UserBook.objects.bulk_create([
            UserBook(book_id=16, user_id=2, bought_time='2023-01-10 10:05:00'),
            UserBook(book_id=12, user_id=2, bought_time='2023-01-10 10:05:00'),
            UserBook(book_id=13, user_id=2, bought_time='2023-01-15 14:05:00'),
            UserBook(book_id=11, user_id=2, bought_time='2023-01-15 14:05:00'),
            UserBook(book_id=15, user_id=2, bought_time='2023-01-16 10:05:00'),
            UserBook(book_id=7, user_id=2, bought_time='2023-01-17 11:05:00'),
            UserBook(book_id=7, user_id=1, bought_time='2023-01-17 11:05:00'),
            UserBook(book_id=5, user_id=1, bought_time='2023-01-17 11:05:00'),
            UserBook(book_id=6, user_id=1, bought_time='2023-01-18 12:05:00'),
        ])

        # Insert data into UserBookmarks
        UserBookmark.objects.bulk_create([
            UserBookmark(book_id=16, user_id=2, added_time='2023-01-16 09:00:00', is_delete=False),
            UserBookmark(book_id=12, user_id=2, added_time='2023-01-16 09:00:00', is_delete=False),
            UserBookmark(book_id=13, user_id=2, added_time='2023-01-17 09:00:00', is_delete=False),
            UserBookmark(book_id=11, user_id=2, added_time='2023-01-18 09:00:00', is_delete=False),
            UserBookmark(book_id=15, user_id=2, added_time='2023-01-19 09:00:00', is_delete=False),
            UserBookmark(book_id=2, user_id=1, added_time='2023-01-19 09:00:00', is_delete=False),
            UserBookmark(book_id=1, user_id=1, added_time='2023-01-19 09:00:00', is_delete=False),
            UserBookmark(book_id=4, user_id=1, added_time='2023-01-19 09:00:00', is_delete=False),
            UserBookmark(book_id=5, user_id=1, added_time='2023-01-20 09:00:00', is_delete=False),
        ])

        # Insert data into Comments
        Comment.objects.bulk_create([
            Comment(book_id=11, user_id=2, comment='این کتاب را دوست داشتم! خیلی عالی بود!',
                    created_date='2023-01-10'),
            Comment(book_id=12, user_id=2, comment='هعپ انتطار خوبه...', created_date='2023-01-15'),
            Comment(book_id=15, user_id=2, comment='به سلیقه من نبود.', created_date='2023-01-18'),
            Comment(book_id=7, user_id=1, comment='خواندنی عالی!', created_date='2023-01-16'),
            Comment(book_id=6, user_id=1, comment='بسیار توصیه می‌شود!', created_date='2023-01-17'),
            Comment(book_id=5, user_id=1, comment='به سلیقه من نبود.', created_date='2023-01-18'),
        ])

        # Insert data into BookCategories
        BookCategory.objects.bulk_create([
            BookCategory(category_id=1, book_id=1),
            BookCategory(category_id=2, book_id=2),
            BookCategory(category_id=4, book_id=3),
            BookCategory(category_id=7, book_id=4),
            BookCategory(category_id=6, book_id=5),
            BookCategory(category_id=2, book_id=6),
            BookCategory(category_id=8, book_id=7),
            BookCategory(category_id=7, book_id=8),
            BookCategory(category_id=1, book_id=9),
            BookCategory(category_id=2, book_id=10),
            BookCategory(category_id=16, book_id=11),
            BookCategory(category_id=16, book_id=10),
            BookCategory(category_id=8, book_id=13),
            BookCategory(category_id=5, book_id=14),
            BookCategory(category_id=3, book_id=15),
        ])

        # Seed data for WalletActionTypes
        WalletActionType.objects.bulk_create([
            WalletActionType(action_type='واریز'),
            WalletActionType(action_type='برداشت'),
        ])

        # Seed data for WalletAction
        WalletAction.objects.bulk_create([
            WalletAction(action_type_id=1, user_id=1, amount=30000, is_successful=True, description='شارژ ۳۰۰۰۰ تومان',
                         created_date='2023-01-09'),
            WalletAction(action_type_id=2, user_id=1, amount=30000, is_successful=True, description='خرید کتاب نبرد من',
                         created_date='2023-01-10'),
            WalletAction(action_type_id=1, user_id=1, amount=50000, is_successful=True, description='شارژ ۵۰۰۰۰ تومان',
                         created_date='2023-01-15'),
            WalletAction(action_type_id=2, user_id=2, amount=25000, is_successful=True,
                         description='خرید فرشته عشق بال های مقوایی دارد', created_date='2023-01-15'),
            WalletAction(action_type_id=1, user_id=2, amount=44900, is_successful=True, description='شارژ ۴۴۹۰۰',
                         created_date='2023-01-14'),
            WalletAction(action_type_id=2, user_id=2, amount=19900, is_successful=True,
                         description='خرید در حسرت فرشته', created_date='2023-01-16'),
        ])

        # Seed data for Discounts
        Discount.objects.bulk_create([
            Discount(code='welcome', quantity=10000, percent=30.00, created_date='2023-01-01', expire_date='2030-12-31',
                     is_delete=False),
            Discount(code='DISCOUNT10', quantity=100, percent=10.00, created_date='2023-01-01',
                     expire_date='2023-12-31', is_delete=False),
            Discount(code='DISCOUNT15', quantity=50, percent=15.00, created_date='2023-01-01', expire_date='2023-06-30',
                     is_delete=False),
            Discount(code='DISCOUNT20', quantity=75, percent=20.00, created_date='2023-01-01', expire_date='2023-12-31',
                     is_delete=False),
        ])

        # Seed data for UserDiscounts
        UserDiscount.objects.bulk_create([
            UserDiscount(user_id=1, discount_id=1),
            UserDiscount(user_id=2, discount_id=2),
            UserDiscount(user_id=2, discount_id=3),
        ])

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))