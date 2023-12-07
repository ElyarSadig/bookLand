-- User table
CREATE TABLE Users (
    Id SERIAL PRIMARY KEY,
    Username VARCHAR(255) UNIQUE,
    Email VARCHAR(255) UNIQUE,
    HashedPassword VARCHAR(255) NOT NULL,
    Salt VARCHAR(255) NOT NULL,
    IsActive BOOLEAN NOT NULL,
    RegistrationDate TIMESTAMP NOT NULL,
    LastLoginDate TIMESTAMP,
    IsPublisher BOOLEAN NOT NULL,
    PhoneNumber VARCHAR(11) UNIQUE,
    PhoneNumber2 VARCHAR(11),
    Address TEXT,
    IdentityImage VARCHAR(255),
    CardNumber VARCHAR(50),
    PublicationsName VARCHAR(255) UNIQUE,
    PublicationsImage VARCHAR(255),
    IsConfirm BOOLEAN NOT NULL
);

CREATE TABLE UserActivityCodes (
    Id SERIAL PRIMARY KEY,
    Email VARCHAR(255),
    ActivationCode VARCHAR(6),
    CreatedDateTime TIMESTAMP,
    ExpireDateTime TIMESTAMP
);

-- Role table
CREATE TABLE Roles (
    Id SERIAL PRIMARY KEY,
    Role VARCHAR(50) UNIQUE,
    Description TEXT
);

-- UserRole table
CREATE TABLE UserRoles (
    Id SERIAL PRIMARY KEY,
    UserId INTEGER REFERENCES Users(Id),
    RoleId INTEGER REFERENCES Roles(Id),
    UNIQUE(UserId, RoleId)
);

-- Language table
CREATE TABLE Languages (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(50) UNIQUE
);

-- Book table
CREATE TABLE Books (
    Id SERIAL PRIMARY KEY,
    UserId INTEGER REFERENCES Users(Id),      -- Publisher
    BookName VARCHAR(255) NOT NULL,
    AuthorName VARCHAR(255) NOT NULL,
    TranslatorName VARCHAR(255),
    ReleasedDate INTEGER NOT NULL,
    BookCoverImage VARCHAR(255),
    Price DECIMAL(10,2) NOT NULL,
    Description TEXT,
    NumberOfPages INTEGER,
    LanguageId INTEGER REFERENCES Languages(Id),
    IsDelete BOOLEAN NOT NULL
);

-- Review table
CREATE TABLE Reviews (
    Id SERIAL PRIMARY KEY,
    UserId INTEGER REFERENCES Users(Id),
    BookId INTEGER REFERENCES Books(Id),
    Rating INTEGER CHECK (Rating BETWEEN 1 AND 5),
    CreatedAt TIMESTAMP
);

-- BookFiles table
CREATE TABLE BookFiles (
    Id SERIAL PRIMARY KEY,
    BookId INTEGER REFERENCES Books(Id),
    BookDemoFile VARCHAR(255),
    BookOriginalFile VARCHAR(255)
);

-- UserBooks table
CREATE TABLE UserBooks (
    Id SERIAL PRIMARY KEY,
    BookId INTEGER REFERENCES Books(Id),
    UserId INTEGER REFERENCES Users(Id),
    BoughtTime TIMESTAMP
);

-- UserBookmarks table
CREATE TABLE UserBookmarks (
    Id SERIAL PRIMARY KEY,
    BookId INTEGER REFERENCES Books(Id),
    UserId INTEGER REFERENCES Users(Id),
    AddedTime TIMESTAMP,
    IsDelete BOOLEAN,
    CONSTRAINT unique_user_bookmark UNIQUE (UserId, BookId)
);

-- Comments table
CREATE TABLE Comments (
    Id SERIAL PRIMARY KEY,
    BookId INTEGER REFERENCES Books(Id),
    UserId INTEGER REFERENCES Users(Id),
    Comment TEXT,
    IsDelete BOOLEAN,
    CreatedDate TIMESTAMP
);

-- Category table
CREATE TABLE Categories (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(255) UNIQUE
);

-- BookCategory table
CREATE TABLE BookCategories (
    Id SERIAL PRIMARY KEY,
    CategoryId INTEGER REFERENCES Categories(Id),
    BookId INTEGER REFERENCES Books(Id),
    IsDelete BOOLEAN
);

