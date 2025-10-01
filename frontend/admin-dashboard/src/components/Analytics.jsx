import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const Analytics = () => {
  const revenueData = [
    { name: 'يناير', revenue: 4000 },
    { name: 'فبراير', revenue: 3000 },
    { name: 'مارس', revenue: 5000 },
    { name: 'أبريل', revenue: 4500 },
    { name: 'مايو', revenue: 6000 },
    { name: 'يونيو', revenue: 5500 }
  ]

  const userGrowthData = [
    { name: 'الأسبوع 1', users: 120 },
    { name: 'الأسبوع 2', users: 145 },
    { name: 'الأسبوع 3', users: 167 },
    { name: 'الأسبوع 4', users: 189 }
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">التحليلات والتقارير</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">إحصائيات مفصلة عن أداء المنصة</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>نمو الإيرادات</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="revenue" stroke="#3B82F6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>نمو المستخدمين</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={userGrowthData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="users" fill="#10B981" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-blue-600">45,678</p>
              <p className="text-sm text-gray-600">إجمالي الإيرادات (د.ك)</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-green-600">1,247</p>
              <p className="text-sm text-gray-600">إجمالي المستخدمين</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-purple-600">156</p>
              <p className="text-sm text-gray-600">إجمالي المزادات</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Analytics
