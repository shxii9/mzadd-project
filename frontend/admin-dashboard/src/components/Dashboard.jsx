import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Users, 
  Gavel, 
  Package, 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  Activity,
  Clock,
  CheckCircle,
  AlertTriangle,
  Eye,
  MoreHorizontal
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 1247,
    totalMerchants: 89,
    totalBidders: 1158,
    activeAuctions: 23,
    totalAuctions: 156,
    totalItems: 234,
    pendingItems: 12,
    totalRevenue: 45678.90,
    monthlyRevenue: 12345.67,
    revenueGrowth: 12.5,
    userGrowth: 8.3,
    auctionGrowth: 15.2
  })

  const [recentActivity, setRecentActivity] = useState([
    { id: 1, type: 'auction', title: 'مزاد جديد: ساعة رولكس', user: 'أحمد محمد', time: '5 دقائق', status: 'active' },
    { id: 2, type: 'bid', title: 'مزايدة جديدة: 1500 د.ك', user: 'فاطمة علي', time: '12 دقيقة', status: 'success' },
    { id: 3, type: 'user', title: 'تاجر جديد انضم', user: 'محمد الكندري', time: '1 ساعة', status: 'pending' },
    { id: 4, type: 'item', title: 'سلعة جديدة للمراجعة', user: 'سارة أحمد', time: '2 ساعة', status: 'pending' },
    { id: 5, type: 'auction', title: 'انتهى مزاد: جهاز آيفون', user: 'خالد العتيبي', time: '3 ساعات', status: 'completed' }
  ])

  // Sample data for charts
  const revenueData = [
    { name: 'يناير', revenue: 4000, auctions: 24 },
    { name: 'فبراير', revenue: 3000, auctions: 18 },
    { name: 'مارس', revenue: 5000, auctions: 32 },
    { name: 'أبريل', revenue: 4500, auctions: 28 },
    { name: 'مايو', revenue: 6000, auctions: 35 },
    { name: 'يونيو', revenue: 5500, auctions: 31 },
    { name: 'يوليو', revenue: 7000, auctions: 42 }
  ]

  const categoryData = [
    { name: 'إلكترونيات', value: 35, color: '#3B82F6' },
    { name: 'مجوهرات', value: 25, color: '#10B981' },
    { name: 'سيارات', value: 20, color: '#F59E0B' },
    { name: 'أثاث', value: 12, color: '#EF4444' },
    { name: 'أخرى', value: 8, color: '#8B5CF6' }
  ]

  const userActivityData = [
    { name: 'السبت', active: 120, new: 12 },
    { name: 'الأحد', active: 98, new: 8 },
    { name: 'الاثنين', active: 145, new: 15 },
    { name: 'الثلاثاء', active: 132, new: 11 },
    { name: 'الأربعاء', active: 167, new: 18 },
    { name: 'الخميس', active: 189, new: 22 },
    { name: 'الجمعة', active: 156, new: 16 }
  ]

  const StatCard = ({ title, value, change, icon: Icon, trend, color = "blue" }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="hover:shadow-lg transition-shadow duration-300">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
              {change && (
                <div className="flex items-center mt-2">
                  {trend === 'up' ? (
                    <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-red-500 mr-1" />
                  )}
                  <span className={`text-sm font-medium ${
                    trend === 'up' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {change}%
                  </span>
                  <span className="text-sm text-gray-500 mr-1">من الشهر الماضي</span>
                </div>
              )}
            </div>
            <div className={`p-3 rounded-full bg-${color}-100 dark:bg-${color}-900/20`}>
              <Icon className={`w-6 h-6 text-${color}-600 dark:text-${color}-400`} />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )

  const getActivityIcon = (type) => {
    switch (type) {
      case 'auction': return Gavel
      case 'bid': return DollarSign
      case 'user': return Users
      case 'item': return Package
      default: return Activity
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
      case 'success': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'pending': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'completed': return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">لوحة التحكم</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            مرحباً بك في لوحة تحكم BidFlow - نظرة شاملة على أداء المنصة
          </p>
        </div>
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <Button variant="outline" size="sm">
            <Eye className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
            عرض التقرير الكامل
          </Button>
          <Button size="sm">
            تحديث البيانات
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="إجمالي المستخدمين"
          value={stats.totalUsers.toLocaleString()}
          change={stats.userGrowth}
          trend="up"
          icon={Users}
          color="blue"
        />
        <StatCard
          title="المزادات النشطة"
          value={stats.activeAuctions}
          change={stats.auctionGrowth}
          trend="up"
          icon={Gavel}
          color="green"
        />
        <StatCard
          title="السلع المعلقة"
          value={stats.pendingItems}
          icon={Package}
          color="yellow"
        />
        <StatCard
          title="الإيرادات الشهرية"
          value={`${stats.monthlyRevenue.toLocaleString()} د.ك`}
          change={stats.revenueGrowth}
          trend="up"
          icon={DollarSign}
          color="purple"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Chart */}
        <Card>
          <CardHeader>
            <CardTitle>الإيرادات والمزادات</CardTitle>
            <CardDescription>تطور الإيرادات وعدد المزادات خلال الأشهر الماضية</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="revenue" 
                  stroke="#3B82F6" 
                  strokeWidth={2}
                  name="الإيرادات (د.ك)"
                />
                <Line 
                  type="monotone" 
                  dataKey="auctions" 
                  stroke="#10B981" 
                  strokeWidth={2}
                  name="عدد المزادات"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Category Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>توزيع الفئات</CardTitle>
            <CardDescription>توزيع السلع حسب الفئات</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* User Activity and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* User Activity Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>نشاط المستخدمين</CardTitle>
            <CardDescription>المستخدمون النشطون والجدد خلال الأسبوع</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={userActivityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="active" fill="#3B82F6" name="المستخدمون النشطون" />
                <Bar dataKey="new" fill="#10B981" name="المستخدمون الجدد" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>النشاط الأخير</CardTitle>
            <CardDescription>آخر الأنشطة على المنصة</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => {
                const Icon = getActivityIcon(activity.type)
                return (
                  <motion.div
                    key={activity.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-start space-x-3 rtl:space-x-reverse p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                  >
                    <div className="p-2 rounded-full bg-gray-100 dark:bg-gray-700">
                      <Icon className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                        {activity.title}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        بواسطة {activity.user}
                      </p>
                      <div className="flex items-center justify-between mt-2">
                        <span className="text-xs text-gray-500">{activity.time}</span>
                        <Badge className={`text-xs ${getStatusColor(activity.status)}`}>
                          {activity.status === 'active' && 'نشط'}
                          {activity.status === 'success' && 'مكتمل'}
                          {activity.status === 'pending' && 'معلق'}
                          {activity.status === 'completed' && 'منتهي'}
                        </Badge>
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </div>
            <Button variant="outline" className="w-full mt-4">
              عرض جميع الأنشطة
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>إجراءات سريعة</CardTitle>
          <CardDescription>الإجراءات الأكثر استخداماً</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Button variant="outline" className="h-20 flex flex-col space-y-2">
              <Users className="w-6 h-6" />
              <span className="text-sm">إضافة مستخدم</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col space-y-2">
              <Package className="w-6 h-6" />
              <span className="text-sm">مراجعة السلع</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col space-y-2">
              <Gavel className="w-6 h-6" />
              <span className="text-sm">إدارة المزادات</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col space-y-2">
              <Activity className="w-6 h-6" />
              <span className="text-sm">عرض التقارير</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard
