import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Gavel, Clock, DollarSign, Users, Eye, MoreHorizontal } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

const AuctionsManagement = () => {
  const [auctions] = useState([
    {
      id: 1,
      title: 'ساعة رولكس أصلية',
      current_price: 1500,
      total_bids: 23,
      end_time: '2024-01-25T18:00:00',
      status: 'active',
      merchant: 'أحمد محمد'
    },
    {
      id: 2,
      title: 'جهاز آيفون 15 برو',
      current_price: 800,
      total_bids: 15,
      end_time: '2024-01-24T20:00:00',
      status: 'active',
      merchant: 'سارة أحمد'
    }
  ])

  const getStatusBadge = (status) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      scheduled: 'bg-blue-100 text-blue-800',
      closed: 'bg-gray-100 text-gray-800'
    }
    const labels = { active: 'نشط', scheduled: 'مجدول', closed: 'منتهي' }
    return <Badge className={colors[status]}>{labels[status]}</Badge>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">إدارة المزادات</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">مراقبة وإدارة جميع المزادات</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">المزادات النشطة</p>
                <p className="text-2xl font-bold">23</p>
              </div>
              <Gavel className="w-8 h-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">إجمالي المزايدات</p>
                <p className="text-2xl font-bold">1,247</p>
              </div>
              <Users className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">إجمالي القيمة</p>
                <p className="text-2xl font-bold">45,678 د.ك</p>
              </div>
              <DollarSign className="w-8 h-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">المزادات المنتهية اليوم</p>
                <p className="text-2xl font-bold">8</p>
              </div>
              <Clock className="w-8 h-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>المزادات الحالية</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>المزاد</TableHead>
                <TableHead>السعر الحالي</TableHead>
                <TableHead>المزايدات</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>ينتهي في</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {auctions.map((auction, index) => (
                <motion.tr
                  key={auction.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <TableCell>
                    <div>
                      <div className="font-medium">{auction.title}</div>
                      <div className="text-sm text-gray-500">بواسطة {auction.merchant}</div>
                    </div>
                  </TableCell>
                  <TableCell className="font-bold">{auction.current_price} د.ك</TableCell>
                  <TableCell>{auction.total_bids}</TableCell>
                  <TableCell>{getStatusBadge(auction.status)}</TableCell>
                  <TableCell>
                    {new Date(auction.end_time).toLocaleString('ar-SA')}
                  </TableCell>
                  <TableCell>
                    <Button variant="ghost" size="sm">
                      <Eye className="w-4 h-4" />
                    </Button>
                  </TableCell>
                </motion.tr>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

export default AuctionsManagement
