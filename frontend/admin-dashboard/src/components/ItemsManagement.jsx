import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Package, CheckCircle, XCircle, Clock, Eye } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

const ItemsManagement = () => {
  const [items] = useState([
    {
      id: 1,
      name: 'ساعة رولكس أصلية',
      category: 'مجوهرات',
      start_price: 1000,
      status: 'pending',
      owner: 'أحمد محمد',
      created_at: '2024-01-20'
    },
    {
      id: 2,
      name: 'جهاز آيفون 15 برو',
      category: 'إلكترونيات',
      start_price: 600,
      status: 'active',
      owner: 'سارة أحمد',
      created_at: '2024-01-18'
    }
  ])

  const getStatusBadge = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      active: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
      sold: 'bg-blue-100 text-blue-800'
    }
    const labels = { pending: 'معلق', active: 'نشط', rejected: 'مرفوض', sold: 'مباع' }
    return <Badge className={colors[status]}>{labels[status]}</Badge>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">إدارة السلع</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">مراجعة وإدارة السلع المعروضة</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">إجمالي السلع</p>
                <p className="text-2xl font-bold">234</p>
              </div>
              <Package className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">في انتظار المراجعة</p>
                <p className="text-2xl font-bold">12</p>
              </div>
              <Clock className="w-8 h-8 text-yellow-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">السلع المعتمدة</p>
                <p className="text-2xl font-bold">198</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">السلع المرفوضة</p>
                <p className="text-2xl font-bold">24</p>
              </div>
              <XCircle className="w-8 h-8 text-red-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>قائمة السلع</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>السلعة</TableHead>
                <TableHead>الفئة</TableHead>
                <TableHead>السعر المبدئي</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>المالك</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.map((item, index) => (
                <motion.tr
                  key={item.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <TableCell>
                    <div className="font-medium">{item.name}</div>
                  </TableCell>
                  <TableCell>{item.category}</TableCell>
                  <TableCell className="font-bold">{item.start_price} د.ك</TableCell>
                  <TableCell>{getStatusBadge(item.status)}</TableCell>
                  <TableCell>{item.owner}</TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button variant="ghost" size="sm">
                        <Eye className="w-4 h-4" />
                      </Button>
                      {item.status === 'pending' && (
                        <>
                          <Button variant="ghost" size="sm" className="text-green-600">
                            <CheckCircle className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-red-600">
                            <XCircle className="w-4 h-4" />
                          </Button>
                        </>
                      )}
                    </div>
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

export default ItemsManagement