-- WalletActionType table
CREATE TABLE WalletActionTypes (
    Id SERIAL PRIMARY KEY,
    ActionType VARCHAR(255) UNIQUE
);

-- WalletAction table
CREATE TABLE WalletActions (
    Id SERIAL PRIMARY KEY,
    ActionTypeId INTEGER REFERENCES WalletActionTypes(Id),
    UserId INTEGER REFERENCES Users(Id),
    Amount DECIMAL(10,2),
    IsSuccessful BOOLEAN,
    Description TEXT,
    CreatedDate TIMESTAMP
);

-- Discount table
CREATE TABLE Discounts (
    Id SERIAL PRIMARY KEY,
    Code VARCHAR(255) UNIQUE,
    Quantity INTEGER,
    Percent DECIMAL(4,2),
    CreatedDate TIMESTAMP,
    ExpireDate TIMESTAMP,
    IsDelete BOOLEAN
);

-- UserDiscounts table
CREATE TABLE UserDiscounts (
    Id SERIAL PRIMARY KEY,
    UserId INTEGER REFERENCES Users(Id),
    DiscountId INTEGER REFERENCES Discounts(Id)
);
 -- Insert data into Language
INSERT INTO Languages (Name) VALUES
('فارسی'),    -- Persian
('انگلیسی'),  -- English
('فرانسوی'),  -- French
('آلمانی'),   -- German
('ترکی استانبولی'), -- Turkish
('اسپانیایی'), -- Spanish
('ایتالیایی'), -- Italian
('روسی'),     -- Russian
('چینی'),     -- Chinese
('ژاپنی');    -- Japanese

-- Insert data into Role
INSERT INTO Roles (Role, Description) VALUES
('Publisher', 'Publishes books on the platform'),           -- 1
('Customer', 'Buys and reviews books on the platform');     -- 2

-- Insert data into Category
INSERT INTO Categories (Name) VALUES
('کمک درسی'),         -- 1
('داستانی'),          -- 2
('غیر داستانی'),      -- 3
('زندگینامه'),        -- 4
('طنز'),              -- 5
('رمان'),             -- 6
('کتاب آشپزی'),       -- 7
('هیجان انگیز'),      -- 8
('رازآلود'),          -- 9
('شعر'),              -- 10
('فلسفه'),            -- 11
('علمی-تخیلی'),       -- 12
('تاریخ'),            -- 13
('خودیاری'),          -- 14
('فانتزی'),           -- 15
('عاشقانه');          -- 16

-- Insert data into Users
INSERT INTO Users (Username, Email, HashedPassword, Salt, IsActive, RegistrationDate, IsPublisher, IsConfirm)
VALUES
('Ali', 'alitaami2002@gmail.com', '6733b7ffeace4887c3b31258079c780d8db3018db9cbc05c500df3521f968df8', 'abc', TRUE, '2023-01-01', FALSE, TRUE),
('Elyar', 'ElyarNejati@gmail.com', '478a7da128a2875a1484798da2010d8f518ab4f341000da93c59fc5c201ded2c','def', TRUE, '2023-01-02', FALSE, TRUE),
('AliTaami', 'alitaami81@gmail.com', '59a1ea0e7b558df84d247db20315c9e4b9bff7719ffaafd3150a3c529aa38d98', 'ghi', TRUE, '2023-01-03', FALSE, TRUE);


-- Insert data into Users Publishers
INSERT INTO Users (Username, Email, HashedPassword, Salt, IsActive, RegistrationDate, IsPublisher, IsConfirm, PhoneNumber, IdentityImage, CardNumber, PublicationsImage, PublicationsName)
VALUES
('KheyliSabz', 'kheylisabz@kheylisabz.com', 'b77e3c94b3fbc99f22771482363dc0ea731113fb184e655d2ec9461e1c68519b', 'jkl', TRUE, '2023-01-04', TRUE, TRUE, '09214491645', 'http://localhost:8080/identities/demo-1.jpg', '6104337457855984', 'http://localhost:8080/publications/demo-1.png', 'انتشارات خیلی سبز'),      --publisher
('AmirKabir', 'AmirKabir@amirkabiruni.com', 'ebbf75fd13baaab8ce25b1d576efd9d071f8e95b8e8024035bb027a45604651e', 'mno', TRUE, '2023-01-05', TRUE, TRUE, '09214491746', 'http://localhost:8080/identities/demo-2.jpg', '6104337427855984', 'http://localhost:8080/publications/demo-2.jpg', 'انتشارات امیر کبیر'),     --publisher
('Sana', 'sanapub@sanapublications.com', '5d6e996d4ef01c66b299460b84d470c585ac813064ce1b5616dbfb738e232d38', 'pqr', TRUE, '2023-01-06', TRUE, TRUE, '09214491849', 'http://localhost:8080/identities/demo-3.jpg', '6037997333763952', 'http://localhost:8080/publications/demo-3.png', 'انتشارات سنا');              --publisher


