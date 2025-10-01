import React, { createContext, useContext, useState, useEffect } from 'react'

const LanguageContext = createContext()

export const useLanguage = () => {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}

// Translation data
const translations = {
  ar: {
    // Navigation
    home: 'الرئيسية',
    auctions: 'المزادات',
    categories: 'الفئات',
    about: 'حول مزاد',
    contact: 'اتصل بنا',
    login: 'تسجيل الدخول',
    register: 'إنشاء حساب',
    profile: 'الملف الشخصي',
    logout: 'تسجيل الخروج',
    
    // Hero Section
    heroTitle: 'مرحباً بك في مزاد',
    heroSubtitle: 'منصة المزادات الإلكترونية الرائدة في الكويت',
    heroDescription: 'اكتشف وزايد على آلاف السلع المميزة من التجار المعتمدين',
    startBidding: 'ابدأ المزايدة',
    browseAuctions: 'تصفح المزادات',
    
    // Featured Auctions
    featuredAuctions: 'المزادات المميزة',
    liveAuctions: 'المزادات المباشرة',
    endingSoon: 'ينتهي قريباً',
    currentBid: 'المزايدة الحالية',
    timeLeft: 'الوقت المتبقي',
    placeBid: 'ضع مزايدتك',
    viewDetails: 'عرض التفاصيل',
    
    // Categories
    categoriesTitle: 'تصفح حسب الفئة',
    electronics: 'إلكترونيات',
    jewelry: 'مجوهرات',
    cars: 'سيارات',
    furniture: 'أثاث',
    fashion: 'أزياء',
    collectibles: 'مقتنيات',
    
    // How It Works
    howItWorksTitle: 'كيف يعمل مزاد؟',
    step1Title: 'سجل حسابك',
    step1Description: 'أنشئ حساباً مجانياً وأكمل عملية التحقق',
    step2Title: 'تصفح المزادات',
    step2Description: 'اكتشف آلاف السلع المعروضة في مزادات مباشرة',
    step3Title: 'ضع مزايدتك',
    step3Description: 'زايد على السلع التي تعجبك واربح المزاد',
    step4Title: 'اربح واستلم',
    step4Description: 'ادفع واستلم سلعتك بأمان تام',
    
    // Auction Details
    auctionDetails: 'تفاصيل المزاد',
    description: 'الوصف',
    condition: 'الحالة',
    startingPrice: 'السعر المبدئي',
    reservePrice: 'السعر الاحتياطي',
    bidHistory: 'تاريخ المزايدات',
    seller: 'البائع',
    shippingInfo: 'معلومات الشحن',
    
    // Bidding
    yourBid: 'مزايدتك',
    minimumBid: 'أقل مزايدة',
    bidAmount: 'مبلغ المزايدة',
    confirmBid: 'تأكيد المزايدة',
    bidPlaced: 'تم وضع مزايدتك بنجاح',
    outbid: 'تم تجاوز مزايدتك',
    auctionWon: 'مبروك! لقد ربحت المزاد',
    
    // Profile
    myProfile: 'ملفي الشخصي',
    myBids: 'مزايداتي',
    wonAuctions: 'المزادات المكسوبة',
    watchlist: 'قائمة المتابعة',
    settings: 'الإعدادات',
    
    // Forms
    email: 'البريد الإلكتروني',
    password: 'كلمة المرور',
    confirmPassword: 'تأكيد كلمة المرور',
    fullName: 'الاسم الكامل',
    phoneNumber: 'رقم الهاتف',
    submit: 'إرسال',
    cancel: 'إلغاء',
    save: 'حفظ',
    
    // Status
    active: 'نشط',
    ended: 'منتهي',
    upcoming: 'قادم',
    won: 'مكسوب',
    lost: 'مفقود',
    
    // Time
    days: 'أيام',
    hours: 'ساعات',
    minutes: 'دقائق',
    seconds: 'ثواني',
    
    // Footer
    aboutUs: 'من نحن',
    privacyPolicy: 'سياسة الخصوصية',
    termsOfService: 'شروط الخدمة',
    support: 'الدعم',
    followUs: 'تابعنا',
    allRightsReserved: 'جميع الحقوق محفوظة'
  },
  
  en: {
    // Navigation
    home: 'Home',
    auctions: 'Auctions',
    categories: 'Categories',
    about: 'About Mzadd',
    contact: 'Contact Us',
    login: 'Login',
    register: 'Register',
    profile: 'Profile',
    logout: 'Logout',
    
    // Hero Section
    heroTitle: 'Welcome to Mzadd',
    heroSubtitle: 'Kuwait\'s Leading Online Auction Platform',
    heroDescription: 'Discover and bid on thousands of premium items from verified merchants',
    startBidding: 'Start Bidding',
    browseAuctions: 'Browse Auctions',
    
    // Featured Auctions
    featuredAuctions: 'Featured Auctions',
    liveAuctions: 'Live Auctions',
    endingSoon: 'Ending Soon',
    currentBid: 'Current Bid',
    timeLeft: 'Time Left',
    placeBid: 'Place Bid',
    viewDetails: 'View Details',
    
    // Categories
    categoriesTitle: 'Browse by Category',
    electronics: 'Electronics',
    jewelry: 'Jewelry',
    cars: 'Cars',
    furniture: 'Furniture',
    fashion: 'Fashion',
    collectibles: 'Collectibles',
    
    // How It Works
    howItWorksTitle: 'How Mzadd Works?',
    step1Title: 'Create Account',
    step1Description: 'Sign up for free and complete verification',
    step2Title: 'Browse Auctions',
    step2Description: 'Discover thousands of items in live auctions',
    step3Title: 'Place Your Bid',
    step3Description: 'Bid on items you love and win the auction',
    step4Title: 'Win & Receive',
    step4Description: 'Pay securely and receive your item',
    
    // Auction Details
    auctionDetails: 'Auction Details',
    description: 'Description',
    condition: 'Condition',
    startingPrice: 'Starting Price',
    reservePrice: 'Reserve Price',
    bidHistory: 'Bid History',
    seller: 'Seller',
    shippingInfo: 'Shipping Info',
    
    // Bidding
    yourBid: 'Your Bid',
    minimumBid: 'Minimum Bid',
    bidAmount: 'Bid Amount',
    confirmBid: 'Confirm Bid',
    bidPlaced: 'Bid placed successfully',
    outbid: 'You have been outbid',
    auctionWon: 'Congratulations! You won the auction',
    
    // Profile
    myProfile: 'My Profile',
    myBids: 'My Bids',
    wonAuctions: 'Won Auctions',
    watchlist: 'Watchlist',
    settings: 'Settings',
    
    // Forms
    email: 'Email',
    password: 'Password',
    confirmPassword: 'Confirm Password',
    fullName: 'Full Name',
    phoneNumber: 'Phone Number',
    submit: 'Submit',
    cancel: 'Cancel',
    save: 'Save',
    
    // Status
    active: 'Active',
    ended: 'Ended',
    upcoming: 'Upcoming',
    won: 'Won',
    lost: 'Lost',
    
    // Time
    days: 'days',
    hours: 'hours',
    minutes: 'minutes',
    seconds: 'seconds',
    
    // Footer
    aboutUs: 'About Us',
    privacyPolicy: 'Privacy Policy',
    termsOfService: 'Terms of Service',
    support: 'Support',
    followUs: 'Follow Us',
    allRightsReserved: 'All Rights Reserved'
  }
}

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    // Check localStorage first
    const savedLanguage = localStorage.getItem('mzadd_language')
    if (savedLanguage && ['ar', 'en'].includes(savedLanguage)) {
      return savedLanguage
    }
    
    // Check browser language
    const browserLanguage = navigator.language.toLowerCase()
    if (browserLanguage.startsWith('ar')) {
      return 'ar'
    }
    
    // Default to Arabic for Kuwait market
    return 'ar'
  })

  const [direction, setDirection] = useState(language === 'ar' ? 'rtl' : 'ltr')

  useEffect(() => {
    // Update document direction and language
    document.documentElement.dir = direction
    document.documentElement.lang = language
    
    // Save to localStorage
    localStorage.setItem('mzadd_language', language)
    
    // Update direction
    setDirection(language === 'ar' ? 'rtl' : 'ltr')
  }, [language, direction])

  const switchLanguage = (newLanguage) => {
    if (['ar', 'en'].includes(newLanguage)) {
      setLanguage(newLanguage)
    }
  }

  const t = (key) => {
    return translations[language][key] || key
  }

  const value = {
    language,
    direction,
    isRTL: language === 'ar',
    switchLanguage,
    t,
    translations: translations[language]
  }

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  )
}