-- Insert data into UserRole
INSERT INTO UserRoles (UserId, RoleId)
VALUES
(1, 2), -- Ali is a Customer
(2, 2), -- Elyar is a Customer
(3, 2), -- AliTaami is a Customer
(4, 1), -- KheyliSabz is a Publisher
(5, 1), -- AmirKabir is a Publisher
(6, 1); -- Sana is a Publisher


-- Insert data into Book here UserId is actually publisher's id
INSERT INTO Books (UserId, BookName, AuthorName, TranslatorName ,ReleasedDate, BookCoverImage, Price, NumberOfPages, LanguageId, IsDelete, Description)
VALUES
(4, 'پرسش‌های چهار گزینه‌ای فیزیک جامع - رشته ریاضی', 'شاهین اقبالی', NULL, 1400, 'http://localhost:8080/book-covers/demo-1.jpg' ,115000, 350, 1, FALSE, 'کتاب پرسش‌های چهار گزینه‌ای فیزیک جامع - رشته ریاضی، شامل تمام نکات و ایده‌های رایج تستی کنکور، درس‌نامه‌های جامع و کنکوری، بیش از 2600 تست سراسری و تألیفی به سبک کنکور جدید و پاسخ‌های تشریحی با روش‌ها و تکنیک‌های کاربردی است.'),
(4, ' پرسش‌های چهار گزینه‌ای شیمی 2 - پایه یازدهم', 'شاهین اقبالی', NULL, 1399, 'http://localhost:8080/book-covers/demo-2.jpg', 74000 , 400, 1, FALSE, 'کتاب پرسش‌های چهار گزینه‌ای شیمی 2 - پایه یازدهم نوشته‌ی نیما سپهری و مهدی براتی، دربردارنده‌ی درس‌نامه، تست‌های کنکوری و تألیفی و پاسخ‌های تشریحی و کلیدی است که به دانش‌آموزان کمک می‌کند این درس را بهتر یاد بگیرند و سؤالات و تمرینات درسی‌شان را راحت‌تر حل کنند. این کتاب ویژه‌ی دانش‌آموزان رشته‌های ریاضی و تجربی است.'),
(4, 'پرسش‌های چهار گزینه‌ای ریاضیات تجربی جامع: جلد دوم', 'شاهین اقبالی', NULL,1402, 'http://localhost:8080/book-covers/demo-3.jpg',143000, 554, 1, FALSE, 'کتاب پرسش‌های چهار گزینه‌ای ریاضیات تجربی جامع - پاسخ - دهم، یازدهم، دوازدهم: جلد دوم، حاصل همکاری سروش موئینی، رسول محسنی منش و کوروش اسلامی است و پاسخنامه‌ی آزمون‌های جلد اول همین کتاب را در برمی‌گیرد. این پاسخنامه به صورت تشریحی و با راه‌حل‌های متنوع، مفصل و تکنیکی ارائه شده است.'),
(4, ' پرسش‌های چهار گزینه‌ای فارسی 1 - پایه دهم', 'ابوالفضل غلامی',NULL ,1400,'http://localhost:8080/book-covers/demo-4.jpg',52000, 300, 1, FALSE, 'کتاب پرسش‌های چهار گزینه‌ای فارسی 1 - پایه دهم، مجموعه‌ای از درس‌نامه و سؤالات تستی، کادر آموزشی آرایه‌های ادبی، کادر آموزشی دستور زبان فارسی و پاسخ‌نامه‌ی تشریحی است.'),
(4, 'پرسش‌های چهار گزینه‌ای فارسی جامع - سوال - دهم، یازدهم و دوازدهم - جلد اول', 'ابوالفضل غلامی',NULL ,2019, 'http://localhost:8080/book-covers/demo-5.jpg' ,120000, 500, 1, FALSE, 'کتاب پرسش‌های چهار گزینه‌ای فارسی جامع - سوال - دهم، یازدهم و دوازدهم - جلد اول یک مجموعه‌ سوال کنکوری به‌همراه پاسخنامه‌ی کلیدی است که به تسلط شما بر مباحث درسی و قرار گرفتن در حال‌و‌هوای آزمون سراسری کمک می‌کند.'),
(5, 'نبرد من', 'آدولف هیتلر' , 'فرشته اکبر پور', 1395, 'http://localhost:8080/book-covers/demo-6.jpg' ,30000, 663, 1, FALSE, 'کتاب نبرد من تنها کتابی است که انتشار آن در آلمان ممنوع است. آدولف هیتلر در این کتاب دیدگاه‌های خود را بیان کرده، اثری که مبنای برپایی حزب ناسیونالیسم (نازی) شد و جهان را درگیر مصیبتی همه‌گیر کرد.'),
(5, 'با پیشوا تا ابد: خاطرات محافظ شخصی هیتلر', 'روخوس میش', 'فرشته اکبر پور' ,1400, 'http://localhost:8080/book-covers/demo-7.jpg', 70000, 446, 1, FALSE, 'روخوس میش یکی از محافظین شخصی آدولف هیتلر، رهبر جنجالی حزب نازی، بود. او در کتاب با پیشوا تا ابد: خاطرات محافظ شخصی هیتلر، به روایت دوران کارش در سازمان نظامی اس اس پرداخته و از این طریق، برای نخستین بار ناگفته‌های بسیاری را در باب تشکیلات نازی‌ها بیان نموده است.'),
(5, 'کتاب A persian in London (یک ایرانی در لندن)', 'محمد افشاروالا', NULL, 1398, 'http://localhost:8080/book-covers/demo-8.jpg', 43000, 332, 1, FALSE, 'کتاب A persian in London (یک ایرانی در لندن) به قلم محمد افشاروالا، اصطلاحات و واژگان مهم و کاربردی زبان انگلیسی را مورد بررسی قرار می‌دهد. تمرکز این کتاب بر روی فراگیری اصطلاحات بریتانیایی است.'),
(5, 'The Orange Girl', 'Jostein Gaarder', NULL, 2017, 'http://localhost:8080/book-covers/demo-9.jpg', 60000, 155, 2, FALSE, 'نویسنده‌ی کتاب پرفروش دنیای سوفی با یک کتاب پرخواستار دیگر بازگشته است. یوستین گردر در کتاب دختر پرتقالی داستان پسری پانزده‌ساله به نام «جرج» را روایت می‌کند که در کودکی پدر خود را از دست داده است. ماجرا از زمانی آغاز می‌شود که مجموعه‌ نامه‌هایی از پدر به دست جرج می‌رسند. گویی که این دست‌نوشته‌ها راهی تازه برای ارتباط برقرار کردن او با پدرش باشند... لازم به ذکر است بیش از چهل میلیون نسخه از کتاب حاضر در سرتاسر جهان به فروش رسیده است.'),
(6, 'The Egyptian', 'Mika Waltari', NULL, 1940, 'http://localhost:8080/book-covers/demo-10.jpg', 140000, 512, 2, FALSE, 'کتاب The Egyptian نوشته Mika Waltari در سال های بسیار دور نوشته شده است که بسیاری از وقایع و اتفاقاتی که روایت می گردد بر اساس داستانی واقعی می باشد. بیشتر اتفاقات کتاب به سال های فرمانروایی فراعنه در مصر می پردازد…'),
(6, 'فرشته عشق بال‌های مقوایی دارد', 'رافائل ژیوردانو', 'شقایق مختاری', 1400, 'http://localhost:8080/book-covers/demo-11.jpg', 25000, 312, 1, FALSE, 'عشق و خودشناسی در تقابل با یکدیگر! رافائل ژیوردانو خالق کتاب محبوب «زندگی دومت زمانی آغاز می‌شود که می‌فهمی فقط یک زندگی داری» این‌بار به سراغ موضوع تازه‌ای رفته است. داستان کتاب فرشته عشق بال‌های مقوایی دارد روایتی ماجراجویانه و هیجان‌انگیز درباره عشق و تلاش برای یافتن آن در زندگی و در میان روابط انسانی است.'),
(6, 'در حسرت فرشته', 'زهره زندیه', NULL, 1401, 'http://localhost:8080/book-covers/demo-12.jpg', 19900, 274, 1, FALSE, 'کتاب در حسرت فرشته به قلم زهره زندیه، داستانی اجتماعی و جذاب و متعهد به ارزش‌‌‌های انسانی به شمار می‌رود که شما را با خود و احساسات بی‌آلایشتان آشتی می‌دهد. این کتاب روایتگر دردها و مشکلات بسیاری از افراد جامعه است که لحظات غیر قابل وصفی را برای شما رقم می‌زند.'),
(6, 'مناظره با شیطان', 'اصغر بهمنی', NULL, 1392, 'http://localhost:8080/book-covers/demo-13.jpg', 15900, 256, 1, FALSE, 'کتاب مناظره با شیطان نوشته‌ی اصغر بهمنی، دستمایه‌ای است برای شناخت «ابلیس» و یا «رئیس شیاطین عالم» که در این اثر از آن به عنوان «شیطان» یاد می‌شود. در این کتاب، «انسان» عبارت است از یک آدمیزاد پاکدل و دشمن شناس.'),
(6, 'شیطان پرستی مدرن', 'اصغر بهمنی', NULL, 1388, 'http://localhost:8080/book-covers/demo-14.jpg', 18000, 112, 1, FALSE, 'در کتاب شیطان پرستی مدرن، به تالیف حسین بابازاده مقدم، به یکی از جریان‌های فاسد فکری و فرهنگی که ابتدا مرزهای اخلاقیات را در کشورهای اروپایی و آمریکایی در هم شکسته و سپس به سرزمین‌های شرقی رسیده، پرداخته شده است.'),
(6, 'جهان، صفحه شطرنج سازمان‌های سری', 'منصور عبدالحکیم', 'سید شاهپور حسینی', 1398, 'http://localhost:8080/book-covers/demo-15.jpg', 21000, 272, 1, FALSE, 'کتاب جهان، صفحه شطرنج سازمان‌های سری نوشته‌ی منصور عبدالحکیم، مورّخ، پژوهشگر و نویسنده صاحب نام مصری است. او در این اثر به بررسی نحوۀ پیدایش مجامع مخفی و انجمن فراماسونری، نحوۀ عملکرد و معرفی فرقه‌ها و گروه‌های نشئت گرفته از این انجمن و عملکرد این گروه‌ها و تأثیرشان در جهان پرداخته است.');

-- Insert data into Review
INSERT INTO Reviews (UserId, BookId, Rating, CreatedAt)
VALUES
(2, 12, 5, '2023-01-10 10:00:00'),
(2, 11, 5, '2023-01-15 14:00:00'),
(2, 13, 1, '2023-01-16 10:00:00'),
(2, 7, 3, '2023-01-16 10:00:00'),
(1, 7, 4, '2023-01-17 11:00:00'),
(1, 5, 3, '2023-01-18 12:00:00');

-- Insert data into BookFiles
INSERT INTO BookFiles (BookId, BookDemoFile, BookOriginalFile)
VALUES
(1, 'path_to_demo_file1', 'path_to_original_file1'),
(2, 'path_to_demo_file2', 'path_to_original_file2'),
(3, 'path_to_demo_file3', 'path_to_original_file3'),
(4, 'path_to_demo_file4', 'path_to_original_file4'),
(5, 'path_to_demo_file5', 'path_to_original_file5'),
(6, 'path_to_demo_file5', 'path_to_original_file5'),
(7, 'path_to_demo_file5', 'path_to_original_file5'),
(8, 'path_to_demo_file5', 'path_to_original_file5'),
(9, 'path_to_demo_file5', 'path_to_original_file5'),
(10, 'path_to_demo_file5', 'path_to_original_file5'),
(11, 'path_to_demo_file5', 'path_to_original_file5'),
(12, 'path_to_demo_file5', 'path_to_original_file5'),
(13, 'path_to_demo_file5', 'path_to_original_file5'),
(14, 'path_to_demo_file5', 'path_to_original_file5'),
(15, 'path_to_demo_file5', 'path_to_original_file5');

-- Insert data into UserBooks
INSERT INTO UserBooks (BookId, UserId, BoughtTime)
VALUES
(12, 2, '2023-01-10 10:05:00'),
(13, 2, '2023-01-15 14:05:00'),
(11, 2, '2023-01-15 14:05:00'),
(15, 2, '2023-01-16 10:05:00'),
(7, 2, '2023-01-17 11:05:00'),
(7, 1, '2023-01-17 11:05:00'),
(5, 1, '2023-01-17 11:05:00'),
(6, 1, '2023-01-18 12:05:00');

-- Insert data into UserBookmarks
INSERT INTO UserBookmarks (BookId, UserId, AddedTime, IsDelete)
VALUES
(12, 2, '2023-01-16 09:00:00', FALSE),
(13, 2, '2023-01-17 09:00:00', FALSE),
(11, 2, '2023-01-18 09:00:00', FALSE),
(15, 2, '2023-01-19 09:00:00', FALSE),
(2, 1, '2023-01-19 09:00:00', FALSE),
(1, 1, '2023-01-19 09:00:00', FALSE),
(4, 1, '2023-01-19 09:00:00', FALSE),
(5, 1, '2023-01-20 09:00:00', FALSE);

-- Insert data into Comments
INSERT INTO Comments (BookId, UserId, Comment, IsDelete, CreatedDate)
VALUES
(11, 2, 'این کتاب را دوست داشتم! خیلی عالی بود!', FALSE, '2023-01-10'),
(12, 2, 'هعپ انتطار خوبه...', FALSE, '2023-01-15'),
(15, 2, 'به سلیقه من نبود.', FALSE, '2023-01-18'),
(7, 1, 'خواندنی عالی!', FALSE, '2023-01-16'),
(6, 1, 'بسیار توصیه می‌شود!', FALSE, '2023-01-17'),
(5, 1, 'به سلیقه من نبود.', FALSE, '2023-01-18');

-- Insert data into BookCategory
INSERT INTO BookCategories (CategoryId, BookId, IsDelete)
VALUES
(1, 1, FALSE),
(2, 2, FALSE),
(4, 3, FALSE),
(7, 4, FALSE),
(6, 5, FALSE),
(2, 6, FALSE),
(8, 7, FALSE),
(7, 8, FALSE),
(1, 9, FALSE),
(2, 10, FALSE),
(16, 11, FALSE),
(16, 12, FALSE),
(8, 13, FALSE),
(5, 14, FALSE),
(3, 15, FALSE);

-- Insert data into WalletActionType
INSERT INTO WalletActionTypes (ActionType)
VALUES
('واریز'),
('برداشت');

-- Insert data into WalletAction
INSERT INTO WalletActions (ActionTypeId, UserId, Amount, IsSuccessful, Description, CreatedDate)
VALUES
(1, 1, 30000, TRUE, 'شارژ ۳۰۰۰۰ تومان', '2023-01-09'),
(2, 1, 30000, TRUE, 'خرید کتاب نبرد من', '2023-01-10'),
(1, 1, 50000, TRUE, 'شارژ ۵۰۰۰۰ تومان', '2023-01-15'),
(2, 2, 25000, TRUE, 'خرید فرشته عشق بال های مقوایی دارد', '2023-01-15'),
(1, 2, 44900, TRUE, 'شارژ ۴۴۹۰۰', '2023-01-14'),
(2, 2, 19900, TRUE, 'خرید در حسرت فرشته', '2023-01-16');

-- Insert data into Discount
INSERT INTO Discounts (Code, Quantity, Percent, CreatedDate, ExpireDate, IsDelete)
VALUES
('welcome', 10000, 30.00, '2023-01-01', '2030-12-31', FALSE),
('DISCOUNT10', 100, 10.00, '2023-01-01', '2023-12-31', FALSE),
('DISCOUNT15', 50, 15.00, '2023-01-01', '2023-06-30', FALSE),
('DISCOUNT20', 75, 20.00, '2023-01-01', '2023-12-31', FALSE);

-- Insert data into UserDiscounts
INSERT INTO UserDiscounts (UserId, DiscountId)
VALUES
(1, 1),
(2, 2),
(2, 3);
